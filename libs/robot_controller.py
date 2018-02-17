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
import math
import time


class Snatch3r(object):
    # TODO: Implement the Snatch3r class as needed when working the sandbox exercises

    def __init__(self):
        """The function used to initialize an instance of the Snatch3r class"""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.running = True
        self.color_key = ''
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.color_sensor.connected
        assert self.ir_sensor.connected
        assert self.pixy.connected
        # unnecessary comment to push

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
        print("hello arm down")
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
            time.sleep(0.01)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.

        Type hints:
          :type robot: robo.Snatch3r
          :rtype: bool
        """
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:

            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.turn_degrees(5, 100)
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    self.drive_inches(1, 300)
                    if current_distance == 0:
                        return True
                if math.fabs(current_heading) >= 2 and math.fabs(current_heading) <= 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading > 0:
                        self.turn_degrees(-1, 300)
                    else:
                        self.turn_degrees(1, 300)
                if math.fabs(current_heading) > 10:
                    print("Heading is too far off to fix")
                    self.turn_degrees(1, 100)
            time.sleep(0.2)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False

    def set_leds(self, led_side_string, led_color_string):
        led_side = None
        if led_side_string == 'left':
            led_side = ev3.Leds.LEFT
        elif led_side_string == 'right':
            led_side = ev3.Leds.RIGHT

        led_color = None
        if led_color_string == 'green':
            led_color = ev3.Leds.GREEN
            self.color_key = ev3.ColorSensor.COLOR_GREEN
        elif led_color_string == 'red':
            led_color = ev3.Leds.RED
            self.color_key = ev3.ColorSensor.COLOR_RED
        elif led_color_string == 'black':
            led_color = ev3.Leds.BLACK
            self.color_key = ev3.ColorSensor.COLOR_BLACK
        elif led_color_string == 'yellow':
            led_color = ev3.Leds.YELLOW
            self.color_key = ev3.ColorSensor.COLOR_YELLOW

        if led_side is None or led_color is None:
            print('Invalend parameters sent to set_led. led_side_string = {} led_color_string = {}'.format(
                led_side_string, led_color_string))
        else:
            ev3.Leds.set_color(led_side, led_color)

    def drive(self, left_speed_set, right_speed_set):
        """keeps robot running"""
        self.left_motor.run_forever(speed_sp=left_speed_set)
        self.right_motor.run_forever(speed_sp=right_speed_set)

    def play_note(self, tone, length):
        ev3.Sound.tone(tone, length*1000).wait()