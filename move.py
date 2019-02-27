import pyb
from pyb import Pin, Timer, ADC

class Motor:
	def __init__(self, out1, out2, pwm, chan, tim):
		self.o1 = Pin(out1, Pin.OUT_PP)
		self.o2 = Pin(out2, Pin.OUT_PP)
		self.pwm = Pin(pwm)
		self.ch = tim.channel(chan, Timer.PWM, pin = self.pwm)
		self.speed = 50

	def forward(self):
		self.o1.high()
		self.o2.low()
		self.ch.pulse_width_percent(self.speed)

	def stop(self):
		self.o1.low()
		self.o2.low()
		self.ch.pulse_width_percent(0)

	def backward(self):
		self.o1.low()
		self.o2.high()
		self.ch.pulse_width_percent(self.speed)

class Robot():
	def __init__(self):
		self.tim = Timer(2, freq = 1000)

		self.A1     = 'X7'
		self.A2     = 'X8'
		self.PWMA   = 'X2'
		self.chanA  = 2
		self.motorA = Motor(self.A1, self.A2, self.PWMA, self.chanA, self.tim)

		self.B1     = 'X4'
		self.B2     = 'X3'
		self.PWMB   = 'X1'
		self.chanB  = 1
		self.motorB = Motor(self.B1, self.B2, self.PWMB, self.chanB, self.tim)

		self.speed = 50

		self.ROTATION_SPEED = 50

		self.pot = ADC(Pin('X11'))

	def moveForwards(self):
		self.motorA.forward()
		self.motorB.forward()

	def moveBackwards(self):
		self.motorA.backward()
		self.motorB.backward()

	def stop(self):
		self.motorA.stop()
		self.motorB.stop()

	def changeSpeed(self, s):
		self.motorA.speed = s
		self.motorB.speed = s

	def updateSpeed(self):
		self.s = (self.pot.read() / 4095) * 100
		self.changeSpeed(self.s)

	def rotateLeft(self):
		self.changeSpeed(self.ROTATION_SPEED)
		self.motorA.backward()
		self.motorB.forward()

	def rotateRight(self):
		self.changeSpeed(self.ROTATION_SPEED)
		self.motorA.forward()
		self.motorB.backward()