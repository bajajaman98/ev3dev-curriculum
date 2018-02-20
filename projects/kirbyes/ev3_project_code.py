"""


Author: Eric Kirby
"""

import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""
    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print(" Pokemon")
    print(" Press Back Button to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("Pokemon").wait()
    robot = robo.Snatch3r()
    dc = DataContainer()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    color_sensor = ev3.ColorSensor()

    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    while dc.running:

        if int(color_sensor.color) == ev3.ColorSensor.COLOR_RED:
            send_restore(mqtt_client)
            time.sleep(5)
            ev3.Sound.speak("Your Pokemon is Fully Healed").wait()

        if int(color_sensor.color) == ev3.ColorSensor.COLOR_GREEN:
            ev3.Sound.speak("A Wild Pokemon has appeared").wait()
            send_hurt(mqtt_client)
            time.sleep(2)
            # ev3.Sound.speak("Your Pokemon has been injured. The foe has fainted").wait()
            # time.sleep(1)
            # ev3.Sound.speak("The foe has fainted").wait()

        btn.process()
        time.sleep(0.01)

    ev3.Sound.speak("Goodbye").wait()


# ----------------------------------------------------------------------
# Button event callback functions
# ----------------------------------------------------------------------
def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


def send_restore(mqtt_client):
    mqtt_client.send_message("hp_restore")


def send_hurt(mqtt_client):
    mqtt_client.send_message("hp_hurt")


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
