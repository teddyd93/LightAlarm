# LightAlarm
Very Small-Scale raspberry pi program for controlling outlets through GPIO.

Design Motivation was to create an alarm which wakes the user up with a flashing light. The setup can also signal a 5V device to turn on, such as a PC, by splicing the trigger into the power switch PINS on the motherboard.

Electrically, the pi sends output through the GPIO pins to relay, which turns outlet power on to the relays. Input is gained through a simple button.

This was only inteded for personal use, and is thus very simple in it's design.
