import sqlite3
import json
from datetime import datetime,timezone

class notificationsDB():
    def crear_tablas_si_no_existen():
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()

        # Create tables if not exist previously
        cursor.execute('''CREATE TABLE IF NOT EXISTS registered_users (
                            user TEXT PRIMARY KEY,
                            notifications INTEGER,
                            admin INTEGER
                        )''')

        conn.commit()
        conn.close()

    def set_admin(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()        

        cursor.execute('SELECT user FROM registered_users WHERE user = ?', (user,))

        user_data = cursor.fetchone()
        status = 0
        if user_data: 
            cursor.execute('UPDATE registered_users SET admin = ? WHERE user = ?', (1, user))
        else:
            status = -1
        conn.commit()
        conn.close()

        return status
    

    def register_user(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM chat_theme WHERE user = ?', (user,))
        user_exists = cursor.fetchone()[0] > 0                
        status = 0
        if user_exists:            
            status = -1
        else:
            cursor.execute('INSERT INTO registered_users (user,notifications,admin) VALUES (?, ?, ?)',(user,0,0))            
        conn.commit()
        conn.close()
        return status

    def delete_user(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM registered_users WHERE user = ?',(user,))
        conn.commit()
        conn.close()

