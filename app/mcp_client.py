import asyncio
import re
from dataclasses import dataclass, field
from typing import Union, cast

import anthropic
from anthropic.types import MessageParam, TextBlock, ToolUnionParam, ToolUseBlock
from anthropic.types.message import Message
from config import Config
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

anthropic_client = anthropic.AsyncAnthropic(api_key=Config.ANTHROPIC_API_KEY)


class LlmModels:
    CLAUDE_3_7_SONNET_LATEST = "claude-3-7-sonnet-latest"
    CLAUDE_3_5_SONNET_LATEST = "claude-3-5-sonnet-latest"


# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["app/mcp_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)


@dataclass
class Chat:
    messages: list[MessageParam] = field(default_factory=list)

    system_prompt: str = """
        You are an expert SQLite assistant whose primary function is to execute SQL queries and provide 
        relevant information to users. Follow these guidelines:

        1. DATA SECURITY:
        - Do not reveal sensitive database information (table names, users, fields) unless specifically requested by the user.
        - For ambiguous questions, ask for clarification instead of displaying confidential information.

        2. QUERIES AND RESPONSES:
        - Execute SQL queries requested using the available tools.
        - Present results clearly and in a structured manner.
        - For complex queries, briefly explain your approach.

        3. PROACTIVE ASSISTANCE:
        - Help refine imprecise or poorly structured queries.
        - Suggest optimizations when appropriate.
        - Provide query examples when the user needs guidance.

        4. ACCEPTABLE REQUEST TYPES:
        - "Give me information about..." (requires specificity)
        - "Calculate the average of..."
        - "Show records that..."
        - "How many users have...?"
        - "Execute this query: [SQL]"

        5. PRIVACY:
        - Confirm before executing queries that might expose sensitive data.
        - Remember to only execute SQL queries within the permitted context.

        A continuación el esquema de la tabla de "asegurados"

        Descripción de Variables de Datos Abiertos de Asegurados

        Variables de Identificación Geográfica
        - cve_delegacion: Clave numérica que identifica la delegación de adscripción operativa del IMSS. Existen 35 delegaciones en total.
        - cve_subdelegacion: Clave numérica que identifica la subdelegación de adscripción operativa del IMSS. Existen 133 subdelegaciones en total.
        - cve_entidad: Clave numérica que identifica la entidad federativa asociada a la ubicación del patrón asegurado ante el IMSS.
        - cve_municipio: Clave numérica que identifica el municipio asociado a la ubicación del patrón asegurado ante el IMSS.

        Variables de Sector Económico
        - sector_economico_1: Clasificación de primer nivel de la actividad económica de los patrones afiliados al IMSS.
        - sector_economico_2: Clasificación de segundo nivel de la actividad económica de los patrones afiliados al IMSS.
        - sector_economico_4: Clasificación de cuarto nivel de la actividad económica de los patrones afiliados al IMSS.

        Variables de Características del Trabajador
        - tamaño_patron: Tamaño del patrón determinado con base en el número de asegurados vigentes que registra ante el IMSS. Se clasifica en rangos desde S1 (con un puesto de trabajo) hasta S7 (con más de 1,000 puestos de trabajo).
        - sexo: Clasificación del asegurado como hombre (1), mujer (2) o no binario (3).
        - rango_edad: Rango de edad asociado al asegurado, clasificado desde E1 (menor de 15 años) hasta E14 (mayor de 75 años).
        - rango_salarial: Rango salarial en número de veces el salario mínimo de la Ciudad de México, desde W1 (hasta 1 vez el salario mínimo) hasta W25 (mayor a 24 y hasta 25 veces el salario mínimo).
        - rango_uma: Rango salarial en número de veces la Unidad de Medida y Actualización (UMA), desde U1 (hasta 1 vez el salario mínimo) hasta U25 (mayor a 24 y hasta 25 veces el valor de la UMA).

        Variables de Conteo
        - asegurados: Personas que están aseguradas en el IMSS de manera directa como titulares, incluye todas las modalidades de aseguramiento. La cifra contabiliza a todas las personas afiliadas en el IMSS, ya sea como "puestos trabajo afiliados al IMSS (empleos asegurados)" o como "asegurados sin un empleo (cotizantes sin un puesto de trabajo asociado)". Aquellas personas afiliadas con más de un tipo de afiliación (ej. estudiantes y trabajador) se contabilizan tantas veces como tipos de afiliación mantengan.
        - no_trabajadores: Número de trabajadores.
        - ta: Total de puestos de trabajo afiliados al IMSS (empleo asegurado o asegurados asociados a un empleo).
        - teu: Total de puestos de trabajo eventuales urbanos.
        - tec: Total de puestos de trabajo eventuales del campo.
        - tpu: Total de puestos de trabajo permanentes urbanos.
        - tpc: Total de puestos de trabajo permanentes del campo.

        Variables de Salario
        - ta_sal: Total de puestos de trabajo afiliados con un salario asociado. Incluye las modalidades de aseguramiento asociadas a un empleo y con salario relativo a un ingreso real otorgado por parte de un patrón (10, 13, 14, 17, 34, 36, 38 y 42).
        - teu_sal: Total de puestos de trabajo eventuales urbanos con salario asociado.
        - tec_sal: Total de puestos de trabajo eventuales del campo con salario asociado.
        - tpu_sal: Total de puestos de trabajo permanentes urbanos con salario asociado.
        - tpc_sal: Total de puestos de trabajo permanentes del campo con salario asociado.

        Variables de Masa Salarial
        - masa_sal_ta: Masa salarial total de puestos de trabajo afiliados. Se refiere a la nómina que considera tanto el salario como la plantilla de trabajadores. El salario base de cotización reportado por los patrones al IMSS integra pagos en efectivo por cuota diaria, gratificaciones, percepciones, alimentación, habitación, primas, comisiones, prestaciones en especie y cualquier otra cantidad o prestación entregada al trabajador por su trabajo, con las excepciones previstas en el artículo 27 de la Ley del Seguro Social.
        - masa_sal_teu: Masa salarial de puestos de trabajo eventuales urbanos.
        - masa_sal_tec: Masa salarial de puestos de trabajo eventuales del campo.
        - masa_sal_tpu: Masa salarial de puestos de trabajo permanentes urbanos.
        - masa_sal_tpc: Masa salarial de puestos de trabajo permanentes del campo.
   """

    async def process_query(self, session: ClientSession, query: str) -> str:
        response = await session.list_tools()
        available_tools: list[ToolUnionParam] = [
            {
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema,
            }
            for tool in response.tools
        ]

        # Initial Claude API call
        response = await anthropic_client.messages.create(
            model=LlmModels.CLAUDE_3_5_SONNET_LATEST,
            system=self.system_prompt,
            max_tokens=8_000,
            messages=self.messages,
            tools=available_tools,
        )

        assistant_message_content: list[Union[ToolUseBlock, TextBlock]] = []

        all_message_content = []

        for content in response.content:

            if content.type == "text":
                assistant_message_content.append(content)
                all_message_content.append(content.text)

            elif content.type == "tool_use":
                tool_name = content.name
                tool_args = content.input

                # Execute tool call
                result = await session.call_tool(tool_name, cast(dict, tool_args))

                assistant_message_content.append(content)
                self.messages.append(
                    {"role": "assistant", "content": assistant_message_content}
                )
                self.messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,
                                "content": getattr(result.content[0], "text", ""),
                            }
                        ],
                    }
                )
                # Get next response from Claude
                response = await anthropic_client.messages.create(
                    model=LlmModels.CLAUDE_3_5_SONNET_LATEST,
                    max_tokens=8_000,
                    messages=self.messages,
                    tools=available_tools,
                )
                text_response = getattr(response.content[0], "text", "")
                all_message_content.append(f"\n{text_response}")

                self.messages.append({"role": "assistant", "content": text_response})

        final_message = "\n".join([text for text in all_message_content])

        return final_message

    async def chat_loop(self, session: ClientSession):
        while True:
            query = input("\nQuery: ").strip()
            response = ""
            self.messages.append(
                MessageParam(
                    role="user",
                    content=query,
                )
            )

            response = await self.process_query(session, query)
            print(response)

    async def chat_loop_2(self, session: ClientSession, user_query: str):
        self.messages.append(
            MessageParam(
                role="user",
                content=user_query.strip(),
            )
        )

        return await self.process_query(session, user_query)

    async def run(self):
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                await self.chat_loop(session)

    async def get_chat_response(self, user_query: str) -> str:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                return await self.chat_loop_2(session, user_query)


if __name__ == "__main__":
    chat = Chat()
    asyncio.run(chat.run())
