import sqlite3
import json

class historyDB():
    def crear_tabla_si_no_existe():
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()

        # Crear la tabla si no existe
        cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                            id INTEGER PRIMARY KEY,
                            user TEXT,
                            arreglo TEXT
                        )''')
        
        conn.commit()
        conn.close()

    def guardar_arreglo(user,arreglo):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()

        # Convertir el arreglo a JSON antes de guardarlo en la base de datos
        arreglo_json = json.dumps(arreglo)

        # Insertar el arreglo en la tabla
        cursor.execute('INSERT INTO chat_history (user,arreglo) VALUES (?,?)', (user,arreglo_json,))
        
        conn.commit()
        conn.close()

    def obtener_historial(user,openAi=False):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()

        # Obtener el arreglo de la tabla
        cursor.execute('SELECT arreglo FROM chat_history WHERE user=? ORDER BY id DESC LIMIT 5',(user,))
        resultado = reversed(cursor.fetchall())
        #print(resultado)
        conn.close()

        historial_db = []
        if resultado:
            for entrada in resultado:
                # Convertir el JSON de la base de datos de nuevo a un arreglo de Python
                #print("entrada")
                #print(entrada)
                if not openAi:
                    historial_db.extend(json.loads(entrada[0]))
                else:
                    message_array = json.loads(entrada[0])
                    for msg in message_array:                                
                        formated_message = {}
                        if msg["role"]=="USER":
                            formated_message["role"]='user'
                        else:
                            formated_message["role"]='assistant'
                        formated_message["content"]=msg["text"]
                        historial_db.append(formated_message)
                #print("historial")
                #print(historial_db)
        
        return historial_db
