#Idea: Writes music, each colour it  runs over corresponds to a different note, you can drive using the IR Remote, the notes that have been written display on the TKinter, each channel corresponds to a different length of note. To play the song, the pc sends the notes to the ev3 and the ev3 plays the song. If the robot stays still for 3 seconds, it adds a rest, unless there is something directly in front of the IR sensor (Can put the IR Remote there). If there is something directly in front of the robot, it can't drive forward. If the IR Remote is put in beacon remote and placed in front of the robot, the robot shuts off all motor and then turns off. Edit: Holding button makes rest, pressing button makes corresponding note.Back button deletes note. Touch sensor ends program.

import tkinter
from tkinter import ttk, Canvas

import mqtt_remote_method_calls as com

class Music_sheet():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("MQTT Remote")
        self.main_frame = ttk.Frame(self.root, padding=20, relief='raised')
        self.main_frame.grid()
        self.canvas = Canvas(self.main_frame, width = 200, height = 200)
        self.canvas.create_line(10,50,300,50)
        self.canvas.create_line(10,60,300,60)
        self.canvas.create_line(10,70,300,70)
        self.canvas.create_line(10,80,300,80)
        self.canvas.create_line(10,90,300,90)
        self.note_images = [tkinter.PhotoImage(file='upper_quarter_note.png'),tkinter.PhotoImage(file='upper_half_note.png'),tkinter.PhotoImage(file='upper_dotted_quarter_note.png'),tkinter.PhotoImage(file='one_eighth_note_upper.png'),tkinter.PhotoImage(file='one_eighth_note_lower.png'),tkinter.PhotoImage(file='lower_quarter_note.png'),tkinter.PhotoImage(file='lower_dotted_quarter_note.png'),tkinter.PhotoImage(file='lower_half_note.png'),tkinter.PhotoImage(file='whole_note.png')]

    def add_note(self,colour,length):
        notes = ['c','d','e','f','g','a','b'] #black,blue,green,yellow,red,white,brown
        note_to_add = notes[colour-1]

def main():

    music_sheet = Music_sheet()
    mqtt_client = com.MqttClient(music_sheet)
    mqtt_client.connect_to_ev3()


    music_sheet.canvas.grid(columnspan = 4)


    reset_button = ttk.Button(music_sheet.main_frame, text="Reset")
    reset_button.grid(row=1,column=0)

    delete_button = ttk.Button(music_sheet.main_frame,text="Delete")
    delete_button.grid(row=1,column=1)

    q_button = ttk.Button(music_sheet.main_frame, text="Quit")
    q_button.grid(row=1, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(music_sheet.main_frame, text="Exit")
    e_button.grid(row=1, column=3)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    music_sheet.root.mainloop()


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


main()