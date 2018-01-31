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
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    object.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    object.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    def drive_inches(self, inches_target, speed_deg_per_second):
        assert self.left_motor.connected()
        assert self.right_motor.connected()

        ev3.Sound.speak("Drive Inches Vee Ah Library").wait()
        degrees_per_inch = 90
        time_s = 1
        while time_s > 3:
            input_distance = int(input("Enter a distance:"))
            input_speed = int(input("Enter a speed (0-900):"))
            rotations_in_degrees = input_distance * degrees_per_inch
            if input_speed == 0:
                break
            self.left_motor.run_to_rel_pos(position_sp=rotations_in_degrees, speed_sp=input_speed)
            self.right_motor.run_to_rel_pos(position_sp=rotations_in_degrees, speed_sp=input_speed)
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.ev3.Sound.beep().wait()

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

