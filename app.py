from flask import Flask, request, jsonify
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import os

# Configuración de la app Flask
app = Flask(__name__)

# Ruta a la base de datos Chroma
persist_directory = "chroma_db"
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

@app.route("/")
def home():
    return "✅ Asesor Legal TEDECO en línea"

@app.route("/preguntar", methods=["POST"])
def preguntar():
    try:
        data = request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "Falta el campo 'pregunta' en el cuerpo del JSON"}), 400

        # Buscar documentos similares
        documentos = vectordb.similarity_search(pregunta, k=3)
        respuestas = []

        for i, doc in enumerate(documentos, start=1):
            respuestas.append({
                "fuente": f"Documento {i}",
                "contenido": doc.page_content[:1000]  # Máx. 1000 caracteres por respuesta
            })

        return jsonify({
            "pregunta": pregunta,
            "respuestas": respuestas
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
