import tkinter
from tkinter import ttk, BOTH
import mqtt_remote_method_calls as com


def main():
    master = Tk()

    Label(text="one").pack()

    separator = Frame(height=2, bd=1, relief=SUNKEN)
    separator.pack(fill=X, padx=5, pady=5)

    Label(text="two").pack()

    mainloop()

main()
