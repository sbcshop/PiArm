#! /usr/bin/python3

'''
This file contains GUI code for Controlling PiArm
Developed by - SB Components
http://sb-components.co.uk
'''

import piarm
import logging
import os
import threading
import shutil
import subprocess
import time
import re
import picamera
from tkinter import font
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog


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
        self.groupSelected = None
        self.loopVar = tk.IntVar()
        self.checkIDVar = []
        self.posEntry = []
        self.timeEntry = []
        self.modify_data = []
        self.servo_POS_error = False
        
        self.geometry("%dx%d+%d+%d" %(self.app_width,self.app_height,self.xpos,
                                      self.ypos))
        self.title("PiArm Controller")
        if not self.screen_width > self.app_width:
            self.attributes('-fullscreen', True)
            
        self.config(bg="gray85")

        self.container = tk.Frame(self,height=480, width=800)
        self.container.pack(fill = 'both', expand = True)

        self.camFrame = tk.Frame(self,height=480, width=800, bg='black')
        
        self.left_frame=tk.Frame(self.container,width=int(self.app_width/4),
                                 bg="gray85")
        self.left_frame.pack(side="left", fill="both")
        self.left_frame.pack_propagate(0)

        self.mid_frame=tk.Frame(self.container,width=5,bg="gray50")
        self.mid_frame.pack(side="left", fill="both")

        self.right_frame=tk.Frame(self.container,bg="gray85")
        self.right_frame.pack(side="left",fill="both",expand=True)
        
        logo = tk.PhotoImage(file = Root_Dir + '/Images/sblogo.png')
        img = tk.PhotoImage(file = Root_Dir + '/Images/piarm.png')
        self.camIcon = tk.PhotoImage(file = Root_Dir + '/Images/camera.png')
        self.vidIcon = tk.PhotoImage(file = Root_Dir + '/Images/video.png')
        self.clickIcon = tk.PhotoImage(file = Root_Dir + '/Images/click.png')
        self.homeIcon = tk.PhotoImage(file = Root_Dir + '/Images/home.png')
        self.backIcon = tk.PhotoImage(file = Root_Dir + '/Images/back.png')

        self.protocol("WM_DELETE_WINDOW", self.close_Robot)
        
        self.leftFrame_Contents()
        self.rightFrame_Contents()

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

    def leftFrame_Contents(self):
        '''
        This function creates the left frame widgets
        '''
        serial_box=tk.Canvas(self.left_frame,width=160,
                             height=110)
        serial_box.grid(row=0, column=0)
        serial_box.grid_propagate(False)
        
        ''' Serial Canvas '''
        for i in range (4):
            serial_box.grid_rowconfigure(i,weight=1)
            if i < 2:
                serial_box.grid_columnconfigure(i,weight=1)
        
        serial_heading=tk.Label(serial_box,bg="gray50",fg="white",
                                text="SERIAL")
        serial_heading.grid(row=0, column=0,columnspan=2, sticky="new")

        com_label = tk.Label(serial_box, fg="Black",text="Port")
        com_label.grid(row=1, column=0)

        self.com_entry = tk.Entry(serial_box,width=10)
        self.com_entry.grid(row=1, column=1)
        if self.port:
            self.com_entry.insert(0, self.port)

        baud_label = tk.Label(serial_box, fg="Black",text="Baudrate")
        baud_label.grid(row=2, column=0)

        baud_entry = tk.Entry(serial_box,width=10)
        baud_entry.insert("end", "115200")
        baud_entry.grid(row=2, column=1)
        baud_entry.config(state="readonly")

        self.circle=tk.Canvas(serial_box,height=40, width=40,bg="gray85",bd=0)
        self.indication = self.circle.create_oval(10,10,30,30, fill="red")
        self.circle.grid(row=3, column=0)

        self.connect_button = tk.Button(serial_box,text="Open",bg="gray80", bd=2,
                                        borderwidth=2,command = self.connectPort)
        self.connect_button.grid(row=3, column=1)

        ''' Record Canvas '''
        record_box=tk.Canvas(self.left_frame,width=160, height=120)
        record_box.grid(row=1, column=0)
        record_box.grid_propagate(False)

        for i in range (4):
            record_box.grid_rowconfigure(i,weight=1)
            if i < 2:
                record_box.grid_columnconfigure(i,weight=1)
        
        record_heading=tk.Label(record_box,bg="gray50",fg="white",
                                text="RECORD")
        record_heading.grid(row=0, column=0, columnspan=2, sticky="new")

        readButton = tk.Button(record_box,text="Read",bg='gray80',borderwidth=2,
                               command=self.read_ServoPos, bd=2)
        readButton.grid(row=0, column=0, pady=(22,0))

        writeButton = tk.Button(record_box,text="Write",bg='gray80',borderwidth=2,
                                command = self.write_ServoPos, bd=2)
        writeButton.grid(row=0, column=1, pady=(22,0))
        
        defaultButton = tk.Button(record_box,text=" Default_Position  ",bg='gray80',
                                  borderwidth=2, command=self.default_Pos, bd=2)
        defaultButton.grid(row=1, column=0,columnspan=2)
        
        self.torqueButton = tk.Button(record_box,text="All_Torque_Enable",
                                      bg='gray80',command=self.allTorque_Enable,
                                      bd=2, borderwidth=2)
        self.torqueButton.grid(row=2, column=0, columnspan=2)

        ''' Group Canvas '''
        group_box=tk.Canvas(self.left_frame,width=160, height=90)
        group_box.grid(row=2, column=0)
        group_box.grid_propagate(False)

        for i in range (4):
            group_box.grid_rowconfigure(i,weight=1)
            if i < 2:
                group_box.grid_columnconfigure(i,weight=1)

        group_Label=tk.Label(group_box,bg="gray50",fg="white",
                                text="GROUP")
        group_Label.grid(row=0, column=0, columnspan=2, sticky="new")

        addGroup_Button = tk.Button(group_box,text=" Add  ",bg='gray80', bd=2,
                                    command = self.add_Group, borderwidth=2)
        addGroup_Button.grid(row=0, column=0, pady=(22,0))

        delGroup_Button = tk.Button(group_box,text="Delete",bg='gray80',bd=2,
                                    command=self.deleteGroup, borderwidth=2)
        delGroup_Button.grid(row=0, column=1, pady=(22,0))
        
        importButton = tk.Button(group_box,text="Import",bg='gray80', bd=2,
                                 command=self.importGroup, borderwidth=2)
        importButton.grid(row=1, column=0)
        
        exportButton = tk.Button(group_box,text="Export",bg='gray80',bd=2,
                                 command=self.exportGroup, borderwidth=2)
        exportButton.grid(row=1, column=1)

        ''' Command Canvas '''
        cmd_box=tk.Canvas(self.left_frame,width=160, height=140)
        cmd_box.grid(row=3, column=0)
        cmd_box.grid_propagate(False)

        for i in range (4):
            cmd_box.grid_rowconfigure(i,weight=1)
            if i < 2:
                cmd_box.grid_columnconfigure(i,weight=1)

        record_heading=tk.Label(cmd_box,bg="gray50",fg="white",
                                text="COMMAND")
        record_heading.grid(row=0, column=0, columnspan=2, sticky="new")

        timeLabel=tk.Label(cmd_box, text="Time (ms)")
        timeLabel.grid(row=0, column=0, pady=(22,0))

        delay_vcmd = (self.register(self.delay_validate),'%P')
        self.delayEntry = tk.Entry(cmd_box,validate='key',width=5, bd='1',
                                   validatecommand=delay_vcmd)
        self.delayEntry.grid(row=0, column=1, pady=(22,0))
        self.delayEntry.insert('end', 1000)

        addCmd_Button = tk.Button(cmd_box,text=" Add  ",bg='gray80',borderwidth=2,
                                  command=self.add_Command, bd=2)
        addCmd_Button.grid(row=1, column=0)

        delCmd_Button = tk.Button(cmd_box,text="Delete",bg='gray80',borderwidth=2,
                                  command=self.del_Command, bd=2)
        delCmd_Button.grid(row=1, column=1)
        
        insertButton = tk.Button(cmd_box,text="Insert",bg='gray80', borderwidth=2,
                                 command=self.insert_Command, bd=2 )
        insertButton.grid(row=2, column=0)
        
        modifyButton = tk.Button(cmd_box,text="Modify",bg='gray80', borderwidth=2,
                                 command=self.modify_Command, bd=2)
        modifyButton.grid(row=2, column=1)
        
        loopButton = tk.Checkbutton(cmd_box, text='Loop',variable = self.loopVar,
                                    onvalue=1, offvalue=0)
        loopButton.grid(row=3, column=0)

        self.playButton = tk.Button(cmd_box,text="Play",font=('Helvetica', 12),
                                    command=self.cmdPlay,bg='SteelBlue2', bd=2,
                                    borderwidth=2)
        self.playButton.grid(row=3, column=1)


    def connectPort(self):
        '''
        This function connects the serial port
        '''
        if self.connect_button.cget('text') == 'Open' and self.com_entry.get():
            robot.connect("/dev/"+self.com_entry.get())
            if robot.alive:
                self.connect_button.config(relief="sunken", text="Close")
                self.circle.itemconfigure(self.indication, fill="green3")
                self.com_entry.config(state="readonly")
            
        elif self.connect_button.cget('text') == 'Close':
            self.connect_button.config(relief="raised", text="Open")
            self.circle.itemconfigure(self.indication, fill="red")
            robot.disconnect()
            self.com_entry.config(state="normal")
        else:
            messagebox.showerror("Port Error", "Enter Comm Port..!!")
            self.com_entry.config(state="normal")

    def read_ServoPos(self):
        '''
        This funciton read servo position
        '''
        if robot.alive:
            try:
                for ID in range(1, 7):
                    response = robot.positionRead(ID)
                    pos = int.from_bytes(response[5]+response[6], byteorder='little')
                    if pos > MAX_VALUE:
                        self.servo_POS_error = True
                        break
                    else:
                        self.posEntry[ID-1].delete(0,'end')
                        self.posEntry[ID-1].insert(0, pos)
                        
                if self.servo_POS_error:
                    messagebox.showerror("Servo Error", "Servo " + str(ID) +
                                     ' - Position Out of Range..!')
                    self.servo_POS_error = False
                else:
                    messagebox.showinfo("Data Read","Read Done Successfully")
                    
            except TypeError:
                messagebox.showerror("Servo Error", "Servo " + str(ID) +
                                     ' - Not Responding')
        else:
            messagebox.showerror("Comm Error", 'Comm Port is not Connected !!')
            
            
    def write_ServoPos(self):
        '''
        This funciton write servo position
        '''
        try:
            if robot.alive:
                for ID in range(1, 7):
                    robot.servoWrite(ID,int(self.posEntry[ID-1].get()),
                                     int(self.timeEntry[ID-1].get()))
                    self.checkIDVar[ID-1].set(1)
                self.torqueButton.config(relief="sunken", text="All_Torque_Disable")
                messagebox.showinfo("Data Write","Write Done Successfully")
            else:
                messagebox.showerror("Comm Error", 'Comm Port is not Connected !!')

        except ValueError:
            messagebox.showerror("Value Error", 'Entry value cannot be empty..!! !!')
            
    def default_Pos(self):
        '''
        This funciton set each servo to default position
        '''
        if robot.alive:
            DEFAULT = [500, 500, 500, 500, 500, 500]
            
            for ID in range(1, 7):
                robot.servoWrite(ID, int(DEFAULT[ID -1]), 500)
                self.posEntry[ID-1].delete(0,'end')
                self.posEntry[ID-1].insert(0, DEFAULT[ID-1])
                self.checkIDVar[ID-1].set(1)
            self.torqueButton.config(relief="sunken", text="All_Torque_Disable")
            messagebox.showinfo("Default","Write Done Successfully")
        else:
            messagebox.showerror("Comm Error", 'Comm Port is not Connected !!')

    def allTorque_Enable(self):
        '''
        This function enable all servo torque
        '''
        if robot.alive:
            if self.torqueButton.cget('text') == 'All_Torque_Enable':
                self.torqueButton.config(relief="sunken", text="All_Torque_Disable")
                for ID in range(1, 7):
                    robot.torqueServo(ID, 1)
                    self.checkIDVar[ID-1].set(1)
                
            elif self.torqueButton.cget('text') == 'All_Torque_Disable':
                self.torqueButton.config(relief="raised", text="All_Torque_Enable")
                for ID in range(1, 7):
                    robot.torqueServo(ID, 0)
                    self.checkIDVar[ID-1].set(0)
        else:
            messagebox.showerror("Comm Error", 'Comm Port is not Connected !!')
            
    def tick_EnTorque(self, index):
        '''
        This funciton enable selected servo torque 
        '''
        if robot.alive:
            robot.torqueServo(index + 1, self.checkIDVar[index].get())
        else:
            messagebox.showerror("Comm Error", 'Comm Port is not Connected !!')

    def add_Group(self):
        '''
        This funciton add a group name
        '''
        groupName = simpledialog.askstring('Group Name', 'Enter a name')
        if groupName:
            for entry in self.groupBox.get('0', 'end'):
                if entry == groupName:
                    tk.messagebox.showerror('Name Error','Group Name Already Exits..!!')
                    return 0

            self.groupBox.insert('end', groupName)
            if len(self.groupBox.get('0', 'end')) == 1:
                self.groupBox.select_set(0)
                self.groupBox.activate(0)
                self.groupSelected = groupName
            with open(Root_Dir+"/.Temp/"+groupName + ".txt", "w") as file:
                self.log.info(groupName + ' temperary file created')

    def deleteGroup(self):
        '''
        This funciton deleter selected group name
        '''
        if self.groupBox.size():
            index = self.groupBox.index('active')
            self.groupBox.delete(index)
            os.remove(Root_Dir +'/.Temp/'+self.groupSelected+'.txt')
            self.commandBox.delete(0, 'end')
            size = self.groupBox.size()
            if size:
                self.groupSelected = self.groupBox.get('0')
                self.groupBox.select_set(0)
                self.groupBox.activate(0)
                file = open(Root_Dir+'/.Temp/'+ self.groupSelected +'.txt', 'r')
                for line in file:
                    stripLine = line.strip()
                    self.commandBox.insert(0,stripLine)
            if size == 0:
                self.groupSelected = None
        else:
            tk.messagebox.showerror('Group Error','Group Name Not Selected..!!')

    def add_Command(self):
        '''
        This funciton add servo read values (i.e. command) to selected group
        '''
        if self.groupSelected:
            cmdList = []
            for ID in range(0, 6):
                cmd = ("ID:" + str(ID+1) +' P' + (self.posEntry[ID].get()) + ",T" + (self.timeEntry[ID].get())+'  ')
                cmdList.append(cmd)
            if str(self.delayEntry.get()) == '':
                cmdList.append('Time:' + '1000')
            else:
                cmdList.append('Time:' + str(self.delayEntry.get()))
            self.commandBox.insert('end',''.join(cmdList))

            with open(Root_Dir+'/.Temp/' + self.groupSelected +'.txt', 'a') as file:
                file.write(''.join(cmdList)+'\n')
        else:
            tk.messagebox.showerror('Group Error','Group Name Not Selected..!!')

    def del_Command(self):
        '''
        This funciton delete selected command
        '''
        item = self.commandBox.curselection()
        if item and self.groupSelected:
            self.commandBox.delete(item)
            cmd_List = self.commandBox.get(0, 'end')
            with open(Root_Dir +"/.Temp/"+self.groupSelected+'.txt', 'w') as file:
                for value in cmd_List:
                    file.write(value + '\n')
        else:
            tk.messagebox.showerror('Command Error','Command Not Selected..!!')

    def insert_Command(self):
        '''
        This funciton insert command above the selected command
        '''
        item = self.commandBox.curselection()
        if item and self.groupSelected:
            cmdList = []
            for ID in range(0, 6):
                cmd = ("ID:" + str(ID+1) +' P' + (self.posEntry[ID].get()) + ",T" + (self.timeEntry[ID].get())+'  ')
                cmdList.append(cmd)
            if str(self.delayEntry.get()) == '':
                cmdList.append('Time:' + '1000')
            else:
                cmdList.append('Time:' + str(self.delayEntry.get()))

            position = self.commandBox.curselection()
            self.commandBox.insert(position,''.join(cmdList))
            cmd_List = self.commandBox.get(0, 'end')
            with open(Root_Dir+"/.Temp/"+self.groupSelected+'.txt', 'w') as file:
                for value in cmd_List:
                    file.write(value + '\n')

        else:
            tk.messagebox.showerror('Command Error','Command Not Selected..!!')
        
        
    def modify_Command(self):
        '''
        This funciton modify the selected command
        '''
        item = self.commandBox.curselection()
        if item and self.groupSelected:
            self.top_Level = tk.Toplevel()

            windowWidth = self.top_Level.winfo_reqwidth()
            windowHeight = self.top_Level.winfo_reqheight()
            # Gets both half the screen width/height and window width/height
            positionRight = int(self.top_Level.winfo_screenwidth()/2 - windowWidth/2)
            positionDown = int(self.top_Level.winfo_screenheight()/2- windowHeight/2)
     
            # Positions the window in the center of the page.
            self.top_Level.geometry("+{}+{}".format(positionRight, positionDown))
            
            self.top_Level.title('Modify')
            self.top_Level.resizable(False, False)
            
            self.modify_data = []
            index = self.commandBox.curselection()

            tk.Label(self.top_Level, text="ID").grid(row=0, column=0)
            tk.Label(self.top_Level, text="Position").grid(row=0, column=1)
            tk.Label(self.top_Level, text="Speed").grid(row=0, column=2)

            rawData = self.commandBox.get(index)
            rawData = rawData.split('  ')
            for index in range(0,6):
                cmd_Data = re.findall('\d+', rawData[index])
                self.modify_data.append([0,0,0])
                self.modify_data[index][0]= tk.Entry(self.top_Level, width=6)
                self.modify_data[index][0].insert(0,index+1)
                self.modify_data[index][0].grid(row=index+1,column=0)
                self.modify_data[index][0].config(state='readonly')

                self.modify_data[index][1]= tk.Entry(self.top_Level, width=12)
                self.modify_data[index][1].insert(0,cmd_Data[1])
                self.modify_data[index][1].grid(row=index+1,column=1)
                    
                self.modify_data[index][2]= tk.Entry(self.top_Level, width=12)
                self.modify_data[index][2].insert(0,cmd_Data[2])
                self.modify_data[index][2].grid(row=index+1,column=2)
            tk.Button(self.top_Level, text='Save', command=self.modify_Save).grid(row = 7, column = 1, pady = 10, stick = 'W')
            tk.Button(self.top_Level, text='Cancel', command=self.top_Level.destroy).grid(row = 7, column = 2, pady = 10, stick = 'W')

        else:
            tk.messagebox.showerror('Command Error','Command Not Selected..!!')

    def modify_Save(self):
        '''
        This funciton save the modified command to command box
        '''
        cmdList = []
    
        for index in range(0,6):
            if (self.modify_data[index][1].get()) and (self.modify_data[index][2].get()):
                cmd = "ID:" + str(index+1) +' P' + self.modify_data[index][1].get() + ",T" + self.modify_data[index][2].get() +'  '
                cmdList.append(cmd)
            else:
                tk.messagebox.showerror('Error','Fields cannot be empty')
                break
        if cmdList:
            if str(self.delayEntry.get()) == '0':
                cmdList.append('Time:' + '1000')
            else:
                cmdList.append('Time:' + str(self.delayEntry.get()))
            value = self.commandBox.curselection()[0]
            self.commandBox.delete(value)
            self.commandBox.insert(value,''.join(cmdList))
            self.commandBox.select_set(value)
            self.commandBox.activate(value)
        self.top_Level.destroy()

    def cmdPlay(self):
        '''
        This funciton creates a thread to play the commands of the
        selected group
        '''
        #if robot.alive:
        if self.playButton.cget('text') == 'Play' and self.commandBox.size():
            self.playButton.config(relief="sunken", text="Stop")
            self.playFlag = True
            self.threadContRead = threading.Thread(target=self._continousPlay)
            self.threadContRead.daemon = True
            self.threadContRead.start()
                                        
        elif self.playButton.cget('text') == 'Stop':
            self.playButton.config(relief="raised", text="Play")
            self.playFlag = False
        else:
            messagebox.showerror("Data Error", "No command to play..!!")

    def _continousPlay(self):
        '''
        This thread play the coomands of the selected group
        '''
        self.torqueButton.config(relief="sunken", text="All_Torque_Disable")
        size = self.commandBox.size()

        while self.playFlag:
            for index in range(0, size):
                self.commandBox.select_set(index)
                rawData = self.commandBox.get(index)
                rawData = rawData.split('  ')
                delay = rawData[-1].split(':')
                delay = int(delay[1])/1000
                if robot.alive:
                    for value in range(0, 6):
                        cmd_Data = re.findall('\d+', rawData[value])
                        robot.servoWrite(int(cmd_Data[0]), int(cmd_Data[1]), int(cmd_Data[2]))
                        self.checkIDVar[value].set(1)
                else:
                    messagebox.showerror("Comm Error", 'Comm Port is not Connected !!')     
                time.sleep(delay)
                self.commandBox.select_clear(index)

                if not self.playFlag:
                    break

            if not self.loopVar.get():    
                self.playButton.config(relief="raised", text="Play")
                self.playFlag = False
                
    def importGroup(self):
        '''
        This funciton import the group and its commands
        '''
        file_path = filedialog.askopenfilename(initialdir = Root_Dir)
        line_index = 0
        if file_path:
            file_name = file_path.split('/')
            group_Name = file_name[-1].split('.')
            for name in self.groupBox.get(0, 'end'):
                if group_Name[0] == name:
                    tk.messagebox.showerror('Group Error','Group Name already exists..!!')
                    return False
                
            file = open(file_path, 'r')
            shutil.copy2(file_path, Root_Dir + '/.Temp/' + group_Name[0] + '.txt' )
            self.groupBox.insert('end', group_Name[0])
            if self.groupBox.size() == 1:
                self.groupBox.select_set(0)
                self.groupBox.activate(0)
                self.groupSelected = group_Name[0]
                for line in file:
                    stripLine = line.strip()
                    self.commandBox.insert(line_index,stripLine)
                    line_index = line_index + 1
        

    def exportGroup(self):
        '''
        This funciton exports the group in .txt format
        '''
        if self.groupBox.size():
            with open(Root_Dir + '/Export Files/'+ self.groupSelected +'.txt', 'w') as file:
                size = self.commandBox.size()
                if size:
                    for index in range(0, size):
                        cmdValue = self.commandBox.get(index)
                        file.write(''.join(cmdValue)+'\n')
                    tk.messagebox.showinfo('Export',self.groupSelected+'.txt'+'- Exported')
                else:
                    tk.messagebox.showerror('Export Error','Cannot export file empty file..!!')
        else:
            tk.messagebox.showerror('Export Error','Group Name Not Selected..!!')
        
    
    def rightFrame_Contents(self):
        '''
        This function creates right frame contents
        '''
        LINE = [
            (130,  70, 180, 70, 'SteelBlue2', 30),  (110,  20, 110, 100,  'gray30', 50),
            (180,  70, 260, 70, 'gray30', 50),      (260,  70, 310,  70, 'SteelBlue2', 30),
            (310,  70, 390, 70, 'gray30', 50),      (350,  150, 350, 95, 'SteelBlue2', 30),
            (280, 255, 370, 155, 'SteelBlue2', 30), (310, 170, 390, 170, 'gray30', 50),
            (250, 260, 330, 260, 'gray30', 50),     (220, 285, 420, 285, 'SteelBlue2', 5),
            (240, 293, 400, 293, 'gray65', 10),     (240, 300, 240, 350,  'gold', 8),
            (400, 300, 400, 350, 'gold', 8),        (220, 300, 420, 300, 'SteelBlue2', 5),
            (280, 325, 360, 325, 'gray30', 47)]

        ID_LABEL = [(95, 20), (190, 50), (320, 50), (320, 150), (260, 240), (290, 305)]

        C_BUTTON = [(95, 35), (230, 50), (360, 50),(360, 150), (300, 240), (330, 305)]

        POS_VAL = [(500, 90, 55), (500, 184, 72), (500, 314, 72), (500, 314, 172),
                    (500, 254, 262), (500, 284, 327)]

        TIME_VAL = [(95, 78), (227, 72), (357, 72), (357, 172), (297, 262), (327, 327)]
            
        
        self.bodyCanvas=tk.Canvas(self.right_frame,width=480,height=350,bg="white")
        self.bodyCanvas.grid(row=0, column=0)
        self.bodyCanvas.grid_propagate(0)

        self.bodyCanvas.create_polygon(90,20,30,20, 30,30, 90, 60, 90,100,30,100, 30,90, 90, 60, fill='gray30')
        

        pos_vcmd = (self.register(self.pos_validate),'%s','%S','%P', '%V')
        time_vcmd = (self.register(self.time_validate),'%P')

        for index in range(15):
             self.bodyCanvas.create_line(LINE[index][0], LINE[index][1], LINE[index][2],
                                         LINE[index][3], fill=LINE[index][4],
                                         width=LINE[index][5])
        for index in range(6):
            var = tk.IntVar()
            
            label = tk.Label(self.bodyCanvas, text='ID-'+ str(index+1), bg='gray30',
                             fg='white')
            label.place(x=ID_LABEL[index][0], y=ID_LABEL[index][1])

            checkBut = tk.Checkbutton(self.bodyCanvas,bg='gray30',variable=var,
                                      command= lambda index=index: self.tick_EnTorque(index))
            checkBut.place(x=C_BUTTON[index][0],y=C_BUTTON[index][1])
            self.checkIDVar.append(var)

            entry = tk.Entry(self.bodyCanvas,validate='key', bg='SlateGray1',
                             validatecommand = pos_vcmd, width=4, bd='1')
            entry.place(x=POS_VAL[index][1], y=POS_VAL[index][2])
            entry.insert('end', POS_VAL[index][0])
            self.posEntry.append(entry)

            entry = tk.Entry(self.bodyCanvas, validate='key',
                                 validatecommand = time_vcmd, width=3, bd='1')
            entry.place(x=TIME_VAL[index][0], y=TIME_VAL[index][1])
            entry.insert('end', 500)
            self.timeEntry.append(entry)

        logoButton = tk.Button(self.bodyCanvas, image=logo, height = 40, width = 130,
                               bg='white', bd=0, highlightthickness=0, fg='white', 
                               state='disabled')
        logoButton.place(x=10, y=300)

        self.camButton = tk.Button(self.bodyCanvas,text='Camera',command = self.camera,bg='gray80',highlightthickness=0)
        self.camButton.place(x=320, y=5)

        self.closeButton = tk.Button(self.bodyCanvas,text='Close',command=self.close_Robot,
                                     bg='gray80',highlightthickness=0)
        self.closeButton.place(x=410, y=5)

        # Group Name
        tk.Label(self.right_frame,text="GROUP NAME",fg='white',bg="gray50",padx=36).place(x=481,y=0)
        self.groupBox = tk.Listbox(self.right_frame, exportselection=0,height=22, width = 19)
        self.groupBox.place(x=480,y=18)
        self.groupBox.select_set(0)
        self.groupBox.activate(0)
        ygscrollbar = tk.Scrollbar(self.right_frame)
        ygscrollbar.place(x=620, y=21, relheight = 0.69)
        self.groupBox.config(yscrollcommand=ygscrollbar.set)
        ygscrollbar.config(command=self.groupBox.yview)
        self.groupBox.bind("<<ListboxSelect>>",self.groupBindData )

        # Command
        frame = tk.Frame(self.right_frame,height=15, width=632, bg="gray50")
        frame.place(x=0,y=350)
        tk.Label(self.right_frame,text="COMMAND",fg="white",bg="gray50",pady=0).place(x=270,y=350)

        self.commandBox = tk.Listbox(self.right_frame,exportselection=0,height=7,width=77)
        self.commandBox.place(x=0,y=364)
        xscrollbar = tk.Scrollbar(self.right_frame, orient = 'horizontal')
        xscrollbar.place(x=0, y=468, relwidth = 1)
        yscrollbar = tk.Scrollbar(self.right_frame)
        yscrollbar.place(x=620, y=367, relheight = 0.21)

        self.commandBox.config(xscrollcommand=xscrollbar.set)
        self.commandBox.config(yscrollcommand=yscrollbar.set)
        xscrollbar.config(command=self.commandBox.xview)
        yscrollbar.config(command=self.commandBox.yview)
        self.commandBox.bind("<Double-Button-1>", self.onclickPlay)

    def delay_validate(self, new_value):
        '''
        This funciton validate delay entry value
        '''
        try:
            if str(new_value) == '':
                return True 
            elif int(new_value) >= 0 and int(new_value) <= 3000:
                return True
            else:
                self.bell()
                return False
        except ValueError:
            self.bell()
            return False

    def pos_validate(self, textBefore, textInserted, entryValue, focus):
        '''
        This funciton validate position entry values
        '''
        try:
            if entryValue:
                if int(entryValue) >= 0 and int(entryValue) <= 999:
                    return True
                else:
                    self.bell()
                    return False
            else:
                return True

        except ValueError:
            self.bell()
            return False
        

    def time_validate(self, new_value):
        '''
        This funciton validates time entry values
        '''
        try:
            if new_value:
                if int(new_value) >= 0 and int(new_value) <= 999:
                    return True
                else:
                    self.bell()
                    return False
            else:
                return True
        except ValueError:
            self.bell()
            return False

    def groupBindData(self,event):
        '''
        This funciton bind data of the group box
        '''
        curSelection = self.groupBox.curselection()
        if curSelection:
            selectedGroup = self.groupBox.get(curSelection)
            if self.groupSelected != selectedGroup:
                self.commandBox.delete(0, 'end')
                self.groupSelected = selectedGroup
            
                file = open(Root_Dir+'/.Temp/'+ self.groupSelected +'.txt', 'r')
                for line in file:
                    stripLine = line.strip()
                    self.commandBox.insert(0,stripLine)

    def onclickPlay(self, event):
        '''
        This funciton handle double click play of command
        '''
        index = self.commandBox.curselection()
        if index:
            rawData = self.commandBox.get(index)
            rawData = rawData.split('  ')
            delay = rawData[-1].split(':')
            delay = int(delay[1])/1000
            if robot.alive:    
                for value in range(0, 17):
                    cmd_Data = re.findall('\d+', rawData[value])
                    robot.servoWrite(int(cmd_Data[0]), int(cmd_Data[1]), int(cmd_Data[2]))
                    self.checkIDVar[value].set(1)
            else:
                messagebox.showerror("Comm Error", 'Comm Port is not Connected !!')

    def camera(self):
        '''
        This funciton creates camera frame and forget GUI
        '''
        self.container.pack_forget()
        self.camFrame.pack(fill = 'both', expand = True)

        self.Fl_VideoRecord = False

        camButton = tk.Button(self.camFrame,text="Photo",font=("Helvetica",16),compound="top",
                              bd = 0,bg = "black", fg = "white",highlightbackground = "black",
                              activebackground = "black",activeforeground = "white",
                              image=self.camIcon,command = lambda: self.startPreview("Picture"),
                              highlightthickness=0)
        camButton.place(x=140, y=100)

        vidButton = tk.Button(self.camFrame,text="Video",font=("Helvetica",16),compound="top",
                              bd = 0,bg = "black", fg = "white",highlightbackground = "black",
                              activebackground = "black",activeforeground = "white",
                              image=self.vidIcon,command = lambda: self.startPreview("Video"),
                              highlightthickness=0)
        vidButton.place(x=450, y=100)

        self.camhome = tk.Button(self.camFrame,image=self.homeIcon, bg = "black", fg = "black", bd = 0,
                              highlightbackground = "black",text='Home',
                              activebackground = "black",command=self.forgetCam,
                              activeforeground = "black")
        self.camhome.place(x=730,y=40)

        self.back = tk.Button(self.camFrame,text = "Home", bg = "black", fg = "black",
                              bd = 0, image = self.backIcon,
                              highlightbackground = "black",
                              activebackground = "black",
                              activeforeground = "black",state="disable",
                              command = self.camBack)
        self.back.place(x=730,y=280)

        self.click = tk.Button(self.camFrame, image=self.clickIcon,bg = "black", fg = "black",
                               bd = 0,font=("bold",12), command=self.camClick,
                               highlightbackground="black",
                               activebackground = "black",
                               activeforeground="black",compound="center",
                               state="disable")
        self.click.place(x=725,y=160)

    def startPreview(self, arg):
        ''' 
        Start Preview of Camera
        '''
        self.cameraMode = arg
        label = tk.Label(self.camFrame, text="",font=("helvetica", 15), bg='black')
        label.place(x=250, y=350)

        response = subprocess.check_output(["sudo","vcgencmd","get_camera"])

        if(response == b'supported=1 detected=1\n'):
            self.camera = picamera.PiCamera()
            self.back.config(state="normal")
            self.click.config(state="normal")

            if arg == "Picture":
                self.click.config(text="Photo")
            else:
                self.click.config(text="Video")

            self.camera.preview_fullscreen=False
            self.camera.preview_window=(400, 240, 730, 480)
            self.camera.resolution=(800,480)
            self.camera.start_preview()
            self.camhome.config(state="disable")

        elif(response == b'supported=0 detected=0\n'):
            label.config(text="Error: Camera is not enabled", bg="yellow")
            label.after(4000, label.place_forget)
        else:
            label.config(text="Error: Camera is not connected properly",
                         bg="yellow")
            label.after(4000, label.place_forget)

    def camClick(self):
        '''
        Click Photos and Videos
        '''
        if(self.cameraMode == "Picture"):
            self.camera.capture(Root_Dir + '/Gallery/Photos/' + 'img_' +
                                time.strftime('%d%m%Y_')+time.strftime('%H%M%S')
                                + '.jpg')
        elif (self.cameraMode == "Video") and self.Fl_VideoRecord == False:
            self.click.config(text="Record", fg="red")
            self.back.config(state="disable")
            self.Fl_VideoRecord = True
            self.camera.start_recording(Root_Dir + '/Gallery/Videos/' + 'vid_' +
                                        time.strftime('%d%m%Y_')+
                                        time.strftime('%H%M%S') + '.h264')
        elif self.Fl_VideoRecord == True:
            self.Fl_VideoRecord = False
            self.cameraMode = None
            self.camera.stop_recording()
            self.camera.stop_preview()
            self.camera.close()
            self.click.config(text="",fg="black")
            self.back.config(state="disable")
            self.click.config(state="disable")
            self.camhome.config(state="normal")
        
        
    def camBack(self):
        '''
        This funciton goes back to camera home frame
        '''
        self.camera.stop_preview()
        self.camera.close()
        self.click.config(text="",fg="black")
        self.back.config(state="disable")
        self.click.config(state="disable")
        self.camhome.config(state="normal")

        
    def forgetCam(self):
        '''
        This funciton close the camera frame and open the GUI
        '''
        self.camFrame.pack_forget()
        self.container.pack(fill = 'both', expand = True)
        

#######################################################################################################        
robot = None
logo = None
img = None
MAX_VALUE = 1023

Root_Dir = os.path.dirname(os.path.realpath(__file__))

if os.path.exists(Root_Dir + '/.Temp'):
    shutil.rmtree(Root_Dir + '/.Temp')
os.mkdir(Root_Dir + '/.Temp')

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    robot = piarm.PiArm()
    app = MainApp()
    app.tk.call('wm', 'iconphoto', app._w, img)
    app.resizable(0,0)
    app.mainloop()
