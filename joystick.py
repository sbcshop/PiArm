#! /usr/bin/python3

'''
This file contains Joystick example code for controlling PiMecha
Developed by - SB Components
http://sb-components.co.uk
'''

import os
import re
import pygame
import piarm
from time import time

path = os.path.dirname(os.path.realpath(__file__))

class Joystick_Controller(object):
    """ Joystick controller class """

    def __init__(self):
        self.servo_POS_error = False
        self.step = 1
        self.joystick_keypress_status = False
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

        pygame.init()
        try:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            print('Joystick initialized')
        except pygame.error as perr:
            print(perr)
        self.read_servo_position()
        print(self.servo_position)


    def listen(self):
        """Listen for events to happen"""
        time_init = time()
        while True:
            for event in pygame.event.get():
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

                elif event.type == pygame.JOYBUTTONUP:
                    if event.button in range(7):
                        self.button_status[event.button] = 0
                        print('button {} released: '.format(event.button), 
                                     self.button_status[event.button])

                    print(self.button_status)


                if self.button_status[0] == self.button_status[2]:
                    self.button_status[0] = 0
                    self.button_status[1] = 0

            # print(self.button_status)
            for button, status in self.button_status.items():
                if status:
                    #  Move UP
                    if button == 0:
                        if self.servo_position[5] - self.step in range(101, 999):
                            self.servo_position[5] -= self.step
                        if self.servo_position[4] + self.step in range(1, 999):
                            self.servo_position[4] += self.step
                        if self.servo_position[3] - self.step in range(52, 970):
                            self.servo_position[3] -= self.step

                    #  Move Left
                    elif button == 1:
                        if self.servo_position[6] - self.step in range(10, 980):
                            self.servo_position[6] -= self.step
                    
                    #  Move Down
                    elif button == 2:       
                        if self.servo_position[5] + self.step in range(101, 999):
                            self.servo_position[5] += self.step
                        if self.servo_position[4] - self.step in range(1, 999):
                            self.servo_position[4] -= self.step
                        if self.servo_position[3] + self.step in range(52, 970):
                            self.servo_position[3] += self.step


                    #  Move Right
                    elif button == 3:
                        if self.servo_position[6] + self.step in range(10, 980):
                            self.servo_position[6] += self.step

                    #  Claw Open
                    elif button == 4:
                        if self.servo_position[1] - self.step in range(144, 710):
                            self.servo_position[1] -= self.step

                    #  Claw Close
                    elif button == 5:
                        if self.servo_position[1] + self.step in range(144, 710):
                            self.servo_position[1] += self.step
                    self.joystick_keypress_status = True
                    # print('servo pos: ', self.servo_position, ' Button: ',button, 
                    #             ' status: ', status)

            #  Write current positions
            if time() - time_init > .1 and self.joystick_keypress_status:
                time_init = time()
                if robot.alive:
                    for ID in range(1, 7):
                        robot.servoWrite(ID, self.servo_position[ID], 100)
                        print("servo {} position: ".format(ID), self.servo_position[ID])
                    self.joystick_keypress_status = False
                else:
                    print('Comm port is not conected')

             # controller.get_button(button)

            

    def read_servo_position(self):
        '''
        This funciton read servo position
        '''
        if robot.alive:
            try:
                for ID in range(1, 7):
                    response = robot.positionRead(ID)
                    pos = int.from_bytes(response[5]+response[6], byteorder='little')    
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
    try:
        joystick.listen()
    except KeyboardInterrupt:
        pass
        for ID in range(1, 7):
            robot.servoWrite(ID, 500, 1500)
        # for ID in range(1, 5):
        #     robot.torqueServo(ID, 0)
        