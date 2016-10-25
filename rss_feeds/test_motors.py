#!/usr/bin/python
# -*- coding: utf-8 -*-


###############################################################################
## Imports

# Adafruit library realted imports
import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor


# Recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# Make the two motors turn simultaniously
def rotate_motors(motor1, motor2):
	for i in range(0, 200):
		motor1.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
		motor2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.SINGLE)
	for i in range(0, 200):
		motor1.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.DOUBLE)
		motor2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
	for i in range(0, 200):
		motor1.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.INTERLEAVE)
		motor2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
	for i in range(0, 200):
		motor1.oneStep(Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.MICROSTEP)
		motor2.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)


# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT()

atexit.register(turnOffMotors)

motor1 = mh.getStepper(200, 1)  	# 200 steps/rev, motor port #1
motor1.setSpeed(60)  				# RPM
motor2 = mh.getStepper(200, 2)
motor2.setSpeed(60)

rotate_motors(motor1, motor2)
