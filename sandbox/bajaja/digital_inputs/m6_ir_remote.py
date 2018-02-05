#!/usr/bin/env python3
"""
  This is your opportunity to work as a team on a mini-project.  You will need to handle the following actions.

  When your program starts it should say IR Remote, print instructions, and do a robot.arm_calibration()

  IR remote channel 1 to drive the crawler tracks around:
    -- Pressing  red up   makes the left  LED turn green and the left_motor  move at  600.
         Releasing turns off the LED and stops left_motor.
    -- Pressing  red down makes the left  LED turn red   and the left_motor  move at -600.
         Releasing turns off the LED and stops left_motor.
    -- Pressing  blue up  makes the right LED turn green and the right_motor move at  600.
         Releasing turns off the LED and stops right_motor.
    -- Pressing blue down makes the right LED turn red   and the right_motor move at -600.
         Releasing turns off the LED and stops right_motor.
    You should be able to use one red (left) button and one blue (right) button at the same time.  For example:
     while pressing both red up and blue down the robot should spin and LEDs will be green (left) and red (right).

  IR remote channel 2 to raise and lower the arm
    -- Pressing red up   calls robot.arm_up().
    -- Pressing red down calls robot.arm_down(). 
    -- Pressing blue up  calls robot.arm_calibration().

  Buttons
    -- Pressing the Back button will allow your program to end.  It should stop motors, turn on both green LEDs, and
       then print and say Goodbye.  You will need to implement a new robot method called shutdown to handle this task.

Authors: David Fisher and Aman Bajaj.
"""  # DONE: 1. PUT YOUR NAME IN THE ABOVE LINE.

import ev3dev.ev3 as ev3
import time

import robot_controller as robo

# Note that todo2 is farther down in the code.  That method needs to be written before you do todo3.
# DONE: 3. Have someone on your team run this program on the EV3 and make sure everyone understands the code.
# Can you see what the robot does and explain what each line of code is doing? Talk as a group to make sure.


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True


def main():
    print("--------------------------------------------")
    print("IR Remote")
    print(" - Use IR remote channel 1 to drive around")
    print(" - Use IR remote channel 2 to for the arm")
    print(" - Press the Back button on EV3 to exit")
    print("--------------------------------------------")
    ev3.Sound.speak("I R Remote")

    ev3.Leds.all_off()  # Turn the leds off
    robot = robo.Snatch3r()
    dc = DataContainer()
    rc1 = ev3.RemoteControl(channel=1)
    rc2 = ev3.RemoteControl(channel=2)

    # TODO: 4. Add the necessary IR handler callbacks as per the instructions above.
    # Remote control channel 1 is for driving the crawler tracks around (none of these functions exist yet below).
    # Remote control channel 2 is for moving the arm up and down (all of these functions already exist below).

    # For our standard shutdown button.
    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)
    rc1.on_red_up = lambda state: handle_left_forward(state, robot)
    rc1.on_red_down = lambda state: handle_left_backward(state, robot)
    rc1.on_blue_up = lambda state: handle_right_forward(state, robot)
    rc1.on_blue_down = lambda state: handle_right_backward(state, robot)
    rc2.on_red_up = lambda state: handle_arm_up_button(state, robot)
    rc2.on_red_down = lambda state: handle_arm_down_button(state, robot)
    rc2.on_blue_up = lambda state: handle_calibrate_button(state, robot)
    robot.arm_calibration()  # Start with an arm calibration in this program.

    while dc.running:
        # DONE: 5. Process the RemoteControl objects.
        rc1.process()
        rc2.process()
        btn.process()
        time.sleep(0.01)

    # DONE: 2. Have everyone talk about this problem together then pick one  member to modify libs/robot_controller.py
    # as necessary to implement the method below as per the instructions in the opening doc string. Once the code has
    # been tested and shown to work, then have that person commit their work.  All other team members need to do a
    # VCS --> Update project...
    # Once the library is implemented any team member should be able to run his code as stated in todo3.
    btn.on_backspace = robot.shutdown()

# ----------------------------------------------------------------------
# Event handlers
# Some event handlers have been written for you (ones for the arm).
# Movement event handlers have not been provided.
# ----------------------------------------------------------------------
# DONE: 6. Implement the IR handler callbacks handlers.

# TODO: 7. When your program is complete, call over a TA or instructor to sign your checkoff sheet and do a code review.
#
# Observations you should make, IR buttons are a fun way to control the robot.


def handle_arm_up_button(button_state, robot):
    """
    Moves the arm up when the button is pressed.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
    """
    if button_state:
        robot.arm_up()


def handle_arm_down_button(button_state, robot):
    """
    Moves the arm down when the button is pressed.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
    """
    if button_state:
        robot.arm_down()


def handle_calibrate_button(button_state, robot):
    """
    Has the arm go up then down to fix the starting position.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
    """
    if button_state:
        robot.arm_calibration()


def handle_shutdown(button_state, dc):
    """
    Exit the program.

    Type hints:
      :type button_state: bool
      :type dc: DataContainer
    """
    if button_state:
        dc.running = False

def handle_left_forward(button_state, robot):
    if button_state:
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        robot.left_motor.run_to_rel_pos(speed_sp = 600, position_sp = 100)
    else:
        robot.left_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

def handle_left_backward(button_state, robot):
    if button_state:
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
        robot.left_motor.run_to_rel_pos(speed_sp = -600, position_sp = 100)
    else:
        robot.left_motor.stop()
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

def handle_right_forward(button_state, robot):
    if button_state:
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        robot.right_motor.run_to_rel_pos(speed_sp=600, position_sp=100)
    else:
        robot.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)

def handle_right_backward(button_state, robot):
    if button_state:
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
        robot.right_motor.run_to_rel_pos(speed_sp=-600, position_sp=100)
    else:
        robot.right_motor.stop()
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
