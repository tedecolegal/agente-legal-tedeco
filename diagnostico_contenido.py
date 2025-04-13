from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os

# Esta línea solo si estás ejecutando localmente (no en Render)
os.environ["OPENAI_API_KEY"] = "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"

persist_directory = "chroma_db"
embedding = OpenAIEmbeddings()

vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Diagnóstico: cuántos documentos están indexados
print(f"📚 Documentos indexados en la base: {vectordb._collection.count()}")

# Muestra ejemplos de lo que se puede consultar
docs = vectordb.similarity_search("¿Qué leyes están disponibles?", k=5)
for i, doc in enumerate(docs):
    print(f"\n📄 Documento {i+1}:\n{doc.page_content[:500]}...")
