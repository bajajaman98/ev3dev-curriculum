# This is csse120. 
## This is the final project documentation. 

# Robot Wheel of Fortune 
## Requirements for A Grade: 
* MQTT: Must use an mqtt client to send information both from the robot to the PC and from the PC to the robot. This info must be integrated into the rest of the program in an interesting way, not just as an add-on feature.
* TKinter: Must have a nice-looking TKinter GUI on the PC with several buttons, text, etc. Includes some type of widget that you didn’t learn about in the video to do something interesting.
* Analog sensors: Must use at least one in an interesting way.
* Digital inputs: Must use at least one digital input in some way.
* Motors: The robot must drive via remote control and/or in some way that depends on its environment.
* Sensor → motor interaction: The sensors and actions (motor movements) must interact in an interesting way. While we don’t want to give spoilers here, consider the line following module as an example: the color sensor input was used to control the motors, which as the robot moved, affected the color sensors.  The sensors and actions interact in an interesting way.
* Creativity: Your project should be fun and interesting.  One potential way to check this box is to have a theme for your project.  For example, “My project is a PACMAN game” or “My robot is a fire fighter” then explain how you are using that theme in your project.
* Human input: You must allow the user to interact with the robot in some interesting way.  (So while line following is cool, it didn’t have human interaction / input.)
An A project would either include all of these features or all but one of these features with one exceptional feature.
 
 ## Implementation 
 * Tkinter empty rectangle board...or nice colors & shit? 
 * Tkinter window: Canvas widget, Enter widget (class), Text widget 
 * user input into tkinter the letter 
 * self drive using the arrow keys on the letter to sticky notes on the floor or on the wall
 * use the pixy camera (wall) or the color sensor to 'touch' the panel 
    * concern: the pixy camera's line of sight isn't narrow enough for that degree of precision. You might need big-ass sheets of colored paper for that. 
    
 ####Extra Shit 
 * leds light up when you guess a right letter 
 * little beep sound when you guess a wrong answer 
 * some sort of random spin wheel for dollar amounts 
 * picture on the ev3 screen in the theme 