#! /usr/bin/python3

'''
This file contains GUI code for Configuring PiArm Servo
Developed by - SB Components
http://sb-components.co.uk
'''

import piarm
import meter
import shutil
import logging
import threading
import webbrowser
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from os import path, system
from serial.tools import list_ports

##########################  MainApp  ###########################################
class MainApp(piarm.PiArm, tk.Tk):
    '''
    This is a class for Creating Frames and Buttons for left and top frame
    '''
    def __init__(self, *args, **kwargs):
        global logo, img
    
        tk.Tk.__init__(self, *args, **kwargs)

        self.screen_width=tk.Tk.winfo_screenwidth(self)
        self.screen_height=tk.Tk.winfo_screenheight(self)
        self.app_width=800
        self.app_height= 480
        self.xpos = (self.screen_width/2)-(self.app_width/2)
        self.ypos = (self.screen_height/2)-(self.app_height/2)
        self.port = None
        
        self.geometry("%dx%d+%d+%d" %(self.app_width,self.app_height,self.xpos,
                                      self.ypos))
        self.title(" Servo Configuration")
        if not self.screen_width > self.app_width:
            self.attributes('-fullscreen', True)
            
        self.config(bg="gray85")
        
        img = tk.PhotoImage(file= Root_Dir + '/Images/settings.png')
        logo = tk.PhotoImage(file= Root_Dir + '/Images/sblogo.png')
        
        self.top_frame=tk.Frame(self,height=int(self.app_height/15),bd=2,
                                width=self.app_width,bg="gray85")
        self.top_frame.pack(padx=(225,0),side="top",fill="both")
        self.top_frame.pack_propagate(0)
        
        self.left_frame=tk.Frame(self,width=int(self.app_width/4),bg="gray85")
        self.left_frame.pack(side="left", fill="both")
        self.left_frame.pack_propagate(0)
        
        self.right_frame=tk.Frame(self,bg="gray85")
        self.right_frame.pack(side="left",fill="both",expand=True)

        self.label_font=font.Font(family="Helvetica",size=10)
        self.heading_font=font.Font(family="Helvetica",size=12)

        self.topframe_contents()

        self.frames={}
        
        for F in(OperateFrame,ParameterFrame, AboutFrame):
            frame_name=F.__name__
            frame=F(parent=self.right_frame,controller=self)
            self.frames[frame_name]=frame
            frame.config(bg="white")
            frame.grid(row=0,column=0, sticky="nsew")

        ports = list(list_ports.comports())
        for p in ports:
            if "USB2.0-Serial" in p:
                self.port = ((p.device).split("/"))[2]
                
        self.leftframe_contents()
        self.show_frame("OperateFrame")

        labelName = tk.Label(self, text="PiArm", bg="gray85",fg='SteelBlue', font=("Helvetica", 20))
        labelName.place(x=60,y=0)

    def close_Robot(self):
        '''
        This function delete the temp folder and close PiArm
        '''
        try:
            shutil.rmtree(Root_Dir + '/.Temp')
        except FileNotFoundError:
            pass
        self.log.info('PiArm Closed Successfully..!!')
        self.destroy()

    def operateButton(self):
        '''
        This function raise and sunk Operate button on top frame
        '''
        self.operate_button.config(relief="sunken", fg="SteelBlue2")
        self.about_button.config(relief="raised", fg="black")
        self.param_button.config(relief="raised", fg="black")
        self.show_frame("OperateFrame")

    def parameterButton(self):
        '''
        This function raise and sunk Parameter button on top frame
        '''
        self.operate_button.config(relief="raised", fg="black")
        self.about_button.config(relief="raised", fg="black")
        self.param_button.config(relief="sunken", fg="turquoise4")
        retFrame = self.get_frame("OperateFrame")
        if retFrame.readFlag == True:
            retFrame.servoContinousRead()
        self.show_frame("ParameterFrame")

    def aboutButton(self):
        '''
        This function raise and sunk About Us button on top frame
        '''
        self.operate_button.config(relief="raised", fg="black")
        self.param_button.config(relief="raised", fg="black")
        self.about_button.config(relief="sunken", fg="SteelBlue2")
        self.show_frame("AboutFrame")

    def manualButton(self):
        '''
        This function will open a pdf file in pdf reader
        '''
        system("xdg-open " + Root_Dir + "/Manuals/Servo_Config.pdf")
        

    def topframe_contents(self):
        '''
        This function creates the top frame buttons
        '''
        self.closeButton = tk.Button(self.top_frame, text='Close',fg="black",
                                     bg="gray90",font = self.label_font, bd=2,
                                     highlightthickness=0,
                                     command=self.close_Robot)
        self.closeButton.pack(padx=15,side="right")

        self.manual_button=tk.Button(self.top_frame,text="Manual",fg="black",
                               bg="gray90",font = self.label_font,bd=2,
                               highlightthickness=0, command = self.manualButton)
        self.manual_button.pack(padx = 15, side="right")

        self.about_button=tk.Button(self.top_frame,text="About Us",fg="black",
                               bg="gray90",font = self.label_font,bd=2,
                               highlightthickness=0,command=self.aboutButton)
        self.about_button.pack(padx = 15,side="right")
        
        self.param_button=tk.Button(self.top_frame,text="Parameters",fg="black",
                                    bg="gray90",font = self.label_font, bd=2,
                                    highlightthickness=0,
                                    command=self.parameterButton)
        self.param_button.pack(padx = 15,side="right")

        self.operate_button=tk.Button(self.top_frame,text="Operation", fg="black",
                                 bg="gray90",font = self.label_font, bd=2,
                                 highlightthickness=0,
                                 command=self.operateButton)
        self.operate_button.pack(padx=15,side="right")

        
    def leftframe_contents(self):
        '''
        This function creates the left frame widgets
        '''
        global logo
        
        serial_box=tk.Canvas(self.left_frame,width=200,
                               height=150,bg="white",bd=2)
        serial_box.grid(row=0, column=0, sticky="n", padx=10, pady=20)
        serial_box.grid_propagate(False)

        for i in range (4):
            serial_box.grid_rowconfigure(i,weight=1)
            if i < 3:
                serial_box.grid_columnconfigure(i,weight=1)
        
        serial_heading=tk.Label(serial_box,bg="SteelBlue2",fg="white",
                                text="Serial",font=self.heading_font)
        serial_heading.grid(row=0, column=0, columnspan=3, sticky="new",padx=2,
                          pady=2)

        com_label = tk.Label(serial_box, bg="white", fg="Black",text="Comm Port",
                             font=self.label_font)
        com_label.grid(row=1, column=0)

        self.com_entry = tk.Entry(serial_box,width=13,font = self.label_font)
        self.com_entry.grid(row=1, column=2)
        if self.port:
            self.com_entry.insert(0, self.port)

        baud_label = tk.Label(serial_box, bg="white", fg="Black",text="Baudrate",
                             font=self.label_font)
        baud_label.grid(row=2, column=0)

        baud_entry = tk.Entry(serial_box,width=13,font = self.label_font)
        baud_entry.insert("end", "115200")
        baud_entry.grid(row=2, column=2)
        baud_entry.config(state="readonly")

        self.circle=tk.Canvas(serial_box,height=40, width=40,bg="white",bd=0)
        self.indication = self.circle.create_oval(10,10,30,30, fill="red")
        self.circle.grid(row=3, column=0)

        self.connect_button = tk.Button(serial_box,text="Connect",bg="gray90",
                                   font=self.label_font, command = self.connectPort)
        self.connect_button.grid(row=3, column=2)

        label = tk.Label(self.left_frame, image=logo,height=40, width=225, bg='white')
        label.place(x=0,y=400)

    def connectPort(self):
        '''
        This function connects the serial port
        '''
        if self.connect_button.cget('text') == 'Connect' and self.com_entry.get():
            robot.connect("/dev/"+self.com_entry.get())
            if robot.alive:
                self.connect_button.config(relief="sunken", text="Disconnect")
                self.circle.itemconfigure(self.indication, fill="green3")
                self.com_entry.config(state="readonly")
            
        elif self.connect_button.cget('text') == 'Disconnect':
            retFrame = self.get_frame("OperateFrame")
            if retFrame.readFlag == True:
                messagebox.showinfo("Thread Error","Stop Continuos Read..!!")
            else:
                self.connect_button.config(relief="raised", text="Connect")
                self.circle.itemconfigure(self.indication, fill="red")
                robot.disconnect()
                self.com_entry.config(state="normal")
        else:
            errorLabel = tk.Label(self.left_frame, text="Enter Comm Port..!!",
                                  bg="yellow")
            errorLabel.grid(row=4, column=0)
            errorLabel.after(2000, errorLabel.grid_forget)

    def show_frame(self,frame_name):
        '''
        This function raise the frame on Top
        Args:
            frame_name: Name of the Frame
        '''
        frame=self.frames[frame_name]
        frame.tkraise()

    def get_frame(self, frame_name):
        '''
        This function returns the address of given frame
        Args:
            frame_name: Name of the Frame
        Return:
            Address of frame_name
        '''
        return self.frames[frame_name]
        
################################### Operate ####################################
class OperateFrame(tk.Frame):
    '''
    This is a class for creating widgets for Operation frame
    '''
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.readFlag = False
        for i in range(2):
            self.grid_columnconfigure(i,weight=1)

        self.controller.operate_button.config(relief="sunken", fg="SteelBlue3")

        self.IDVar = tk.IntVar()
        self.IDVar.set(1)
        self.posScaleVar = tk.IntVar()
        self.timeScaleVar = tk.IntVar()
        
        id_box=tk.Canvas(self,width=int(self.controller.app_width/3.5),
                         height=int(self.controller.app_height/6),bd=2,
                         bg="white")
        id_box.grid(row=0, column=0, padx=10, pady=5)
        id_box.grid_propagate(0)

        for i in range (3):
            id_box.grid_columnconfigure(i,weight=1)
            if i < 2:
                id_box.grid_rowconfigure(i,weight=1)

        id_heading=tk.Label(id_box,bg="SteelBlue2",fg="white",
                                text="ID",font=self.controller.heading_font)
        id_heading.grid(row=0, column=0, columnspan=3, sticky="new",padx=2,
                          pady=2)

        id_label = tk.Label(id_box, bg="white", fg="Black",text="Servo ID(1~253):",
                             font=self.controller.label_font)
        id_label.grid(row=1, column=0, pady=(0,8))

        id_vcmd = (self.register(self.id_validate),'%P')
        self.id_entry = tk.Entry(id_box, validate='key', validatecommand = id_vcmd,
                                        width=6, textvariable=self.IDVar)
        self.id_entry.grid(row=1, column=2, pady=(0,8))

        self.readServo_button = tk.Button(id_box,text="Read",bg="gray90",
                                          command=self.servoContinousRead)
        self.readServo_button.grid(row=2, column=0, pady=(0,5))

        servo_box=tk.Canvas(self,width=int(self.controller.app_width/3.5),
                            height=int((self.controller.app_height/2)),
                            bg="white",bd=2)
        servo_box.grid(row=1, column=0, padx=10,pady=5)
        servo_box.grid_propagate(0)
        
        for i in range (4):
            servo_box.grid_columnconfigure(i,weight=1)

        servo_heading=tk.Label(servo_box,bg="SteelBlue2",fg="white",
                                text="Servo Test",font=self.controller.heading_font)
        servo_heading.grid(row=0, column=0, columnspan=4, sticky="new",padx=2,
                          pady=2)

        time_label = tk.Label(servo_box, text="Time (ms)",bg="white",fg="red",
                              font=self.controller.label_font)
        time_label.grid(row=1,column=0)

        time_vcmd = (self.register(self.time_validate),'%P')
        time_entry=tk.Entry(servo_box, validate='key', validatecommand = time_vcmd, 
                            width=6, font=self.controller.label_font,
                            textvariable=self.timeScaleVar)
        time_entry.grid(row=2,column=0)

        time_scale=tk.Scale(servo_box,orient="horizontal",bg="white",from_=0, to=3000,
                            troughcolor="gray90",highlightthickness=0,
                            variable=self.timeScaleVar)
        time_scale.grid(row=2,column=1,columnspan=3,sticky="ew",padx=5, pady=(0,12))

        pos_label = tk.Label(servo_box, text="Position",bg="white",fg="green",
                              font=self.controller.label_font)
        pos_label.grid(row=3,column=0, pady=(10,0))

        pos_vcmd = (self.register(self.pos_validate),'%P')
        pos_entry=tk.Entry(servo_box, validate='key', validatecommand = pos_vcmd, width=6, font=self.controller.label_font,
                            textvariable=self.posScaleVar)
        pos_entry.bind('<Return>', self.updatePosValue)
        pos_entry.grid(row=4,column=0)

        pos_scale=tk.Scale(servo_box,orient="horizontal",bg="white",from_=0, to=1000,
                           variable=self.posScaleVar, command=self.updatePosValue,
                           troughcolor="gray90",highlightthickness=0)

        pos_scale.grid(row=4,column=1,columnspan=3,sticky="ew",padx=5, pady=(0,12))

        write_button = tk.Button(servo_box,text="Write", command = self.writeServo)
        write_button.grid(row=5, column=1,pady=(10,0))


        motor_box=tk.Canvas(self,
                            width=int(self.controller.app_width/3.5),
                            height=int(self.controller.app_height/6),bg="white",bd=2)
        motor_box.grid(row=2, column=0, padx=10, pady=5)
        motor_box.grid_propagate(0)
        motor_box.grid_columnconfigure(0,weight=1)

        motor_heading=tk.Label(motor_box,bg="SteelBlue2",fg="white",
                                text="Torque On/Off ",font=self.controller.heading_font)
        motor_heading.grid(row=0, column=0,sticky="new",padx=2,
                          pady=2)
        self.motorButton = tk.Button(motor_box,text="ON",bg="green3",
                                   font=20, command = self.servoTorque)
        self.motorButton.grid(row=1, column=0,padx=5,pady=5)

        status_box=tk.Canvas(self, width=310,height=10,bg="white",bd=2)
        status_box.grid(row=0, column=1,rowspan=3,pady=5,padx=(0,10),
                        sticky = "nsew")
        status_box.grid_propagate(0)

        status_box.grid_columnconfigure(0,weight=1)

        status_heading = tk.Label(status_box,bg="SteelBlue2",fg="white",
                                  text="Current Status",font=self.controller.heading_font)
        status_heading.grid(row=0, column=0,sticky="nsew",padx=2,pady=2)

        self.posGauge = meter.PositionMeter(status_box, max_value=1000, min_value=0,size=180)
        self.posGauge.grid(row=1,column=0, pady=(0,20))

        self.volGauge = meter.VoltageMeter(status_box,max_value=10, min_value= 0,
                                            size=200)
        self.volGauge.grid(row=2,column=0)

        self.tempScale=tk.Scale(status_box,from_=-10, to=150,width=10, orient="horizontal",
                                label="Temperature °C",font=("helvetica",11),bg="white",
                                troughcolor="tomato",fg="black",highlightthickness=0)
        self.tempScale.grid(row=3,column=0, columnspan=2, pady=20,padx=20,sticky="nsew")

    def id_validate(self, new_value):
        '''
        This function will validate servo ID
        '''
        try:
            if new_value == '':
                return True
            if int(new_value) in range(1, 254):
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False

    def time_validate(self, new_value):
        '''
        This function will validate Time range
        '''
        try:
            if new_value == '':
                return True
            if int(new_value) in range(3001):
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False
    
    def pos_validate(self, new_value):
        '''
        This function will validate Position for servo
        '''
        try:
            if new_value == '':
                return True
            if int(new_value) in range(1001):
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False
        
    def writeServo(self):
        '''
        This function write time and position slider values to servo motor
        '''
        try:
            if robot.alive:
                if self.id_entry.get() == '':
                    messagebox.showerror("Servo Id", "Please enter Servo Id..!!")
                else:
                    robot.servoWrite(int(self.id_entry.get()), int(self.posScaleVar.get()),
                                    int(self.timeScaleVar.get()))
            else:
                messagebox.showerror("Comm Error", "Comm Port is not Connected..!!")

        except ValueError:
            messagebox.showerror("Value Error", "Incorrect Entry Value")

    def servoTorque(self):
        '''
        This function enable and disbale servo motor torque
        '''
        if robot.alive:
            if self.motorButton.cget('text') == 'ON' and self.id_entry.get():
                self.motorButton.config(relief="sunken", bg="tomato", text="OFF")
                robot.torqueServo(int(self.id_entry.get()), 1)
                              
            elif self.motorButton.cget('text') == 'OFF' and self.id_entry.get():
                self.motorButton.config(relief="raised", bg="green3",text="ON")
                robot.torqueServo(int(self.id_entry.get()), 0)

            elif self.id_entry.get() == '':
                messagebox.showerror("Servo Id", "Please enter Servo Id..!!")

        else:
            messagebox.showerror("Comm Error", "Comm Port is not Connected..!!")

    def updatePosValue(self, value):
        '''
        This function write time and position slider values to servo motor
        '''
        if robot.alive:
            if self.id_entry.get() != '':
                robot.servoWrite(int(self.id_entry.get()), int(self.posScaleVar.get()),
                                     int(self.timeScaleVar.get()))
    
    def servoContinousRead(self):
        '''
        This function create thread to read params from servo motor
        '''
        if robot.alive:
            if self.readServo_button.cget('text') == 'Read' and self.id_entry.get():
                self.readServo_button.config(relief="sunken", text="Stop")
                self.id_entry.config(state="readonly")
                self.readFlag = True
                self.threadContRead = threading.Thread(target=self._continousRead)
                self.threadContRead.daemon = True
                self.threadContRead.start()
                            
            elif self.readServo_button.cget('text') == 'Stop':
                self.readServo_button.config(relief="raised", text="Read")
                self.id_entry.config(state="normal")
                self.readFlag = False

            elif self.id_entry.get() == '':
                messagebox.showerror("Servo Id", "Please enter Servo Id..!!")
            
        else:
            messagebox.showerror("Comm Error", "Comm Port is not Connected..!!")
            

    def _continousRead(self):
        '''
        This thread read params from servo motor & display on gauge
        '''
        try:
            while self.readFlag:
                response = robot.positionRead(int(self.id_entry.get()))
                pos = int.from_bytes(response[5]+response[6], byteorder='little')
                if pos > 1100:
                    pos = 0
                self.posGauge.set_value(int(pos))
            
                response = robot.voltageRead(int(self.id_entry.get()))
                voltage = int.from_bytes(response[5]+response[6], byteorder='little')
                self.volGauge.set_value(float(voltage/1000))

                response = robot.tempRead(int(self.id_entry.get()))
                temp = int.from_bytes(response[5], byteorder='little')
                self.tempScale.set(temp)

                if not self.readFlag:
                    self.posGauge.set_value(int(0))
                    self.volGauge.set_value(float(0))
                    self.tempScale.set(0)
                    break
        except TypeError:
            self.servoContinousRead()
            messagebox.showerror("Response Error", "No Response from Motor..!!")
        
################################### Parameters #################################
class ParameterFrame(tk.Frame):
    '''
    This is a class for Creating widgets for Paramter frame
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        for i in range(3):
            self.grid_columnconfigure(i,weight=1)

        self.ID_Var = tk.IntVar()
        self.ID_Var.set(1)
        self.offset_Var = tk.IntVar()
        self.led_textlabel = tk.StringVar()
        self.led_textlabel.set('Press Button to switch Off\nServo Led')

        self.image_LedOff = tk.PhotoImage(file = Root_Dir + '/Images/ledOff.png')
        self.image_LedOn = tk.PhotoImage(file = Root_Dir + '/Images/ledOn.png')
                
        id_box=tk.Canvas(self,width=int(2*(self.controller.app_width/9)),
                         height=int(self.controller.app_height/6),bg="white",bd=2)
        id_box.grid(row=0, column=0, padx=10, pady=5,sticky="w")
        id_box.grid_propagate(0)

        for k in range (3):
            id_box.grid_columnconfigure(k,weight=1)
            if i < 2:
                id_box.grid_rowconfigure(k,weight=1)

        id_heading=tk.Label(id_box,bg="turquoise3",fg="white",
                                text="ID",font=self.controller.heading_font)
        id_heading.grid(row=0, column=0, columnspan=3, sticky="new",padx=2,
                          pady=2)

        id_label = tk.Label(id_box, bg="white", fg="Black",text="Servo ID(1~253):",
                             font=self.controller.label_font)
        id_label.grid(row=1, column=0, pady=20)

        id_vcmd = (self.register(self.id_validate), '%P')
        self.id_entry = tk.Entry(id_box,validate='key', validatecommand = id_vcmd,
                                 width=6,font = self.controller.label_font,
                                 textvariable=self.ID_Var)
        self.id_entry.grid(row=1, column=2)

        deviation_box=tk.Canvas(self,
                                width=int(2*(self.controller.app_width/9)),
                                height=int(self.controller.app_height/6),bg="white",bd=2)
        deviation_box.grid(row=1, column=0, padx=10, pady=5,sticky="w")
        deviation_box.grid_propagate(0)

        for j in range(2):
            deviation_box.grid_columnconfigure(j,weight=1)

        deviation_heading=tk.Label(deviation_box,bg="turquoise3",fg="white",
                                   text="Deviation",font=self.controller.heading_font)
        deviation_heading.grid(row=0, column=0, columnspan=2, sticky="new",
                               padx=2,pady=2)

        id_vcmd = (self.register(self.deviation_validate), '%P')
        self.deviation_entry=tk.Entry(deviation_box, validate='key', validatecommand = id_vcmd, 
                                            width=4, textvariable = self.offset_Var)
        self.deviation_entry.grid(row=1,column=0, pady=18)


        deviation_scale=tk.Scale(deviation_box,orient="horizontal",bg="white",from_=-125,
                                 to=125,troughcolor="gray90",highlightthickness=0,
                                 variable=self.offset_Var, command=self.updateDeviation)
        deviation_scale.grid(row=1,column=1,sticky="ew",padx=5, pady=(0,15))


        angle_box=tk.Canvas(self,
                            width=int(2*(self.controller.app_width/9)),
                            height=int(self.controller.app_height/3),bg="white",bd=2)
        angle_box.grid(row=2, column=0, padx=10, pady=5,sticky="w")
        angle_box.grid_propagate(0)
        angle_box.grid_columnconfigure(0,weight=1)

        angle_heading=tk.Label(angle_box,bg="turquoise3",fg="white",
                                   text="Angle",font=self.controller.heading_font)
        angle_heading.grid(row=0, column=0, sticky="new",
                               padx=2,pady=2)
        
        self.angleScale1=tk.Scale(angle_box,orient="horizontal",bg="white",from_=0,
                           to=1000, troughcolor="gray90",highlightthickness=0)
        self.angleScale1.grid(row=1,column=0,sticky="ew",padx=5, pady=20)
        self.angleScale1.set(1000)

        self.angleScale2=tk.Scale(angle_box,orient="horizontal",bg="white",from_=0,
                              to=1000, troughcolor="gray90",highlightthickness=0)
        self.angleScale2.grid(row=2,column=0,sticky="ew",padx=5)

        led_box=tk.Canvas(self, width=int(3*(self.controller.app_width/9)),bd=2,
                         height=int(2*(self.controller.app_height/6)),bg="white")
        led_box.grid(row=0, column=1, pady=5,sticky="nw",columnspan=2,rowspan=2)
        led_box.grid_propagate(0)

        for ii in range(4):
            led_box.grid_rowconfigure(ii,weight=1)
            if ii <2:
                led_box.grid_columnconfigure(ii,weight=1)

        #  LED Cotrol
        led_heading = tk.Label(led_box,bg="turquoise3",fg="white",text="LED Control",
                             font=self.controller.heading_font)
        led_heading.grid(row=0, column=0, sticky="new",columnspan=2,
                               padx=2,pady=2)

        self.led_button = tk.Button(led_box,text="ON", command = self.writeLED,
                                     image=self.image_LedOn, bg = 'WHITE',
                                     width="68",height="68")
        self.led_button.grid(row=0, column=0,padx=5,pady=5,rowspan=6)
        led_label = tk.Label(led_box, textvariable = self.led_textlabel,
                                     bg = 'WHITE', font = ('Helvetica', 10))
        led_label.grid(row=2, column=1, sticky="new",columnspan=2,
                               padx=2,pady=2)
        

        voltage_box=tk.Canvas(self, width=int((self.controller.app_width/6)+2),
                              height=int(2*(self.controller.app_height/6)+2),
                              bg="white",bd=2)
        voltage_box.grid(row=2, column=1, pady=5,sticky="nw")
        voltage_box.grid_propagate(0)
        for jj in range(2):
            voltage_box.grid_columnconfigure(jj,weight=1)
            voltage_box.grid_rowconfigure(jj,weight=1)

        volt_heading=tk.Label(voltage_box,bg="turquoise3",fg="white",
                              text="Voltage",font=self.controller.heading_font)
        volt_heading.grid(row=0, column=0, sticky="new",columnspan=2,
                             padx=2,pady=2)

        self.voltScale1=tk.Scale(voltage_box,bg="white",from_=12, to=4.5,
                                 resolution=0.1, troughcolor="gray90",
                                 highlightthickness=0, label='L')
        self.voltScale1.grid(row=1,column=0,sticky="ns",pady=5)

        self.voltScale2=tk.Scale(voltage_box,bg="white",from_=12, to=4.5,
                                 resolution=0.1, troughcolor="gray90",
                                 highlightthickness=0, label='H')
        self.voltScale2.grid(row=1,column=1,sticky="ns",pady=5)
        self.voltScale2.set(12)

        temperature_box=tk.Canvas(self, width=int((self.controller.app_width/6)),
                                  height=int(2*(self.controller.app_height/6)),
                                  bg="white",bd=2)
        temperature_box.grid(row=2, column=2, pady=5,sticky="nw")
        temperature_box.grid_propagate(0)
        temperature_box.grid_columnconfigure(0,weight=1)
        
        temperature_heading=tk.Label(temperature_box,bg="turquoise3",fg="white",
                                     font=self.controller.heading_font,
                                     text="Temperature (°F)",)
        temperature_heading.grid(row=0, column=0, sticky="new", padx=2,pady=2)

        self.temp_scale=tk.Scale(temperature_box,bg="white",orient="horizontal",
                                 from_=50, to=100, troughcolor="white",
                                 highlightthickness=0)
        self.temp_scale.grid(row=1,column=0,sticky="nsew",padx=5, pady=20)
        self.temp_scale.set(85)

        read_button = tk.Button(self,text="Read",bg="gray90",
                                command=self.readParameters)
        read_button.grid(row=3, column=0, pady=10)

        write_button = tk.Button(self,text="Write",bg="gray90",
                                 command = self.writeParameters)
        write_button.grid(row=3, column=1, pady=10)

        default_button = tk.Button(self,text="Default",bg="gray90",
                                   command=self.defaultWrite)
        default_button.grid(row=3, column=2, pady=10)

    def id_validate(self, new_value):
        '''
        This function validate the Servo Id
        '''
        try:
            if new_value == '' or new_value == None:
                return True
            if int(new_value) in range(1, 254):
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False

    def deviation_validate(self, new_value):
        '''
        This function will validate the Deviation range
        '''
        try:
            if new_value == '' or  new_value == '-':
                return True
            if int(new_value) in range(-125, 126):
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False


    def updateDeviation(self, value):
        '''
        This function will write the deviation to the motor
        '''
        if robot.alive:
            if self.id_entry.get():
                robot.adjustAngleOffset(self.ID_Var.get()), int(self.offset_Var.get())

    def readParameters(self):
        '''
        This function read all the parameters from servo and display it
        '''
        try:
            if robot.alive:
                response = robot.readID()
                self.ID_Var.set(str(int.from_bytes(response[5], byteorder='little')))
                response = robot.readAngleOffset(self.ID_Var.get())
                offsetValue = int.from_bytes(response[5], byteorder='little')
                if offsetValue > 125:
                    offsetValue = offsetValue - 256
                self.offset_Var.set(offsetValue)

                response = robot.readAngleLimit(self.ID_Var.get())
                self.angleScale1.set(int.from_bytes(response[7] + response[8],
                                                    byteorder='little'))
                self.angleScale2.set(int.from_bytes(response[5] + response[6],
                                                    byteorder='little'))

                response = robot.readVolLimit(self.ID_Var.get())
                self.voltScale1.set(float(int.from_bytes(response[5] + response[6],
                                                    byteorder='little'))/1000)
                self.voltScale2.set(float(int.from_bytes(response[7] + response[8],
                                                    byteorder='little'))/1000)

                response = robot.readTempLimit(self.ID_Var.get())
                self.temp_scale.set(int.from_bytes(response[5], byteorder='little'))

                response = robot.ledRead(self.ID_Var.get())
                if int.from_bytes(response[5], byteorder='little'):
                    self.led_button.config(image = self.image_LedOff,
                                             relief="sunken", text="OFF")
                    self.led_textlabel.set('Press Button to turn On\nServo Led')
                else:
                    self.led_button.config(image = self.image_LedOn, 
                                             relief="sunken", text="ON")
                    self.led_textlabel.set('Press Button to turn Off\nServo Led')
                    
                messagebox.showinfo("Data Read","Read Done Successfully")
            else:
                messagebox.showerror("Comm Error", "Comm Port is not Connected..!!")
        except:
            messagebox.showerror("Read Error", "Data Read Error..!!")

    def writeParameters(self):
        '''
        This function write all the parameters to servo motor
        '''
        if robot.alive:
            if self.id_entry.get():
                robot.writeID(self.ID_Var.get())
                robot.writeAngleLimit(self.ID_Var.get(), self.angleScale2.get(),
                                      self.angleScale1.get())
                robot.writeVolLimit(self.ID_Var.get(), self.voltScale1.get(),
                                    self.voltScale2.get())
                robot.writeTempLimit(self.ID_Var.get(), self.temp_scale.get())
                messagebox.showinfo("Data Write","Write Done Successfully")
            else:
                messagebox.showerror("Servo Id", "Please enter Servo Id..!!")
        else:
            messagebox.showerror("Comm Error", "Comm Port is not Connected..!!")

    def writeLED(self):
        '''
        This function enable and disbale servo motor LED
        Write 0 for LED ON
        Write 1 for LED OFF
        '''
        if robot.alive:
            if self.led_button.cget('text') == 'OFF' and self.id_entry.get():
                self.led_textlabel.set('Press Button to turn Off\nServo Led')
                self.led_button.config(image = self.image_LedOn, 
                                         relief="sunken", text="ON")
                robot.ledWrite(self.ID_Var.get(), 0)
                              
            elif self.led_button.cget('text') == 'ON' and self.id_entry.get():
                self.led_textlabel.set('Press Button to turn On\nServo Led')  
                self.led_button.config(image = self.image_LedOff,
                                            relief="raised", text="OFF")
                robot.ledWrite(self.ID_Var.get(), 1)

            elif self.id_entry.get() == '':
                messagebox.showerror("Servo Id", "Please enter Servo Id..!!")

        else:
            messagebox.showerror("Comm Error", "Comm Port is not Connected..!!")

    def defaultWrite(self):
        '''
        This function set default parameters of servo
        '''
        if robot.alive:
            if self.id_entry.get():
                robot.adjustAngleOffset(self.ID_Var.get())
                messagebox.showinfo("Default Write","Default Done Successfully")
            else:
                messagebox.showerror("Servo Id", "Please enter Servo Id..!!")
        else:
            messagebox.showerror("Comm Error", "Comm Port is not Connected..!!")
        
################################### About Us ###################################
class AboutFrame(tk.Frame):
    '''
    This is a class for Creating widgets for About Us frame
    '''
    def __init__(self,parent,controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self,bg="white",fg="SteelBlue2", text="PiArm",
                         font=('Helvetica', 25))
        label.grid(row=0, column=0,padx=200, pady=30)

        
        text = tk.Label(self,bg="white",fg="black",font=('Helvetica', 11),
                        text="Robotic Arm powered by Raspberry Pi & based on Smart Digital Servo Motors")
        text.grid(row=1, column=0, padx=20)
        text = tk.Label(self,bg="white",fg="black", font=('Helvetica', 11),
                        text="\n1. Miniature Robotic Arm with 6 DOF")
                        
        text.grid(row=2, column=0, padx=(0,260), sticky = 'w')
        text = tk.Label(self,bg="white",fg="black", font=('Helvetica', 11),
                        text="2. Moves around with precise Smart Bus Servo Motors")
                        
        text.grid(row=3, column=0, padx=(0,180), sticky = 'w')
        text = tk.Label(self,bg="white",fg="black", font=('Helvetica', 11),
                        text="3. Upgradable and customizable with various parts and sensors.")
        text.grid(row=4, column=0, padx=(0,95), sticky = 'w')
        text = tk.Label(self,bg="white",fg="black", font=('Helvetica', 11),
                        text="4. All metallic body")
        text.grid(row=5, column=0, padx=(0,270), sticky = 'w')

        
        label = tk.Label(self,bg='white',fg="black", font=('Helvetica', 12),
                         text="For More Info:")
        label.grid(row=6, column=0,pady=(80,10))

        website = tk.Button(self,bg="SteelBlue2",fg="white", font=('Helvetica', 15),
                         text="www.sb-components.co.uk", command=self.mainWebsite)
        website.grid(row=7, column=0)

        shop = tk.Button(self,bg="tomato",fg="white", font=('Helvetica', 15),
                         text="Online Store", command=self.shopWebsite)
        shop.grid(row=8, column=0, padx=(0,130), pady=10)

        github = tk.Button(self,bg="gray60",fg="white", font=('Helvetica', 15),
                         text="Github", command=self.github)
        github.grid(row=8, column=0, padx=(180, 0))

    def mainWebsite(self):
        '''
        Open browser with sb-components website
        '''
        webbrowser.open('https://sb-components.co.uk')

    def shopWebsite(self):
        '''
        Open website with sb-components shop's website
        '''
        webbrowser.open('https://shop.sb-components.co.uk')

    def github(self):
        '''
        open website with github code for PiArm
        '''
        webbrowser.open('https://github.com/sbcshop/PiArm')
    

#######################################################################################################
logo = None
img = None
Root_Dir = path.dirname(path.realpath(__file__))
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    robot = piarm.PiArm()
    app = MainApp()
    app.tk.call('wm', 'iconphoto', app._w, img)
    app.resizable(0,0)
    app.mainloop()      
        
