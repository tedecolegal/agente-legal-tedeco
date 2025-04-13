from flask import Flask, request, jsonify
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import os

app = Flask(__name__)

# Configuración de la base de datos
persist_directory = "chroma_db"
embedding = OpenAIEmbeddings()

try:
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
except Exception as e:
    vectordb = None
    print(f"❌ Error al cargar ChromaDB: {e}")

@app.route("/")
def home():
    return "✅ Asesor Legal TEDECO en línea"

@app.route("/preguntar", methods=["POST"])
def preguntar():
    if vectordb is None:
        return jsonify({"error": "La base de datos no está disponible"}), 500

    try:
        data = request.get_json()
        pregunta = data.get("pregunta")

        if not pregunta:
            return jsonify({"error": "Falta el campo 'pregunta'"}), 400

        documentos = vectordb.similarity_search(pregunta, k=3)
        respuestas = []

        for i, doc in enumerate(documentos, 1):
            respuestas.append({
                "fuente": f"Documento {i}",
                "contenido": doc.page_content[:1000]  # Máx. 1000 caracteres
            })

        if not respuestas:
            return jsonify({"respuesta": "No se encontraron coincidencias legales"}), 200

        return jsonify({
            "pregunta": pregunta,
            "respuestas": respuestas
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Puerto dinámico para Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
