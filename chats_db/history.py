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

    def obtener_historial(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()

        # Obtener el arreglo de la tabla
        cursor.execute('SELECT arreglo FROM chat_history WHERE user=? ORDER BY id DESC LIMIT 5',(user,))
        resultado = reversed(cursor.fetchall())
        print(resultado)
        conn.close()

        historial_db = []
        if resultado:
            for entrada in resultado:
                # Convertir el JSON de la base de datos de nuevo a un arreglo de Python
                print("entrada")
                print(entrada)
                historial_db.extend(json.loads(entrada[0]))
                print("historial")
                print(historial_db)
        
        return historial_db
