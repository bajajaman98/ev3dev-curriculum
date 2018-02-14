"""
This is my final project code. The basic idea behind this code is the game Pokemon.

Author: Eric Kirby
"""

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

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    root.bind('<Up>', lambda event: send_forward(mqtt_client, int(left_speed_entry.get())))
    root.bind('<Left>', lambda event: send_left(mqtt_client, int(right_speed_entry.get())))
    root.bind('<space>', lambda event: send_stop(mqtt_client))
    root.bind('<Right>', lambda event: send_right(mqtt_client, int(left_speed_entry.get())))
    root.bind('<Down>', lambda event: send_back(mqtt_client, int(left_speed_entry.get())))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

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
