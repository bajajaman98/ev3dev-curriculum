"""
Code to be run on the ev3 robot.
"""

import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    robot.loop_forever()

# Call main. To get the ball rolling of course.
main()
