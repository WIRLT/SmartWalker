import socket
import time
from tkinter import messagebox
HOST = '192.168.4.1'  # The server's hostname or IP address
#HOST = '127.0.0.1'
PORT = 12345  # The port used by the server
soc = None

'''
handle erorrs in connection
'''
def handle_error():
    global soc
    try:
        soc.close()
    except OSError as e:
        print(e)
    finally:
        soc=None


'''
create new connection
'''
def connection_setup():
    global soc
    i=0
    while True:
        i+=1
        if i==2:
            messagebox.showerror("Error","connection faild! check wifi")
            break
        try:
            soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the ESP32 
            soc.connect((HOST, PORT))
            soc.setblocking(False)
            print("Connected to the walker system.")
            break
        except:
            print("failed attempting to reconnect in 3 seconds")
            time.sleep(3)
            handle_error()

'''
recive data from the system
'''
def get_data():
    try:
        data = soc.recv(50)  # 30 is the buffer size
        if data:
            data = data.decode('utf-8')
            data=data.split(",")
            if data[-1]=='0':
                return tuple(data[:-1])
        return None
    except OSError as e:
        if e.args[0] == 10035:  # EAGAIN or EWOULDBLOCK
            pass
        else:
            print(e.args)
            handle_error()
            connection_setup()
    