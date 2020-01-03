import RPi.GPIO as GPIO
from time import time, sleep

from piarm import PiArm

class ultrasonic:
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BOARD)

    #  set GPIO Pin
    Trigger_Pin = 31
    Echo_Pin = 29

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        #  Pin Configuration
        GPIO.setup(self.Trigger_Pin, GPIO.OUT)
        GPIO.setup(self.Echo_Pin, GPIO.IN)


    def distance_check(self):
        '''
        Check distance from the pulse duration
        '''
        self.trigger()

        StartTime = time()
        StopTime = time()

        # save StartTime
        while GPIO.input(self.Echo_Pin) == 0:
            StartTime = time()

        # save time of arrival
        while GPIO.input(self.Echo_Pin) == 1:
            StopTime = time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime

        # multiply with the sonic speed (34300 cm/s) and divide by 2
        distance = (TimeElapsed * 34300) / 2

        return distance

    def trigger(self):
        '''
        Send high on Trigger pin
        '''
        # set Trigger_Pin to HIGH
        GPIO.output(self.Trigger_Pin, True)
        # set Trigger_Pin after 0.01ms to LOW
        sleep(0.00001)
        GPIO.output(self.Trigger_Pin, False)


class example_ultrasonic:
    robot = PiArm()
    # write your serial comm
    robot.connect("/dev/ttyS0")

    def __init__(self, distance):

        self.usonic = ultrasonic()

        self.min_dist = distance
        self.commands = [[472, 497, 306, 478, 484, 570],
        [471, 499,303 ,739, 486, 571],
        [472 ,499,206 ,739 ,421, 576],
        [579, 499 ,207, 739 ,408, 576],
        [579, 499 ,206, 739 ,533, 576],
        [579, 499 ,206 ,748 ,555, 944],
        [579, 499 ,207 ,748 ,413, 944],
        [498, 499 ,207 ,748 ,420, 944],
        [498, 499 ,208 ,748 ,575, 944],
        [496, 499 ,206 ,749 ,614 ,575]
                        ]

    def distance_compare(self):
        '''
        compare distance and return object detection status
        '''
        distance = self.usonic.distance_check()
        print(distance)
        if distance <= self.min_dist:
            return True
        else:
            return False

    def move_piarm(self):
        '''
        move PiArm if ditance is in given minimum distance
        '''
        if self.distance_compare():
            print('changing PiArm position')
            for command in self.commands:
                for ID in range(6):
                    self.robot.servoWrite(ID + 1, command[ID], 500)
                sleep(1)
        else:
            pass

if __name__ == '__main__':
    ex = example_ultrasonic(distance = 15)
    try:
        while True:
            ex.move_piarm()
            sleep(.5)
    except KeyboardInterrupt:
        robot = PiArm()
        # write your serial comm
        robot.connect("/dev/ttyS0")
        for ID in range(1, 7):
            robot.servoWrite(ID, 500, 500)