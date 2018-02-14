import robot_controller as robo
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    bs1 = ev3.BeaconSeeker(channel=1)
    bs2 = ev3.BeaconSeeker(channel=2)
    bs3 = ev3.BeaconSeeker(channel=3)
    bs4 = ev3.BeaconSeeker(channel=4)
    btn = ev3.Button
    running = True
    beacons = [bs1,bs2,bs3,bs4]
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    while True:
        if running:
            for k in range(len(beacons)):
                if beacons[k].distance != -128 and beacons[k].distance < 2:
                    robot.shutdown()
            btn.on_enter = lambda state: send_rest(robot.color_sensor.color,mqtt_client)
            btn.on_up = lambda state: send_quarter(robot.color_sensor.color,mqtt_client)
            btn.on_left = lambda state: send_half(robot.color_sensor.color, mqtt_client)
            btn.on_right = lambda state: send_whole(robot.color_sensor.color, mqtt_client)
            btn.on_down = lambda state: send_eighth(robot.color_sensor.color, mqtt_client)
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------


def send_rest(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),0])


def send_quarter(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),0.5])


def send_eighth(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),0.25])


def send_half(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),1])


def send_whole(color,mqtt_client):
    mqtt_client.send_message("add_note",[int(color),2])


main()