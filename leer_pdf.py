import os
import fitz  # PyMuPDF
from chromadb import PersistentClient

# Ruta de tu carpeta con los PDFs (actualiza si cambias de ubicación)
RUTA_PDFS = os.path.join(os.path.expanduser("~"), "Desktop", "agente-legal-tedeco", "pdfs")

# Crear base de datos local (chroma_db debe estar en la raíz del proyecto)
chroma_client = PersistentClient(path="chroma_db")

# Crear o acceder a una colección
coleccion = chroma_client.get_or_create_collection(name="documentos_legales")

# Función para leer un PDF y extraer su texto
def leer_pdf(ruta_archivo):
    try:
        with fitz.open(ruta_archivo) as doc:
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
            return texto
    except Exception as e:
        print(f"❌ Error al leer {ruta_archivo}: {e}")
        return ""

# Procesar todos los archivos PDF en la carpeta
for archivo in os.listdir(RUTA_PDFS):
    if archivo.endswith(".pdf"):
        ruta_completa = os.path.join(RUTA_PDFS, archivo)
        print(f"📄 Leyendo: {archivo}")
        texto = leer_pdf(ruta_completa)

        if texto.strip():
            coleccion.add(
                documents=[texto],
                metadatas=[{"nombre_archivo": archivo}],
                ids=[archivo]  # El ID debe ser único
            )
        else:
            print(f"⚠️ El archivo {archivo} no contiene texto legible.")

print("✅ Todos los PDFs fueron procesados y almacenados en ChromaDB.")
