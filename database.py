from sqlite3 import *
from datetime import datetime


'''
GET THE USER CHECKS HISTORY
'''
def get_user_history(id):
    connection = connect("users.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT datetime,speed,distance,step,left,right FROM main WHERE id=={id}")
    history_of_id=cursor.fetchall()
    connection.close()
    return history_of_id


'''
DELETE THE USER CHECKS HISTORY
'''
def delet(id):
    connection = connect("users.db")
    cursor = connection.cursor()

    cursor.execute(f"DELETE FROM main WHERE id=={id}")
    connection.commit()
    connection.close()


'''
INSERT A NEW CHECKS TO THE USER HISTORY
'''
def insert_check(id,time,data):
    connection = connect("users.db")
    cursor = connection.cursor()
    for d in data:
        insert=f"INSERT INTO main (id,datetime,speed,distance,step,left,right) VALUES (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(insert,(str(id),time,f"{d[0]} m/s",f"{d[1]} m",f"{d[2]} m",f"{d[3]} %",f"{d[4]} %"))
    connection.commit()
    connection.close()