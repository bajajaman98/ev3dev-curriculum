"""
This is my final project code. The basic idea behind this code is the game Pokemon.

Author: Eric Kirby
"""

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in


hp = 100


def main():
    root = tkinter.Tk()
    root.title("Pokemon")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    speed = 800

    root.bind('<Up>', lambda event: send_forward(mqtt_client, speed))
    root.bind('<Left>', lambda event: send_left(mqtt_client, speed))
    root.bind('<space>', lambda event: send_stop(mqtt_client))
    root.bind('<Right>', lambda event: send_right(mqtt_client, speed))
    root.bind('<Down>', lambda event: send_back(mqtt_client, speed))

    # Buttons for quit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    pc_delegate = MyDelegateOnThePc()
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def send_forward(mqtt_client, speed):
    print("Moving forward")
    mqtt_client.send_message("drive_inches", [0.1, speed])


def send_back(mqtt_client, speed):
    print("Moving backwards")
    mqtt_client.send_message("drive_inches", [-0.1, speed])


def send_left(mqtt_client, speed):
    print("Turning left")
    mqtt_client.send_message("turn_degrees", [1, speed])


def send_right(mqtt_client, speed):
    print("Turning right")
    mqtt_client.send_message("turn_degrees", [-1, speed])


def send_stop(mqtt_client):
    print("Stop")
    mqtt_client.send_message("drive_inches(0,0)")


def hp_restore():
    global hp
    hp = 100


def hp_hurt():
    global hp
    hp = hp / 2


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
