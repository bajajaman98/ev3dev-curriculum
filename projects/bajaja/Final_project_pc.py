#Idea: Writes music, each colour it  runs over corresponds to a different note, you can drive using the IR Remote, the notes that have been written display on the TKinter, each channel corresponds to a different length of note. To play the song, the pc sends the notes to the ev3 and the ev3 plays the song. If the robot stays still for 3 seconds, it adds a rest, unless there is something directly in front of the IR sensor (Can put the IR Remote there). If there is something directly in front of the robot, it can't drive forward. If the IR Remote is put in beacon remote and placed in front of the robot, the robot shuts off all motor and then turns off. Edit: Holding button makes rest, pressing button makes corresponding note.Back button deletes note. Touch sensor ends program.

import tkinter
from tkinter import ttk, Canvas

import mqtt_remote_method_calls as com

class Music_sheet():
    def __init__(self):
        self.mqtt_client = com.MqttClient(self)
        self.beat_length = 0.5
        self.root = tkinter.Tk()
        self.root.title("MQTT Remote")
        self.main_frame = ttk.Frame(self.root, padding=20, relief='raised')
        self.main_frame.grid()
        self.canvas = Canvas(self.main_frame, width = 200, height = 200)
        self.canvas.create_line(10,50,330,50)
        self.canvas.create_line(10,60,330,60)
        self.canvas.create_line(10,70,330,70)
        self.canvas.create_line(10,80,330,80)
        self.canvas.create_line(10,90,330,90)
        self.note_images = [tkinter.PhotoImage(file='upper_quarter_note.png').subsample(6),tkinter.PhotoImage(file='upper_half_note.png').subsample(6),tkinter.PhotoImage(file='upper_dotted_quarter_note.png').subsample(6),tkinter.PhotoImage(file='one_eighth_note_upper.png').subsample(6),tkinter.PhotoImage(file='whole_note.png').subsample(6)]
        self.rest_images = [tkinter.PhotoImage(file='quarter_rest.png').subsample(6),
                            tkinter.PhotoImage(file='half_rest.png').subsample(6),
                            tkinter.PhotoImage(file='eighth_rest.png').subsample(6),
                            tkinter.PhotoImage(file='whole_rest.png').subsample(6)]
        self.notes_added = []
        self.actual_notes = []
        self.beats = []

    def add_rest(self,length):
        rest_pitch = 0
        if length == self.beat_length:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,52,image = self.rest_images[0],anchor=tkinter.NW)
        elif length == self.beat_length*2:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,52,image = self.rest_images[1],anchor=tkinter.NW)
        elif length == self.beat_length/2:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,52,image = self.rest_images[2],anchor=tkinter.NW)
        else:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,52,image = self.rest_images[3],anchor=tkinter.NW)
        self.notes_added.append(new_note)
        self.actual_notes.append(rest_pitch)
        self.beats.append(length)

    def add_note(self,colour,length):
        # notes = ['c','d','e','f','g','a','b'] #black,blue,green,yellow,red,white,brown
        self.pitches = [262, 294, 330, 349, 392, 440, 494]
        self.mqtt_client.send_message("play_note",[self.pitches[colour],length])
        if length == self.beat_length:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,57 - colour*5,image = self.note_images[0],anchor=tkinter.NW)
        elif length == self.beat_length*2:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,57 - colour*5,image = self.note_images[1],anchor=tkinter.NW)
        elif length == self.beat_length*1.5:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,57 - colour*5,image = self.note_images[2],anchor=tkinter.NW)
        elif length == self.beat_length/2:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,57 - colour*5,image = self.note_images[3],anchor=tkinter.NW)
        else:
            new_note = self.canvas.create_image(10+len(self.notes_added)*20,60 - colour*5,image = self.note_images[4],anchor=tkinter.NW)
        self.notes_added.append(new_note)
        self.actual_notes.append(self.pitches[colour])
        self.beats.append(length)

    def reset(self):
        for k in range(len(self.notes_added)):
            self.canvas.delete(self.notes_added[k])
        self.notes_added = []
        self.actual_notes = []
        self.beats = []

    def delete(self):
        self.canvas.delete(self.notes_added[len(self.notes_added)-1])
        del self.notes_added[(len(self.notes_added) - 1)]
        del self.actual_notes[len(self.actual_notes)-1]
        del self.beats[len(self.beats)-1]

    def play(self):
        for k in range(len(self.actual_notes)):
            self.mqtt_client.send_message("play_note",[self.actual_notes[k],self.beats[k]])


def main():

    music_sheet = Music_sheet()
    mqtt_client = music_sheet.mqtt_client
    mqtt_client.connect_to_ev3()

    music_sheet.canvas.grid(columnspan = 5)

    reset_button = ttk.Button(music_sheet.main_frame, text="Reset")
    reset_button.grid(row=1,column=0)
    reset_button['command'] = (lambda: music_sheet.reset())

    delete_button = ttk.Button(music_sheet.main_frame,text="Delete")
    delete_button.grid(row=1,column=1)
    delete_button['command'] = (lambda: music_sheet.delete())

    q_button = ttk.Button(music_sheet.main_frame, text="Quit")
    q_button.grid(row=1, column=2)
    # q_button['command'] = (lambda: quit_program(mqtt_client, False))
    q_button['command'] = (lambda: music_sheet.add_note(3,1))

    e_button = ttk.Button(music_sheet.main_frame, text="Exit")
    e_button.grid(row=1, column=3)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    play_button = ttk.Button(music_sheet.main_frame, text="play")
    play_button.grid(row=1, column=4)
    play_button['command'] = (lambda: music_sheet.play())

    music_sheet.root.bind('<Up>', lambda event: send_forward(mqtt_client,500))
    music_sheet.root.bind('<Left>', lambda event: send_left(mqtt_client, 500))
    music_sheet.root.bind('<Right>', lambda event: send_right(mqtt_client, 500))
    music_sheet.root.bind('<Down>', lambda event: send_back(mqtt_client, 500))
    music_sheet.root.bind('<a>', lambda event: music_sheet.add_rest(1))
    music_sheet.root.bind('<b>', lambda event: music_sheet.add_rest(0.5))



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