import robot_controller as robo
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
beat_length = 0.5

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    btn = ev3.Button()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
        #btn.on_down = lambda state: send_eighth(robot.color_sensor.color,mqtt_client)
    while not robot.touch_sensor.is_pressed:
        if btn.down:
            for k in range(30):
                time.sleep(100)
                if not btn.down:
                    send_eighth(robot.color_sensor,mqtt_client)
                    break
            if btn.down:
                send_rest(mqtt_client,beat_length/2)
        if btn.up:
            for k in range(30):
                time.sleep(100)
                if not btn.up:
                    send_quarter(robot.color_sensor,mqtt_client)
                    break
            if btn.up:
                send_rest(mqtt_client,beat_length)
        if btn.left:
            for k in range(30):
                time.sleep(100)
                if not btn.left:
                    send_half(robot.color_sensor,mqtt_client)
                    break
            if btn.left:
                send_rest(mqtt_client,beat_length*2)
        if btn.right:
            for k in range(30):
                time.sleep(100)
                if not btn.right:
                    send_whole(robot.color_sensor,mqtt_client)
                    break
            if btn.right:
                send_rest(mqtt_client,beat_length*4)
        if btn.enter:
            for k in range(30):
                time.sleep(100)
                if not btn.enter:
                    send_dotted_quarter(robot.color_sensor,mqtt_client)
                    break
            if btn.enter:
                send_rest(mqtt_client,beat_length*1.5)
        if btn.backspace:
            for k in range(30):
                time.sleep(100)
                if not btn.backspace:
                    break
            if btn.backspace:
                mqtt_client.send_message("delete_note")
    robot.shutdown()
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------


def send_rest(mqtt_client,length):
    mqtt_client.send_message("add_rest",[length])


def send_quarter(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length])


def send_eighth(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length/2])
    print("hello")


def send_half(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length*2])


def send_whole(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length*4])


def send_dotted_quarter(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length*1.5])


main()