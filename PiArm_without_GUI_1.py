from piarm import PiArm
from time import sleep
import re

robo = PiArm()
robo.connect('/dev/ttyS0')
command_data = []

file = open('/home/pi/PiArm/Export Files/pick and place.txt', 'r')

for line in file:
    command_data.append(line.strip())

size = len(command_data)
print(size)

for command in range(0,size):
    raw_Data = command_data[command]
    raw_Data = raw_Data.split('  ')
    delay = raw_Data.pop()
    delay = delay.split(':')

    delay = int(int(delay[1])/1000)
    print('Go- ', raw_Data, delay)

    for value in range(6):
        cmd_Data = re.findall('\d+',raw_Data[value])
        print('Cmd Data- ', cmd_Data)
        robo.servoWrite(int(cmd_Data[0]), int(cmd_Data[1]), int(cmd_Data[2]))

    sleep(delay)