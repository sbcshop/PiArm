import speech_recognition as sr
import time, datetime
import pyaudio
from piarm import PiArm
import re
from time import sleep


robo = PiArm()
robo.connect('/dev/ttyS0')

r = sr.Recognizer()
r.energy_threshold = 4000
sample_rate = 48000
chunk_size = 1024

pos = [[472, 497, 306, 478, 484, 570],
        [471, 499,303 ,739, 486, 571],
        [472 ,499,206 ,739 ,421, 576],
        [579, 499 ,207, 739 ,408, 576],
        [579, 499 ,206, 739 ,533, 576],
        ]
pos1 = [[579, 499 ,206 ,748 ,555, 944],
        [579, 499 ,207 ,748 ,413, 944],
        [498, 499 ,207 ,748 ,420, 944],
        [498, 499 ,208 ,748 ,575, 944],
        [496, 499 ,206 ,749 ,614 ,575]]

mic_list = sr.Microphone.list_microphone_names()
print(mic_list)
device_id = 0
for i in mic_list:
    if i == 'Yeti Stereo Microphone: USB Audio (hw:1,0)':
        device_id = mic_list.index(i)

while True:
    with sr.Microphone(device_index = device_id, sample_rate = sample_rate,chunk_size = chunk_size) as source:
        r.adjust_for_ambient_noise(source)
        print("Say Something")

        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            text = text.lower()
            print("you said: " + text)
            if re.search("pic", text):
                if re.search('item', text):
                    print("pick item")
                    for command in pos:
                        for ID in range(6):
                            robo.servoWrite(ID + 1, command[ID], 500)
                        sleep(1)

            elif re.search("place", text):
                print("Place item")
                for command in pos1:
                    for ID in range(6):
                        robo.servoWrite(ID + 1, command[ID], 500)
                    sleep(1)


        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        except AssertionError or KeyboardInterrupt:
            print("Problem with Audio Source")
            break