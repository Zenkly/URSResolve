import sqlite3
import json
from datetime import datetime,timezone

class historyDB():
    def crear_tablas_si_no_existen():
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()

        # Create tables if not exist previously
        cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
                            id INTEGER PRIMARY KEY,
                            user TEXT,
                            arreglo TEXT
                        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS chat_theme (
                            user TEXT PRIMARY KEY,
                            theme TEXT,
                            time INTEGER
                        )''')

        conn.commit()
        conn.close()

    def get_theme(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()        

        cursor.execute('SELECT theme,time FROM chat_theme WHERE user = ?', (user,))

        user_data = cursor.fetchone()

        

        if user_data: 
            theme,time = user_data
            print(f"El tema del usuario {user}, es {theme} declarado en {time}")
            now = int(datetime.now().timestamp())
            print(time)
            time_diff = now - time
            print(time_diff)
            if time_diff > 300:
                cursor.execute('DELETE FROM chat_theme WHERE user = ?',(user,))
                print("Debes definir un nuevo tema")
                theme = "expired"
        else:
            theme = None
            print(f"Debes definir un tema antes de iniciar a preguntar")
        
        conn.commit()
        conn.close()

        return theme
    

    def set_theme(user,theme):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM chat_theme WHERE user = ?', (user,))
        user_exists = cursor.fetchone()[0] > 0
        now = int(datetime.now().timestamp())
        print(now)
        if user_exists:
            cursor.execute('UPDATE chat_theme SET theme = ?, time = ? WHERE user = ?', (theme, now, user))
        else:
            cursor.execute('INSERT INTO chat_theme (user,theme,time) VALUES (?, ?, ?)',(user,theme,now))
        conn.commit()
        conn.close()

    def uset_theme(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM chat_theme WHERE user = ?',(user,))
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
