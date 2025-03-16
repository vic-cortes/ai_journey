import sqlite3

import numpy as np
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Configuración inicial
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

# 2. Conexión a la base de datos
conn = sqlite3.connect("inventario_productos.db")
cursor = conn.cursor()

# Asumimos que tenemos una tabla de productos con descripciones
# y otra tabla con preguntas frecuentes vectorizadas


# 3. Función para generar consultas SQL basadas en la entrada del usuario
def generate_sql_query(user_query):
    system_message = """
    Eres un asistente experto en SQL. Tu tarea es convertir la siguiente consulta 
    en lenguaje natural a una consulta SQL válida para una base de datos de inventario 
    de productos. La base de datos tiene la siguiente estructura:
    
    - productos(id, nombre, categoria, precio, stock, descripcion)
    
    Responde SOLO con la consulta SQL sin explicaciones.
    """

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=f"Genera una consulta SQL para: {user_query}"),
    ]

    response = llm(messages)
    sql_query = response.content

    return sql_query


# 4. Función para realizar búsqueda semántica en la base de conocimiento
def semantic_search(user_query, top_k=3):
    # Vectorizar la consulta del usuario
    query_embedding = model.encode([user_query])[0]

    # Obtener todos los documentos y sus embeddings (en una situación real se usaría una base de vectores)
    cursor.execute("SELECT id, pregunta, respuesta, embedding FROM faq_vectorizada")
    faqs = cursor.fetchall()

    similarities = []
    for id, pregunta, respuesta, embedding_str in faqs:
        # Convertir string de embedding almacenado a numpy array
        doc_embedding = np.fromstring(embedding_str, sep=",")
        # Calcular similitud
        similarity = cosine_similarity([query_embedding], [doc_embedding])[0][0]
        similarities.append((id, pregunta, respuesta, similarity))

    # Ordenar por similitud y devolver los top_k
    similarities.sort(key=lambda x: x[3], reverse=True)
    return similarities[:top_k]


# 5. Función principal del RAG Híbrido
def hybrid_rag(user_query):
    # Parte 1: Consulta directa a la base de datos
    try:
        sql_query = generate_sql_query(user_query)
        cursor.execute(sql_query)
        db_results = cursor.fetchall()

        # Convertir resultados a DataFrame para mejor manipulación
        column_names = [description[0] for description in cursor.description]
        df_results = pd.DataFrame(db_results, columns=column_names)
        structured_data = df_results.to_dict(orient="records")
    except Exception as e:
        structured_data = []
        print(f"Error en consulta SQL: {e}")

    # Parte 2: Búsqueda semántica
    semantic_results = semantic_search(user_query)

    # Parte 3: Generar respuesta combinada
    system_prompt = """
    Eres un asistente de atención al cliente. Utiliza la información proporcionada 
    para responder a la consulta del usuario. Combina la información estructurada de 
    la base de datos con el conocimiento de las preguntas frecuentes cuando sea relevante.
    Estructura tu respuesta de manera clara y precisa.
    """

    context = f"""
    Datos estructurados de la base de datos:
    {structured_data}
    
    Información relevante de preguntas frecuentes:
    {[{
        'pregunta': item[1],
        'respuesta': item[2],
        'relevancia': item[3]
    } for item in semantic_results]}
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"Contexto: {context}\n\nConsulta del usuario: {user_query}"
        ),
    ]

    response = llm(messages)
    return response.content


# 6. Ejemplo de uso
if __name__ == "__main__":
    user_query = "¿Qué laptops gaming tienen más de 16GB de RAM y están en stock?"
    response = hybrid_rag(user_query)
    print(response)
    print(response)
