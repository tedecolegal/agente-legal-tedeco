import os
import fitz  # PyMuPDF
from chromadb import PersistentClient

# Ruta de tu carpeta con los PDFs
RUTA_PDFS = r"C:\Users\abiga\Documentos\SEGUROS DERECHOS"

# Crear base de datos local
chroma_client = PersistentClient(path="chroma_db")

# Crear colección (una especie de carpeta dentro de la base de datos)
coleccion = chroma_client.get_or_create_collection(name="documentos_legales")

# Función para leer un PDF y extraer su texto
def leer_pdf(ruta_archivo):
    with fitz.open(ruta_archivo) as doc:
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        return texto

# Leer cada archivo PDF de la carpeta
for archivo in os.listdir(RUTA_PDFS):
    if archivo.endswith(".pdf"):
        ruta_completa = os.path.join(RUTA_PDFS, archivo)
        print(f"📄 Leyendo: {archivo}")

        texto = leer_pdf(ruta_completa)

        # Guardar en la colección
        coleccion.add(
            documents=[texto],
            metadatas=[{"nombre_archivo": archivo}],
            ids=[archivo]  # ID único por nombre de archivo
        )

print("✅ Todos los PDFs fueron leídos y almacenados en ChromaDB.")

