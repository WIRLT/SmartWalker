import customtkinter as ctk
from tkinter import ttk,messagebox
from datetime import datetime
import database
import check_run
import server_connection

defult_color="steelblue2"

#########################################################################################
#                                    FUNCTIONS SECTION                                  #
#########################################################################################

'''
CHECK THE ID INPUT
'''
def check_id(id):
    if not id.isdigit():
        return False
    id_num=int(id)
    if id_num<0 or id_num>999999999:
        return False
    id=id.zfill(9)
    c=0
    for d in range(len(id)):
        result=int(id[d])*((d%2)+1)
        if result>9:
            result=(result%10)+1
        c+=result
    if c%10 != 0:
        return False
    return True

'''
START THE CHECK OPEN NEW WINDOW FOR IT
'''
def start():
    global win
    id=ID_input.get()
    time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if check_id(id):
        win=check_run.check_window(ID=id,TIME=time)
    else:
        messagebox.showwarning(title="Warning",message="ID Is Incorrect!")

'''
SHOW USER HISTORY ON MAIN WINDOW
'''
def history():
    id=ID_input.get()
    table.delete(*table.get_children())
    if check_id(id):
        user_data=database.get_user_history(id)
        for d in user_data:
            table.insert(parent='',index=0,values=d)
    else:
        messagebox.showwarning(title="Warning",message="ID Is Incorrect!")

'''
DELETE ALL USER HISTORY
'''
def delete_all():
    id=ID_input.get()
    if check_id(id):
        if messagebox.askokcancel("Warning!","Delete All History"):
            table.delete(*table.get_children())
            user_data=database.delet(id)
    else:
        messagebox.showwarning(title="Warning",message="ID Is Incorrect!")


#########################################################################################
#                                    BULID WINDOW                                       #
#########################################################################################
main_window = ctk.CTk()
main_window.title('smart walker')
main_window.geometry('850x400')
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("light")

'''
CREATE DATABASE FOR USERS IF NOT CREATED ALREADY
'''
connection = database.connect("users.db")
cursor = connection.cursor()
cursor.execute(f"CREATE TABLE IF NOT EXISTS main (id TEXT,datetime TEXT,speed TEXT,distance TEXT,step TEXT,left TEXT,right TEXT)")
connection.commit()
connection.close()

frame_top = ctk.CTkFrame(main_window,fg_color=defult_color)
frame_top.pack(fill="x")

frame_bottom = ctk.CTkFrame(main_window)
frame_bottom.pack(expand=True,fill="both")

#########################################################################################
#                                    HEADER                                             #
#########################################################################################
title_label = ctk.CTkLabel(frame_top,text="Smart Walker",font=("Times New Roman", 30,'bold'))
title_label.pack(side='top',expand=True,pady=10)

ID_label = ctk.CTkLabel(frame_top,text="ID: ",font=("Arial", 20,'bold'))
ID_label.pack(side='left',padx=10,pady=10)

'''ID INPUT TEXT'''
ID_input = ctk.CTkEntry(frame_top,font=("Arial", 16))
ID_input.pack(side='left',pady=10,ipadx=10)


'''HISTORY DELETE BUTTUN'''
history_delete_buttun= ctk.CTkButton(frame_top,text='DELETE HISTORY',command=delete_all)
history_delete_buttun.pack(side='right',pady=10,padx=5)

'''HISTORY BUTTUN'''
history_buttun= ctk.CTkButton(frame_top,text='HISTORY',command=history)
history_buttun.pack(side='right',pady=10,padx=90)

'''START BUTTUN'''
start_buttun= ctk.CTkButton(frame_top,text='START',command=start)
start_buttun.pack(side='left',pady=10,padx=20)
 

'''TABLE CREATION'''
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 17)) # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 19,'bold'))
style.configure('mystyle.Treeview', rowheight=30)
table=ttk.Treeview(frame_bottom,columns=('DATE','SPEED','DISTANCE','STEP','LEFT','RIGHT'),show='headings',style="mystyle.Treeview")
table.heading('DATE',text='DATE/TIME')
table.column('DATE',anchor="center")
table.heading('SPEED',text='SPEED')
table.column('SPEED',anchor="center")
table.heading('DISTANCE',text='DISTANCE')
table.column('DISTANCE',anchor="center")
table.heading('STEP',text='STEP SIZE')
table.column('STEP',anchor="center")
table.heading('LEFT',text='LEFT HAND FORCE')
table.column('LEFT',anchor="center")
table.heading('RIGHT',text='RIGHT HAND FORCE')
table.column('RIGHT',anchor="center")
table.pack(fill='both',expand='True',padx=20, pady=20)
server_connection.connection_setup()
main_window.mainloop()
