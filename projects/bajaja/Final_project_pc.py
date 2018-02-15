#Idea: Writes music, each colour it  runs over corresponds to a different note, you can drive using the IR Remote, the notes that have been written display on the TKinter, each channel corresponds to a different length of note. To play the song, the pc sends the notes to the ev3 and the ev3 plays the song. If the robot stays still for 3 seconds, it adds a rest, unless there is something directly in front of the IR sensor (Can put the IR Remote there). If there is something directly in front of the robot, it can't drive forward. If the IR Remote is put in beacon remote and placed in front of the robot, the robot shuts off all motor and then turns off. Edit: Holding button makes rest, pressing button makes corresponding note.Back button deletes note. Touch sensor ends program.

import tkinter
from tkinter import ttk, Canvas, Frame, X

import mqtt_remote_method_calls as com

class Music_sheet(Frame):
    def __init__(self):
        super().__init__()
        self.draw_sheet()

    def draw_sheet(self):
        self.canvas = Canvas(self)
        self.canvas.create_line(10,10,300,10)
        self.canvas.create_line(10,40,300,40)
        self.canvas.create_line(10,70,300,70)
        self.canvas.create_line(10,100,300,100)
        self.canvas.create_line(10,130,300,130)
        self.canvas.pack(fill = X, expand = 1.5)


def main():

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    reset_button = ttk.Button(main_frame, text="Reset")
    reset_button.grid(row=4,column=2)

    delete_button = ttk.Button(main_frame,text="Delete")
    delete_button.grid(row=3,column=2)

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def send_forward(mqtt_client,speed):
    print("Moving forward")
    mqtt_client.send_message("drive_inches",[0.1,speed])


def send_back(mqtt_client,speed):
    print("Moving backwards")
    mqtt_client.send_message("drive_inches",[-0.1,speed])


def send_left(mqtt_client,speed):
    print("Turning left")
    mqtt_client.send_message("turn_degrees",[1,speed])


def send_right(mqtt_client,speed):
    print("Turning right")
    mqtt_client.send_message("turn_degrees",[-1,speed])


def send_stop(mqtt_client):
    print("Stop")
    mqtt_client.send_message("drive_inches(0,0)")


def add_note(colour, mqtt_client):



def add_rest(mqtt_client, length):


main()