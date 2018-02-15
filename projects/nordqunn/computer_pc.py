"""
General idea for the project can be found in the readme.md file in this directory.
In this file:
the code to be run on the computer to construct a Tkinter GUI and provide a human interface via MQTT,
sending information from the computer to the robot.
"""

import tkinter
from tkinter import ttk, BOTH
import mqtt_remote_method_calls as com

def main():


    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title('Program Display')

    main_frame = ttk.Frame(root, borderwidth=200, padding=50, relief='raised')
    main_frame.grid()
    reset_button = ttk.Button(main_frame, text='Reset')
    reset_button.grid(row=5, column=2)

    label1 = ttk.Label(main_frame)
    label1['text'] = 'This button does wxyz'
    label1.grid()

    quit_button = ttk.Button(main_frame, text='Quit')
    quit_button.grid(row=6, column=2)
    quit_button['command'] = (lambda: quit_exit_program(mqtt_client, False))

    exit_button = ttk.Button(main_frame, text='Exit')
    exit_button.grid(row=7, column=2)
    exit_button['command'] = (lambda: quit_exit_program(mqtt_client, True))

    entry_field = ttk.Entry(main_frame, width='20', text='Let\'s have a letter')
    entry_field.grid()

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=1, column=2)
    forward_button['command'] = lambda: send_forward(mqtt_client, 300)
    root.bind('<Up>', lambda event: send_forward(mqtt_client, 300))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=2, column=1)
    left_button['command'] = lambda: send_left(mqtt_client, 300)
    root.bind('<Left>', lambda event: send_left(mqtt_client, 300))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=2, column=3)
    right_button['command'] = lambda: send_right(mqtt_client, 300)
    root.bind('<Right>', lambda event: send_right(mqtt_client, 300))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=3, column=2)
    back_button['command'] = lambda: send_back(mqtt_client, 300)
    root.bind('<Down>', lambda event: send_back(mqtt_client, 300))

    root.mainloop()

    puzzle = 'abcdefg'
    puzzle1 = 'bcdefgh'
    puzzle2 = ['a', 'b,' 'c']
    puzzle3 = ['b', 'c', 'd']

    pat(puzzle, puzzle1, puzzle2, puzzle3)


def quit_exit_program(mqtt_client, shutdown_robot): #pass in the client and boolean
    if shutdown_robot:
        print('quit')
        mqtt_client.send_message('shutdown')
    else:
        print('exit')
    mqtt_client.close()
    exit()


def send_forward(mqtt_client,speed):
    print("Moving forward")
    mqtt_client.send_message("drive_inches",[0.1,speed])


def send_left(mqtt_client,speed):
    print("Turning left")
    mqtt_client.send_message("turn_degrees",[1,speed])


def send_right(mqtt_client,speed):
    print("Turning right")
    mqtt_client.send_message("turn_degrees",[-1,speed])


def send_back(mqtt_client,speed):
    print("Moving backwards")
    mqtt_client.send_message("drive_inches",[-0.1,speed])


def pat(entry_field, puzzle, puzzle1, puzzle2, puzzle3):
    if entry_field.get() in puzzle:
        return None # etc
    if 'a' in puzzle:
        print('found the letter a in the STRING')
    if 'a' in puzzle1:
        print('found the letter a in the STRING')
    if 'a' in puzzle2:
        print('found the letter a in the SEQUENCE')
    if 'a' in puzzle3:
        print('found the letter a in the SEQUENCE')
    if 'a' in puzzle:
        print('found the letter a in the SEQUENCE')



# Call main. To get the ball running of course.
main()
