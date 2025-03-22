import asyncio
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
   """

    async def process_query(self, session: ClientSession, query: str) -> None:
        print(f"*** {self.messages = } ***")
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
                all_message_content.append(content)

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
                self.messages.append(
                    {
                        "role": "assistant",
                        "content": getattr(response.content[0], "text", ""),
                    }
                )

                all_message_content.append(getattr(response.content[0], "text", ""))

            final_message = "\n".join([content.text for content in all_message_content])

            print(final_message)

    async def chat_loop(self, session: ClientSession):
        while True:
            query = input("\nQuery: ").strip()
            self.messages.append(
                MessageParam(
                    role="user",
                    content=query,
                )
            )

            await self.process_query(session, query)

    async def run(self):
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()

                await self.chat_loop(session)


chat = Chat()

asyncio.run(chat.run())
