#!/usr/bin/env python3
"""
This module lets you practice using the encoder to determine distances while blocking code execution until complete.

You will now use a run_to_rel_pos command to implement the action drive inches action.

Authors: David Fisher and Aman Bajaj.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

# DPNE: 2. Copy the contents of your m1_drive_timed.py and paste that text into this file below these comments.
#   If your program says and prints anything at the start change it to print and say "Drive using encoders"
import ev3dev.ev3 as ev3
import time


def main():
    print("--------------------------------------------")
    print("  Drive using encoders")
    print("--------------------------------------------")
    ev3.Sound.speak("Drive using encoders").wait()

    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected
    degrees_per_inch = 90
    time_s = 1  # Any value other than 0.
    while time_s != 0:
        left_sp = int(input("Enter a speed for the robot (0 to 900 dps): "))
        right_sp = left_sp
        if left_sp == 0:
            break
        distance = int(input("Enter a distance to travel (seconds): "))
        motor_turns_needed_in_degrees = distance * degrees_per_inch
        if distance == 0:
            break
        left_motor.run_to_rel_pos(position_sp = motor_turns_needed_in_degrees, speed_sp = left_sp, stop_action = "brake")
        right_motor.run_to_rel_pos(position_sp = motor_turns_needed_in_degrees, speed_sp = left_sp, stop_action = "brake")
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()


# DONE: 3. Add a beep after the drive motors stop (see code below).  Test your code to hear the beep AFTER movement.
#   ev3.Sound.beep().wait()

# DONE: 4. Instead of using the run_forever, time.sleep, stop pattern switch to using the run_to_rel_pos command.
#   You will need to determine the position_sp value to pass into the run_to_rel_pos command as a named argument.
#   Assume the diameter of the wheel is 1.3" (close enough).  A 1.3" diameter wheel results in approximately a 4"
#     circumference, so 360 degrees = 4 inches of travel.
#   So you need to move through roughly 90 degrees for every inch of travel. That value is very handy!
#
#       degrees_per_inch = 90
#       motor_turns_needed_in_degrees = inches_target * degrees_per_inch
#
#   Delete your time.sleep and .stop commands as well as your speed equations to get time (we no longer care about time)
#     and convert your run_forever method to use a run_to_rel_pos method with appropriate arguments.
#   Your arguments to the run_to_rel_pos method should include the named arguments (notice time is not needed):
#        -- position_sp
#        -- speed_sp
#        -- stop_action

# DONE: 5. Make sure the beep happens AFTER the motors stop.  Use the wait_while command to block code execution.

# TODO: 6. Formally test your work. When you think you have the problem complete run these tests:
#   200 dps 24 inches (make sure it drives within 2 inches of the target distance)
#   400 dps 24 inches (make sure it drives within 2 inches of the target distance)
#   800 dps 24 inches (make sure it drives within 2 inches of the target distance)
#   400 dps 12 inches (make sure it drives within 1 inches of the target distance)
#   400 dps 36 inches (make sure it drives within 3 inches of the target distance)
#   400 dps -36 inches (make sure it drives within 3 inches of the target distance)
# Add more tests as you see fit.  Ideally you should be +/- 10% of the target goal this time.

# TODO: 7. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.
#
# Observations you should make, run_to_rel_pos is easier to use since it uses encoders that are independent of speed.


