"""
This is my final project code. The basic idea behind this code is the game Pokemon.

Author: Eric Kirby
"""

import tkinter
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import time

import mqtt_remote_method_calls as com

hp = 100


class MyDelegate(object):
    def __init__(self, main_frame):
        self.running = True
        self.main_frame = main_frame

    def hp_restore(self):
        global hp
        hp = 100
        hp_label = ttk.Label(self.main_frame, text="HP:" + str(hp))
        hp_label.grid(row=2, column=0)

    def hp_hurt(self):
        global hp
        hp = 50.0
        hp_label = ttk.Label(self.main_frame, text="HP:" + str(hp))
        hp_label.grid(row=2, column=0)


def main():
    root = tkinter.Tk()
    root.title("Pokemon")

    main_frame = ttk.Frame(root, padding=5)
    main_frame.grid()

    # Make a tkinter.Canvas on a Frame.
    canvas = tkinter.Canvas(main_frame, background="lightgray", width=300, height=200)
    canvas.grid(columnspan=2)

    hp_label = ttk.Label(main_frame, text="HP:" + str(hp))
    hp_label.grid(row=2, column=0)

    # Setting it up
    img = Image.open("Pokemon.png")
    img = img.resize((300, 200), Image.ANTIALIAS)  # The (250, 250) is (height, width)
    img = ImageTk.PhotoImage(img)
    canvas.create_image(1, 1, anchor=NW, image=img)

    speed = 600

    root.bind('<Up>', lambda event: send_forward(mqtt_client, speed))
    root.bind('<Left>', lambda event: send_left(mqtt_client, speed))
    root.bind('<space>', lambda event: send_stop(mqtt_client))
    root.bind('<Right>', lambda event: send_right(mqtt_client, speed))
    root.bind('<Down>', lambda event: send_back(mqtt_client, speed))

    # Buttons for quit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=2, column=1)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    my_delegate = MyDelegate(main_frame)
    mqtt_client = com.MqttClient(my_delegate)
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
    mqtt_client.send_message("drive", [speed, speed])
    time.sleep(0.1)
    mqtt_client.send_message("stop")


def send_back(mqtt_client, speed):
    print("Moving backwards")
    mqtt_client.send_message("drive", [-1*speed, -1*speed])
    time.sleep(0.1)
    mqtt_client.send_message("stop")


def send_left(mqtt_client, speed):
    print("Turning left")
    mqtt_client.send_message("drive", [-1*speed, speed])
    time.sleep(0.1)
    mqtt_client.send_message("stop")


def send_right(mqtt_client, speed):
    print("Turning right")
    mqtt_client.send_message("drive", [speed, -1*speed])
    time.sleep(0.1)
    mqtt_client.send_message("stop")


def send_stop(mqtt_client):
    print("Stop")
    mqtt_client.send_message("stop")


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
