"""
This is my final project code. The basic idea behind this code is the game Pokemon.

Author: Eric Kirby
"""

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    # Setup an mqtt_client.
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    speed = 800

    root.bind('<Up>', lambda event: send_forward(mqtt_client, speed))
    root.bind('<Left>', lambda event: send_left(mqtt_client, speed))
    root.bind('<space>', lambda event: send_stop(mqtt_client))
    root.bind('<Right>', lambda event: send_right(mqtt_client, speed))
    root.bind('<Down>', lambda event: send_back(mqtt_client, speed))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    if ev3.ColorSensor.color == ev3.ColorSensor.COLOR_GREEN:
        mqtt_client.send_message("stop")

    if ev3.ColorSensor.color == ev3.ColorSensor.COLOR_RED:
        mqtt_client.send_message("stop")

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------

# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# Drive Motor command callbacks
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


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
