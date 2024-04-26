import sqlite3
import csv


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

    def user_answered_survey(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user FROM surveys WHERE user = ?',(user,))
        user_data = cursor.fetchone()
        if user_data:
            return True
        return False

    def export_to_csv(user):
        conn = sqlite3.connect('./chats_db/datos.db')
        cursor = conn.cursor()
        table = cursor.execute('SELECT * FROM surveys')

        fields = [field[0] for field in table.description]

        with open("./chats_db/surveysTable.csv",'w',newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(fields)

            for row in table.fetchall():
                csv_writer.writerow(row)

        conn.close()