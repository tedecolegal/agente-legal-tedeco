# Importar bibliotecas necesarias
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pdfplumber

# Autenticación usando el archivo clave_api.json
gauth = GoogleAuth()
gauth.LoadClientConfigFile("clave_api.json")  # Aquí va exactamente tu archivo actual (no lo modifiques)
gauth.LocalWebserverAuth()  # Abrirá navegador automáticamente para que autorices acceso
drive = GoogleDrive(gauth)

# Tu Folder ID exacto (ya confirmado antes)
folder_id = '15vbBX-G4rMpENtVs0vQjpdd7sla-E2VG'

# Listar archivos PDF en tu carpeta específica
file_list = drive.ListFile({
    'q': f"'{folder_id}' in parents and mimeType='application/pdf'"
}).GetList()

# Descargar y extraer texto automáticamente de cada PDF
for file in file_list:
    file.GetContentFile(file['title'])  # Descarga archivo PDF
    
    texto_completo = ""
    with pdfplumber.open(file['title']) as pdf:
        for page in pdf.pages:
            texto_pagina = page.extract_text()
            if texto_pagina:
                texto_completo += texto_pagina.strip() + '\n'

    print(f"\n📄 Archivo: {file['title']} — Texto extraído:\n")
    print(texto_completo[:1500])  # Muestra los primeros 1500 caracteres
