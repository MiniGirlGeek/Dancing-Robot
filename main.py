import move
from ws2812 import WS2812
import pyb
from math import cos, pi
from pyb import Pin, Timer, ADC, UART

robot = move.Robot()
task1 = task_one.Mode(robot)
task2 = task_two.Mode()
release = release.Mode()

key = (0, 1, 2, 3, 'U', 'D', 'L', 'R')
instruction = {"U": robot.moveForwards, "D": robot.moveBackwards, "L": robot.rotateLeft, "R": robot.rotateRight}
uart = UART(6)
uart.init(9600, bits = 8, parity = None, stop = 2)
key_press = None

i = 0

def rgb(i):
	return ((cos(i)+1)*80, (cos(i + 2/3*pi)+1)*80, (cos(i + 4/3*pi)+1)*80)

while True:
	i += 0.1
	if uart.any() >= 5:
		command = uart.read(5)
		print(command)
		key_index = command[2] - ord('1')
		if 0 <= key_index <= 7:
			key_press = key[key_index]
		
		if (command[3] == ord("1")) and (key_press in key[4:]):
			print('press')
			instruction[key_press]()
		else:
			print('release')
			robot.stop()

		if key_press in key[:3]:
			mode = modes[key_press]
		print("You've selected: ", str(key_press))