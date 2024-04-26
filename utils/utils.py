import os
# Extract information from txt files
from aicap.extractor import Extractor
# Create Vectorstore
from aicap.vectorstore import Vectorstore

def get_dir_names(path):
    # Varify if path is directory
    if not os.path.isdir(path):
        print("Path isn't a directory.")
        return []
    # Obtain directories names
    dir_names = [nombre for nombre in os.listdir(path) if os.path.isdir(os.path.join(path, nombre))]
    
    return dir_names

def get_themes(path):

    directories = get_dir_names(path)
    themes = {}
    for dir in directories:
    # Read and process files
        documentos = Extractor(path+"/"+dir+"/")
        documentos.leer_archivos_en_carpeta()
        fragmentar_por_articulo = documentos.fragmentar_contenido()
        
        vectorstore = Vectorstore(fragmentar_por_articulo)
        themes[dir]={"vectorstore":vectorstore, "preamble":documentos.preamble}
    return themes
