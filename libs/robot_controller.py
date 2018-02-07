"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
# import math
import time


class Snatch3r(object):
    # TODO: Implement the Snatch3r class as needed when working the sandbox exercises

    def __init__(self):
        """The function used to initialize an instance of the Snatch3r class"""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor

    def drive_inches(self, inches_target, speed_deg_per_second):
        degrees_per_inch = 90
        rotations_in_degrees = inches_target * degrees_per_inch
        if speed_deg_per_second != 0:
            self.left_motor.run_to_rel_pos(position_sp=rotations_in_degrees, speed_sp=speed_deg_per_second)
            self.right_motor.run_to_rel_pos(position_sp=rotations_in_degrees, speed_sp=speed_deg_per_second)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        degrees_per_turning_degree = 4.7
        degrees_spin_wheel = degrees_to_turn * degrees_per_turning_degree
        if turn_speed_sp < 0:
            self.right_motor.run_to_rel_pos(position_sp=-degrees_spin_wheel, speed_sp=turn_speed_sp)
            self.left_motor.run_to_rel_pos(position_sp=degrees_spin_wheel, speed_sp=turn_speed_sp)
        elif turn_speed_sp > 0:
            self.left_motor.run_to_rel_pos(position_sp=-degrees_spin_wheel, speed_sp=turn_speed_sp)
            self.right_motor.run_to_rel_pos(position_sp=degrees_spin_wheel, speed_sp=turn_speed_sp)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        print('position:', self.arm_motor.position_sp)
        arm_revolutions_for_full_range = int(14.2 * 360)
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        print("hello")
        ev3.Sound.beep().wait()

        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range,speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).
        print('position:', self.arm_motor.position_sp)

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        print("hello")
        ev3.Sound.beep().wait()

    def arm_down(self):
        self.arm_motor.speed_sp = 800
        self.arm_motor.run_to_abs_pos(position_sp=0)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def shutdown(self):
        self.left_motor.stop()
        self.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print("Goodbye")
        ev3.Sound.speak("Goodbye")
        self.running = False

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.