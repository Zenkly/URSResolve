import sqlite3
import json
from datetime import datetime,timezone

class surveysDB():
    def crear_tablas_si_no_existen():
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()

        # Create tables if not exist previously
        cursor.execute('''CREATE TABLE IF NOT EXISTS surveys (
                            id INTEGER PRIMARY KEY,
                            user INTEGER,
                            q1 TEXT,
                            q2 TEXT,
                            q3 TEXT
                        )''')

        conn.commit()
        conn.close()
    
    def register_user(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO surveys (user) VALUES (?)',(user,))
        id = cursor.lastrowid
        conn.commit()
        conn.close()       
        return id

    def register_answer(id,question,answer):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()        
        id_int = int(id)
        q_lower = question.lower()
        cursor.execute('SELECT user FROM surveys WHERE id = ?', (id_int,))
        user_data = cursor.fetchone()
        status = 0
        #print(type(id),question,answer)
        print("USER_DATA")
        print(user_data)
        if user_data: 
            print(id,question,answer)

            cursor.execute(f'UPDATE surveys SET {q_lower} = ? WHERE id = ?', (answer,id_int))
        else:
            status = -1
        conn.commit()
        conn.close()

        return status

      
    def get_user_data(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()        

        cursor.execute('SELECT notifications,admin FROM registered_users WHERE user = ?', (user,))
        user_data = cursor.fetchone()
        if user_data:
            notifications,admin =user_data
            return (notifications,admin)
        else:
            return -1

    def delete_user(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM registered_users WHERE user = ?',(user,))
        conn.commit()
        conn.close()

