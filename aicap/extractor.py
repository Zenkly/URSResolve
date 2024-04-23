import os
import re

class Extractor:
    def __init__(self,ruta):
        self.ruta = ruta
        self.leer_archivos_en_carpeta()
        self.fragmentos = None


    def leer_archivos_en_carpeta(self):
        diccionario_archivos = {}
        for archivo in os.listdir(self.ruta):
            if archivo.endswith('.txt'):
                ruta_completa = os.path.join(self.ruta, archivo)
                with open(ruta_completa, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                    titulo = os.path.splitext(archivo)[0]  # Obtiene el título sin la extensión
                    diccionario_archivos[titulo] = contenido
        self.diccionario_archivos = diccionario_archivos

    def fragmentar_contenido(self):
        diccionario_fragmentado = {}
        for titulo, contenido in self.diccionario_archivos.items():
            segmentos = re.split(r'\*{3}(.+?)\*{3}', contenido)
            segmentos = [seg.strip() for seg in segmentos if seg.strip()]  # Eliminar segmentos vacíos
            lista_diccionarios = []        
            for i in range(0, len(segmentos), 2):
                diccionario_segmento = {
                    'titulo': titulo,
                    'seccion': segmentos[i-1] if i != 0 else "Introducción",
                    'contenido': segmentos[i]
                }
                lista_diccionarios.append(diccionario_segmento)
            diccionario_fragmentado[titulo] = lista_diccionarios

        fragmentar_por_articulo = []

        for titulo, lista_segmentos in diccionario_fragmentado.items():
            if "Reglamento" in titulo:
                patron_art=r'Artículo (\d+)\.\s*\n(.*?)((?=Artículo \d+\.\s*\n)|$)'
                for segmento in lista_segmentos:
                    coincidencias = re.findall(patron_art, segmento['contenido'], re.DOTALL)
                    if len(coincidencias) == 0:        
                        fragmentar_por_articulo.append({
                            'titulo' : titulo,
                            'seccion': segmento['seccion'],
                            'contenido': segmento['contenido'],
                        })
                    for articulo, contenido,_ in coincidencias:
                        fragmentar_por_articulo.append({
                            'titulo' : titulo,
                            'seccion': segmento['seccion'] + ": " + 'Artículo '+ articulo,
                            'contenido': contenido.strip()
                        })
            elif "LINEAMIENTO" in titulo:
                patron_art=r'([IVX]+?)\.(.*?)((?=[IVX]+\.|$))'
                for segmento in lista_segmentos:
                    coincidencias = re.findall(patron_art, segmento['contenido'], re.DOTALL)
                    if len(coincidencias) == 0:        
                        fragmentar_por_articulo.append({
                            'titulo' : titulo,
                            'seccion': segmento['seccion'],
                            'contenido': segmento['contenido'],
                        })
                    for articulo, contenido,_ in coincidencias:
                        fragmentar_por_articulo.append({
                            'titulo' : titulo,
                            'seccion': segmento['seccion'] + ": " + 'Sección '+ articulo,
                            'contenido': contenido.strip()
                        })
            elif "Lineamientos" in titulo:
                patron_art=r'-{3}(.+?)-{3}(.*?)(?=-{3}(.+?)-{3}|$)'
                for segmento in lista_segmentos:
                    coincidencias = re.findall(patron_art, segmento['contenido'], re.DOTALL)
                    if len(coincidencias) == 0:        
                        fragmentar_por_articulo.append({
                            'titulo' : titulo,
                            'seccion': segmento['seccion'],
                            'contenido': segmento['contenido'],
                        })
                    for articulo, contenido,_ in coincidencias:
                        fragmentar_por_articulo.append({
                            'titulo' : titulo,
                            'seccion': segmento['seccion'] + ": " + 'Sección '+ articulo,
                            'contenido': contenido.strip()
                        })
            else:
                patron_art=r'-{3}(.+?)-{3}(.*?)(?=-{3}(.+?)-{3}|$)'
                for segmento in lista_segmentos:
                    coincidencias = re.findall(patron_art, segmento['contenido'], re.DOTALL)
                    if len(coincidencias) == 0:        
                        fragmentar_por_articulo.append({
                            'titulo' : titulo,
                            'seccion': segmento['seccion'],
                            'contenido': segmento['contenido'],
                        })
                        # print({
                        #     'titulo' : titulo,
                        #     'seccion': segmento['seccion'],
                        #     'contenido': segmento['contenido'],
                        # })
                    for articulo, contenido,_ in coincidencias:                        
                        fragmentar_por_articulo.append({
                            'titulo' : titulo,
                            'seccion': segmento['seccion'] + ": " + 'Sección '+ articulo,
                            'contenido': contenido.strip()
                        })
                        # print({
                        #         'titulo' : titulo,
                        #         'seccion': segmento['seccion'] + ": " + 'Sección '+ articulo,
                        #         'contenido': contenido.strip()
                        #     })
        self.fragmentos = fragmentar_por_articulo
        return fragmentar_por_articulo
