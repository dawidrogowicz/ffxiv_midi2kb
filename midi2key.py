import os
import mido
from threading import Thread
from time import sleep
from pynput.keyboard import Key, Controller

kb = Controller()
mido.Backend('mido.backends.rtmidi/LINUX_ALSA')

press = kb.press
release = kb.release

shift = Key.shift
ctrl = Key.ctrl
space = Key.space
alt = Key.alt

startingNote = 48

currentPort = None

letterNoteMap = "q2w3er5t6y7ui9o0p[=zsxdcvgbhnmk,l.;/'"

MainLoop = True
CloseThread = False


# midi port selection
def select_port():
    global currentPort
    if currentPort:
        currentPort.close()
    print("Select input device:")
    inputports = mido.get_input_names()
    
    for portNumber, portName in enumerate(inputports):
        print(str(portNumber + 1) + ": " + portName)
    while True:
        selectedport = int(input("(enter a number from 1 to " + str(len(inputports)) + ")\n")) - 1
        if 0 <= selectedport < len(inputports):
            break
        else:
            print("Please select a valid input device.")
    print("Selected " + inputports[selectedport])
    return inputports[selectedport]

 
# simulate qwerty keypress
def simulate_key(type, note, velocity):
    if not (-15 <= note - startingNote <= 88):
        return
    index = note - startingNote
    key = 0
    try:
        key = letterNoteMap[index]
    except:
        pass
    if type == 'note_on':
        press(key)
    else:
        release(key.lower())

# read and interpret midi input
def parse_midi(message):
    if message.velocity == 0:
        simulate_key('note_off', message.note, message.velocity)
    else:
        simulate_key(message.type, message.note, message.velocity)


# main program loop
def Main():
    global CloseThread
    print("Now listening to note events on " + str(currentPort) + "...")
    for message in currentPort:
        parse_midi(message)
        if CloseThread:
            break
    CloseThread = False


# clear prints
def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


try:
    currentPort = mido.open_input(select_port())

    while MainLoop:
        Clear()
        Thread(target=Main).start()
        sleep(.5)
        CloseThread = True

except Exception as E:
    Clear()
    print('Error detected')
    input(E)
