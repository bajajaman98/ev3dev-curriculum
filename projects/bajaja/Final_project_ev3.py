import robot_controller as robo
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
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
        for k in range(len(beacons)):
            if beacons[k].distance != -128 and beacons[k].distance < 2:
                robot.shutdown()
        btn.on_enter = lambda state: send_rest(robot.color_sensor.color,mqtt_client)
        btn.on_up = lambda state: send_quarter(robot.color_sensor.color,mqtt_client)
        btn.on_left = lambda state: send_half(robot.color_sensor.color, mqtt_client)
        btn.on_right = lambda state: send_whole(robot.color_sensor.color, mqtt_client)
        btn.on_down = lambda state: send_eighth(robot.color_sensor.color, mqtt_client)
    mqtt_client.send_message("quit_program",[backwards_mqtt,True])
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------


def send_rest(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),0])


def send_quarter(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),beat_length])


def send_eighth(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),beat_length/2])


def send_half(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),beat_length*2])


def send_whole(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),beat_length*4])


main()