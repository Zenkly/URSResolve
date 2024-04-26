import sqlite3

class userTypesDB():
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

    def toggle_notifications(user,value):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()        

        cursor.execute('SELECT user FROM registered_users WHERE user = ?', (user,))

        user_data = cursor.fetchone()
        status = 0
        if user_data: 
            cursor.execute('UPDATE registered_users SET notifications = ? WHERE user = ?', (value, user))
        else:
            status = -1
        conn.commit()
        conn.close()

        return status

    def toggle_admin(admin,user,value):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()                
        if userTypesDB.is_admin(admin):
            cursor.execute('SELECT user FROM registered_users WHERE user = ?', (user,))

            user_data = cursor.fetchone()
            status = 0
            if user_data: 
                cursor.execute('UPDATE registered_users SET admin = ? WHERE user = ?', (value, user))
            else:
                status = -5
            conn.commit()
            conn.close()
        else:
            status = -1
        return status
    
    def is_admin(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()        
        cursor.execute('SELECT admin FROM registered_users WHERE user = ?', (user,))
        is_admin = cursor.fetchone()[0]        
        if is_admin:            
            if int(is_admin) == 1:
                return True
        return False
  
    
    def unset_admin(admin,user):
        return userTypesDB.toggle_admin(admin,user,0)

    def set_admin(admin,user):
        return userTypesDB.toggle_admin(admin,user,1)
    
    def unset_notifications(user):
        return userTypesDB.toggle_notifications(user,0)

    def set_notifications(user):
        return userTypesDB.toggle_notifications(user,1)
    
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
        
    def register_user(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM registered_users WHERE user = ?', (user,))
        user_exists = cursor.fetchone()[0] > 0                
        status = 0
        if user_exists:            
            pass
        else:
            cursor.execute('INSERT INTO registered_users (user,notifications,admin) VALUES (?, ?, ?)',(user,0,0))            
        conn.commit()
        conn.close()
        return

    def delete_user(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM registered_users WHERE user = ?',(user,))
        conn.commit()
        conn.close()

