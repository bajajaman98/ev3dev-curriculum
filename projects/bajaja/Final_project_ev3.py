import robot_controller as robo
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
beat_length = 0.5

def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    backwards_mqtt = com.MqttClient
    backwards_mqtt.connect_to_ev3()
    bs1 = ev3.BeaconSeeker(channel=1)
    bs2 = ev3.BeaconSeeker(channel=2)
    bs3 = ev3.BeaconSeeker(channel=3)
    bs4 = ev3.BeaconSeeker(channel=4)
    btn = ev3.Button
    beacons = [bs1,bs2,bs3,bs4]
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    while not robot.touch_sensor.is_pressed:
        btn.on_enter = lambda state: send_dotted_quarter(robot.color_sensor.color,mqtt_client)
        btn.on_left = lambda state: send_half(robot.color_sensor.color, mqtt_client)
        btn.on_right = lambda state: send_whole(robot.color_sensor.color, mqtt_client)
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

    mqtt_client.send_message("quit_program",[backwards_mqtt,True])
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------


def send_rest(mqtt_client,length):
    mqtt_client.send_message("add_rest",[mqtt_client,length])


def send_quarter(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length])


def send_eighth(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length/2])


def send_half(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length*2])


def send_whole(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length*4])


def send_dotted_quarter(colour,mqtt_client):
    mqtt_client.send_message("add_note",[int(colour),beat_length*1.5])


main()