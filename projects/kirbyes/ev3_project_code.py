"""


Author: Eric Kirby
"""

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo


class MyDelegate(object):
    def __init__(self):
        self.running = True


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""
    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print(" Pokemon")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("Pokemon").wait()
    robot = robo.Snatch3r()
    dc = DataContainer()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, robot)

    while dc.running:
        btn.process()
        time.sleep(0.01)


# ----------------------------------------------------------------------
# Button event callback functions
# ----------------------------------------------------------------------
def handle_shutdown(button_state, my_delegate):
    """Exit the program."""
    if button_state:
        my_delegate.running = False


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
