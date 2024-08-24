from typing import Tuple
import customtkinter as ctk
import database
import server_connection
import threading
import numpy as np 
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
defult_color="steelblue2"
data=(0,0,0,0,0,0)
esp32_ip = "192.168.4.1"  # IP address of the ESP32 in access point mode
port = 8050  # Set the desired port number
dis,ind=0,0
flag=False
force_x,speed_x,speed_0_y,speed_1_y,force_0_y,force_1_y=[],[],[],[],[],[]



class check_window(ctk.CTkToplevel):
    def __init__(self,ID=0,TIME="", *args, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        
        self.data=[] #Temporary memory
        self.temp_data=() #current check

        #########################################################################################
        #                                    FUNCTIONS SECTION                                  #
        #########################################################################################
        '''
        WHEN FINISH BUTTUN IS PRESSED SAVE CHECK DATA TO DATABASE AND CLOSE WINDOW
        '''
        def finish():
            global dis,speed_x,force_x,speed_0_y,speed_1_y,force_0_y,force_1_y,step,ind
            database.insert_check(ID,TIME,self.data)
            dis,ind,step=0,0,0
            force_x,speed_x,speed_0_y,speed_1_y,force_0_y,force_1_y=[],[],[],[],[],[]
            flag=False
            plt.close('all')
            self.destroy()


        '''
        WHEN SAVE BUTTUN IS PREESED ADD CURRENT DATA SHOWED TO TEMPRORAY MEMORY
        '''
        def save():
            self.data.append(self.temp_data)

        '''control the speed plot'''
        def speed_plt(i):
            ax0.cla()
            ax0.plot(speed_x, speed_0_y, label="speed left")  # Plot the first line
            ax0.plot(speed_x, speed_1_y, label="speed right")  # Plot the second line
            ax0.legend(loc='upper right')
        
        '''control the force plot'''
        def force_plt(i):
            ax1.cla()
            ax1.plot(force_x, force_0_y, label="force left")  # Plot the first line
            ax1.plot(force_x, force_1_y, label="force right")  # Plot the second line
            ax1.legend(loc='upper right')


        '''
        UPDATE DATA ON THE SECREEN EVERY SECONDE
        '''
        def update_values():
            global dis, data, flag,ind
            # Update the values displayed in the labels
            d=server_connection.get_data()
            if d !=None:
                #print(d)
                if len(d)==6:
                    data=d
                    flag=True
                    speed_x.append(ind)
                    force_x.append(ind)
                    ind+=1
                    if ind>10:
                        speed_x.pop(0)
                        force_x.pop(0)
                        speed_0_y.pop(0)
                        speed_1_y.pop(0)
                        force_0_y.pop(0)
                        force_1_y.pop(0)
                    speed_0_y.append(float(data[0]))
                    speed_1_y.append(float(data[1]))
                    force_0_y.append(float(data[4]))
                    force_1_y.append(float(data[5]))
            speed=(float(data[0])+float(data[1]))/2
            speed="%.2f" % speed
            if flag:
                dis+=float(data[2])
                flag=False
            distance=str("{:.2f}".format(dis))
            step=data[3]
            left_pressure=data[4]
            right_pressure=data[5]
            self.temp_data=(speed,distance,step,left_pressure,right_pressure)
            speed_label.configure(text=f"Speed\n {speed} m/s")
            distance_label.configure(text=f"Distance\n {distance} m")
            step_label.configure(text=f"Step Size\n {step} m")
            left_hand_label.configure(text=f"Left Hand Pressure\n {left_pressure} %")
            right_hand_label.configure(text=f"Right Hand Pressure\n {right_pressure} %")
            left_hand_progress.set(float(left_pressure)/100)
            right_hand_progress.set(float(right_pressure)/100)
            # Schedule the update_values function to be called again after 1000 milliseconds (1 second)
            self.after(200, update_values)
        

        #########################################################################################
        #                                     WINDOW BUILD                                      #
        #########################################################################################
        self.title('smart walker')
        self.geometry('800x600')
        ctk.set_default_color_theme("dark-blue")
        ctk.set_appearance_mode("light")


        frame_top = ctk.CTkFrame(self,fg_color=defult_color)
        frame_top.pack(fill="x")

        frame_left = ctk.CTkFrame(self)
        frame_left.pack(side="left",expand=True,fill="both")

        frame_right = ctk.CTkFrame(self)
        frame_right.pack(side="right",expand=True,fill="both")
        #########################################################################################
        #                                           HEADER                                      #
        #########################################################################################
        title_label = ctk.CTkLabel(frame_top,text="Check in progress",font=("Times New Roman", 30,'bold'))
        title_label.pack(anchor="n",expand=True,pady=10)

        ID_label = ctk.CTkLabel(frame_top,text="ID: "+str(ID),font=("Arial", 20,'bold'))
        ID_label.pack(anchor="w",expand=True,pady=10,padx=10)

        #########################################################################################
        #                                           BODY                                        #
        #########################################################################################

        '''SPEED'''
        frame_speed = ctk.CTkFrame(frame_left,border_color=defult_color,border_width=3)
        frame_speed.pack(anchor="center",expand=True,ipadx=110,ipady=20,pady=10)
        speed_label = ctk.CTkLabel(frame_speed,text="Speed",font=("Arial", 22))
        speed_label.pack(anchor="center",expand=True)

        '''DISTANCE'''
        frame_distance = ctk.CTkFrame(frame_left,border_color=defult_color,border_width=3)
        frame_distance.pack(anchor="center",expand=True,ipadx=110,ipady=20,pady=10)
        distance_label = ctk.CTkLabel(frame_distance,text="Distance",font=("Arial", 22))
        distance_label.pack(anchor="center",expand=True)
        
        '''STEP SIZE'''
        frame_step = ctk.CTkFrame(frame_left,border_color=defult_color,border_width=3)
        frame_step.pack(anchor="center",expand=True,ipadx=110,ipady=20,pady=10)
        step_label = ctk.CTkLabel(frame_step,text="Step Size",font=("Arial", 22))
        step_label.pack(anchor="center",expand=True)

        '''LEFT HAND FORCE'''
        frame_left_hand = ctk.CTkFrame(frame_left,border_color=defult_color,border_width=3)
        frame_left_hand.pack(anchor="center",side="left",expand=True,ipadx=20,ipady=10,pady=10)
        left_hand_label = ctk.CTkLabel(frame_left_hand,text="Left Hand Pressure",font=("Arial", 22))
        left_hand_label.pack(anchor="center",expand=True)
        left_hand_progress = ctk.CTkProgressBar(frame_left_hand,height=15,progress_color=defult_color,width=200)
        left_hand_progress.pack(anchor="center",pady=5)

        '''RIGHT HAND FORCE'''
        frame_right_hand = ctk.CTkFrame(frame_left,border_color=defult_color,border_width=3)
        frame_right_hand.pack(anchor="center",side="right",expand=True,ipadx=20,ipady=10,pady=10)
        right_hand_label = ctk.CTkLabel(frame_right_hand,text="Right Hand Pressure",font=("Arial", 22))
        right_hand_label.pack(anchor="center",expand=True)
        right_hand_progress = ctk.CTkProgressBar(frame_right_hand,height=15,progress_color=defult_color,width=200)
        right_hand_progress.pack(anchor="center",pady=5)

        ''' FINISH BUTTUN '''
        finish_button = ctk.CTkButton(frame_right, text="FINISH",command=finish)
        finish_button.pack(anchor="s",side="right",padx=20, pady=40,ipadx=20, ipady=20)

        ''' SAVE BUTTUN '''
        save_button = ctk.CTkButton(frame_right, text="SAVE",command=save)
        save_button.pack(anchor="center",side="right",padx=20, pady=40,ipadx=20, ipady=20)

        '''plots of speed'''
        fig0, ax0 = plt.subplots()
        canvas0= FigureCanvasTkAgg(fig0,master=frame_right)
        canvas0.get_tk_widget().pack(anchor="center",side="top",pady=10,padx=10)
        canvas0.get_tk_widget().config(width=900, height=380)
        ani0 = FuncAnimation(fig0, speed_plt, interval=1000)
        '''plots of force'''
        fig1, ax1 = plt.subplots()
        canvas1= FigureCanvasTkAgg(fig1,master=frame_right)
        canvas1.get_tk_widget().pack(anchor="center",side="top",pady=10,padx=10)
        canvas1.get_tk_widget().config(width=900, height=380)
        ani1 = FuncAnimation(fig1, force_plt, interval=1000)

        #########################################################################################
        #                                window attrubite                                       #
        #########################################################################################

        thread = threading.Thread(target=update_values)
        self.protocol("WM_DELETE_WINDOW", finish)
        thread.start()
        self.state('zoomed')
        self.mainloop()


