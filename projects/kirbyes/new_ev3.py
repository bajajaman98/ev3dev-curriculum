import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo

robot = robo.Snatch3r()
mqtt_client = com.MqttClient(robot)
mqtt_client.connect_to_pc()
robot.loop_forever()


def loop_forever(self):
    self.running = True
    while self.running:
        btn = ev3.Button()
        btn.on_backspace = lambda state: handle_shutdown(state, robot)

        if ev3.ColorSensor.color == ev3.ColorSensor.COLOR_RED:
            print(ev3.ColorSensor.color)
            robot.stop()
            send_restore(mqtt_client)
            time.sleep(3)
            ev3.Sound.speak("Your Pokemon is Fully Healed").wait()

        if ev3.ColorSensor.color == ev3.ColorSensor.COLOR_GREEN:
            print(ev3.ColorSensor.color)
            ev3.Sound.speak("A Wild Pokemon has appeared").wait()
            robot.stop()
            ev3.Sound.speak("Your Pokemon has been injured").wait()
            send_hurt(mqtt_client)
            ev3.Sound.speak("The foe has fainted").wait()

            btn.process()
            time.sleep(0.01)


def handle_shutdown(button_state, my_delegate):
    """Exit the program."""
    if button_state:
        my_delegate.running = False


def send_restore(mqtt_client):
    mqtt_client.send_message("hp_restore")


def send_hurt(mqtt_client):
    mqtt_client.send_message("hp_hurt")
