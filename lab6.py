import pyb
from pyb import Pin, Timer, ADC, LED, DAC
from array import array
from oled_938 import OLED_938

import micropython
micropython.alloc_emergency_exception_buf(100)

oled = OLED_938(pinout={'sda': 'Y10', 'scl': 'Y9', 'res': 'Y8'}, height=64, external_vcc=False, i2c_devid=61)

oled.poweron()
oled.init_display()
oled.draw_text(0, 0, 'Basic Beat Detection')
oled.display()

mic = ADC(Pin('Y11'))
MIC_OFFSET = 1523
b_LED = LED(4)

N = 160
s_buf = array('H', 0 for i in range(N))
ptr = 0
buffer_full = False

def flash():
	b_LED.on()
	pyb.delay(20)
	b_LED.off()

def energy(buf):
	sum = 0
	for i in range(len(buf)):
		s = buf[i] - MIC_OFFSET
		sum = sum + s*s
	return sum

def isr_sampling(dummy):
	global pty
	global buffer_full

	s_buf[ptr] = mic.read()
	ptr += 1
	if (ptr == N):
		ptr = 0
		buffer_full = True

sample_timer = pyb.Timer(7, freq=8000)
sample_timer.callback(isr_sampling)

M = 50
BEAT_THRESHOLD = 2.0

e_ptr = 0
e_buf = array('L', 0 for i in range(M))
sum_energy = 0
tic = pyb.millis()

while True:
	if buffer_full:
		E = energy(s_buf)

		sum_energy = sum_energy - e_buf[e_ptr] + E
		e_buf[e_ptr] = E
		e_ptr = (e_ptr + 1) % M

		c = E * M / sum_energy

		if (pyb.millis() - tic > 500):
			if (c > BEAT_THRESHOLD):
				flash()
				tic = pyb.millis()
		buffer_full = False