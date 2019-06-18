#! /usr/bin/python3

'''
This file contains Joystick example code for controlling PiArm
Developed by - SB Components
http://sb-components.co.uk
'''

import re
import pygame
import piarm
from time import sleep

class Joystick_Controller(object):
    """
    Joystick controller class
    """

    def __init__(self):
        self.servo_POS_error = False
        self.joystick_keypress_status = False
        self.step = 50
        self.servo_position = {
                 1: 500,
                 2: 500,
                 3: 500,
                 4: 500,
                 5: 500,
                 6: 500,
            }
        self.button_status = {
                     0: 0,
                     1: 0,
                     2: 0,
                     3: 0,
                     4: 0,
                     5: 0,
                     6: 0,
            }

        #  Initialize Joystick
        pygame.init()
        try:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            print('Joystick initialized')
        except pygame.error as pygame_err:
            print(pygame_err)
        self.read_servo_position()
        print(self.servo_position)


    def listen(self):
        """
        Listen for events to happen
        """
        while True:
            for event in pygame.event.get():
                #  Button Pressed
                if event.type == pygame.JOYBUTTONDOWN:
                    # set Servo to default
                    if event.button == 9:
                        if robot.alive:
                            for ID in range(1, 7):
                                self.servo_position[ID] = 500
                                robot.servoWrite(ID, self.servo_position[ID], 1500)
                        else:
                            print('Comm port is not conected')

                    # keypress
                    elif event.button in range(7):
                        self.button_status[event.button] = 1
                        print('button {} pressed: '.format(event.button),
                                     self.button_status[event.button])        
                    print(self.button_status)

                #  Button Released
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button in range(7):
                        self.button_status[event.button] = 0
                        print('button {} released: '.format(event.button), 
                                     self.button_status[event.button])

                #  If facing buttons are pressed reset button position 
                if self.button_status[0] == self.button_status[2]:
                    self.button_status[0] = 0
                    self.button_status[2] = 0
                if self.button_status[1] == self.button_status[3]:
                    self.button_status[1] = 0
                    self.button_status[3] = 0

            # Change servo position
            for button, status in self.button_status.items():
                if status:
                    #  Move UP
                    if button == 0:
                        if self.servo_position[5] - self.step in range(101, 999):
                            self.servo_position[5] -= self.step
                        if self.servo_position[4] + self.step in range(1, 999):
                            self.servo_position[4] += (self.step + 20)
                        if self.servo_position[3] - self.step in range(52, 970):
                            self.servo_position[3] -= (self.step + 40)

                    #  Move Left
                    elif button == 1:
                        if self.servo_position[6] - self.step in range(10, 980):
                            self.servo_position[6] += self.step
                    
                    #  Move Down
                    elif button == 2:       
                        if self.servo_position[5] + self.step in range(101, 999):
                            self.servo_position[5] += self.step
                        if self.servo_position[4] - self.step in range(1, 999):
                            self.servo_position[4] -= (self.step + 20)
                        if self.servo_position[3] + self.step in range(52, 970):
                            self.servo_position[3] += (self.step + 40)

                    #  Move Right
                    elif button == 3:
                        if self.servo_position[6] + self.step in range(10, 980):
                            self.servo_position[6] -= self.step

                    #  Claw Open
                    elif button == 4:
                        if self.servo_position[1] - self.step in range(144, 710):
                            self.servo_position[1] -= (self.step + 20)

                    #  Claw Close
                    elif button == 5:
                        if self.servo_position[1] + self.step in range(144, 710):
                            self.servo_position[1] += (self.step + 20)
                    self.joystick_keypress_status = True

            #  Write current positions
            if self.joystick_keypress_status:
                if robot.alive:
                    for ID in range(1, 7):
                        robot.servoWrite(ID, self.servo_position[ID], 1000)
                        print("Writing to servo Id {} position: ".format(ID), self.servo_position[ID])
                    self.joystick_keypress_status = False
                else:
                    print('Comm port is not conected')
                sleep(1)
            

    def read_servo_position(self):
        '''
        This funciton read current servo position
        '''
        if robot.alive:
            try:
                #  Read Positions of motors one at a time
                for ID in range(1, 7):
                    response = robot.positionRead(ID)
                    pos = int.from_bytes(response[5]+response[6], byteorder='little')    
                    #  Button Position to variable
                    self.servo_position[ID] = pos
                        
                if self.servo_POS_error:
                    print("Servo Error", "Servo " + str(ID) +
                                     ' - Position Out of Range..!')
                else:
                    print("Motor position Read Done Successfully")
                    
            except TypeError:
                print("Servo Error", "Servo " + str(ID) +
                                     ' - Not Responding')

if __name__ == "__main__":
    robot = piarm.PiArm()
    # write your serial comm
    robot.connect("/dev/ttyS0")
    joystick = Joystick_Controller()
    #  Start Joystick
    try:
        joystick.listen()
    #  Set Motors to Default at KeyboardInterrupt
    except KeyboardInterrupt:
        pass
        for ID in range(1, 7):
            robot.servoWrite(ID, 500, 1500)
        