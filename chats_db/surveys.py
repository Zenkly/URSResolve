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
                            q1 INTEGER,
                            q2 INTEGER,
                            q3 INTEGER,
                            q4 INTEGER,
                            q5 INTEGER,
                            q6 INTEGER,
                            q7 INTEGER,
                            q8 INTEGER,
                            q9 INTEGER,
                            q10 INTEGER
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
        cursor.execute('SELECT id FROM surveys WHERE id = ?', (id,))

        user_data = cursor.fetchone()
        status = 0
        if user_data: 
            cursor.execute('UPDATE surveys SET ? = ? WHERE id = ?', (question, answer,id))
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

