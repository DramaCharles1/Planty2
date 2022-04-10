#!/usr/bin/env python

#PlantyConnect
import serial
import serial.tools.list_ports
from datetime import datetime
from time import sleep
#PlantyCommands
from enum import Enum
from enum import IntEnum

class PlantyConnect:
	'''
	Port to access Arduino. Baudrate 57600 default. Delay in ms between send and recieve
	'''
	def __init__(self, port: str, baudrate: int, timeout: float):
		if port == "":
			try:
				self.port = self.__get_connected_port()
			except Exception as e:
				print(e) 
		else:
			self.port = port

		self.baudrate = baudrate
		self.ser = None
		self.read_timeout = timeout
		self.write_timeout = timeout

		try:
			self.ser = serial.Serial(self.port, self.baudrate, timeout=self.read_timeout,
			 write_timeout=self.write_timeout)
		except serial.SerialException as SerialEx:
			print(str(SerialEx))

		sleep(2)
		print(f"Connected to: {self.port}")

	def __get_connected_port(self):
		'''
		Get connected port from arduino if no port has been specified
		'''
		portlist = serial.tools.list_ports.comports(include_links=False)
		arduinoport = ""

		for port in portlist:
			if "Genuino" in port.description:
				arduinoport = port.device

		if arduinoport == "":
			raise Exception("Could not find any arduino")

		return arduinoport

	def close_port(self):
		'''
		Close serial port
		'''
		self.ser.flush()
		self.ser.close()

	def write(self, message: str):
		'''
		Write to serial port
		'''
		message = message + '\n'
		self.ser.write(message.encode('utf-8'))

	def read(self):
		'''
		read from serial port
		'''
		start = datetime.now()
		while (datetime.now() - start).total_seconds() < self.read_timeout:
			if self.ser.in_waiting > 0:
				while self.ser.in_waiting > 0:
					rec = self.ser.readline()
				return rec
			else:
				sleep(0.5)
		raise Exception("No incoming message")


class Temp_option(Enum):
	'''
	Temperature sensor options
	'''
	TEMP = 1
	HUMIDITY = 2


class Light_color_option(IntEnum):
	'''
	Light color option
	'''
	PURPLE = 1
	WHITE = 2
	RED = 3
	GREEN = 4
	BLUE = 5

MOIS_DELAY = 0.5 #s
MOIS_SAMPLES = 5

class PlantyCommands(PlantyConnect):
	'''
	Class with all commands
	'''
	def __init__(self, port="", baudrate=57600, timeout=MOIS_DELAY*(MOIS_SAMPLES + 1), delay=0.3):
		super().__init__(port, baudrate, timeout)
		self.delay = delay

	def __check_command(self, rec):
		'''
		Check command for correct format
		'''
		if "OK" in str(rec):
			return True
		elif "ERR" in str(rec):
			return False
		else:
			raise Exception("Not a valid command recieved" + "rec: " + rec)

	def __get_command_value(self, rec):
		'''
		Get command values
		'''
		separator = ['=',',','\n']
		rec = str(rec).replace('=',',')
		value = str(rec).split(',')

		return value[1]

	def __send_and_recieve(self, message: str):
		self.__send_message(message)
		sleep(self.delay)
		return self.__recieve_message()

	def __send_message(self, message: str):
		'''
		Send message to Planty
		'''
		print(f"send: {message}")
		self.write(message)

	def __recieve_message(self):
		'''
		Recieve message from Planty
		'''
		recieve = self.read()
		print(f"Recieve: {recieve}")

		if self.__check_command(recieve):
			return self.__get_command_value(recieve)
		else:
			raise Exception("Error when recieving message: " + str(recieve))

	def read_plant(self):
		'''
		Read what is planted
		'''
		command = "PLANT=1"
		return self.__send_and_recieve(command)
		#self.__send_message(command)
		#return self.__recieve_message()

	def writePlant(self, plant: str):
		'''
		Write what is planted
		'''
		command = f"PLANT=2,{plant}"
		return self.__send_and_recieve(command)

	def read_temp(self, temp_option: Temp_option):
		'''
		Read temperatue or humidity in house
		'''
		if temp_option == Temp_option.TEMP:
			command = "TEMP=1"
			return self.__send_and_recieve(command)

		elif temp_option == Temp_option.HUMIDITY:
			command = "TEMP=2"
			return self.__send_and_recieve(command)

		else:
			raise AttributeError("No valid temp sensor option")

	def read_moisture(self, samples=1):
		'''
		Read moisture sensor. Average value from n samples
		samples(int): number of samples
		'''
		command = f"MOIS={str(samples)}"
		return self.__send_and_recieve(command)

	def read_ALS(self):
		'''
		Read ALS
		'''
		command = "ALS"
		return self.__send_and_recieve(command)

	def start_pump(self, start: bool, power: int, duration: int):
		'''
		Start or stop pump
		start(bool): start or stop pump
		power(int): pump power in %
		duration(int): duration in ms
		'''
		if start:
			command = f"MOTR=1,{str(power)},{str(duration)}"
		else:
			command = f"MOTR=0,{str(power)},{str(duration)}"
		return self.__send_and_recieve(command)

	def lights(self, write: bool, color_option: Light_color_option, power: int):
		'''
		Set LED lights. 
		write(bool): read or write LED lights
		color_option(Light_color_option): choose color
		power(int): light power in %
		'''
		if write:
			command = f"LED=1,{str(int(color_option))},{str(power)}"
		else:
			command = "LED=2"
		return self.__send_and_recieve(command)

	def light_regulator_values(self, write: bool, kp: float, ki: float, t: int, max_signal: int):
		'''
		Set PI light regulator values
		write(bool): read or write regulator values
		kp(float): p part
		ki(float): i part
		t(int): integral time
		max_signal(int): maximum signal
		'''
		if write:
			command = f"PISET=2,{str(kp)},{str(ki)},{str(t)},{str(max_signal)}"
		else:
			command = "PISET=1"
		return self.__send_and_recieve(command)

	def start_light_regulator(self, start: bool, set_point: int):
		'''
		Start or stop light regulator
		start(bool): start or stop the light regulator
		set_point(int): light set point
		'''
		if start:
			command = f"PI=2,1,{str(set_point)}"
		else:
			command = "PI=2,0,0"
		return self.__send_and_recieve(command)
