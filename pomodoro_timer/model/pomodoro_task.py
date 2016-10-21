from datetime import datetime


class Pomodoro_Task(object):
	"""docstring for Pomodoro_Taskk"""
	
	def __init__(self, title, start_time = None, stop_time = None, cycles = 1):
		super(Pomodoro_Task, self).__init__()
		if type(title) is not str:
			raise ValueError("title should be a string.")
		if  not(start_time is None) and not(isinstance(start_time, datetime)):
			raise ValueError("start_time should be an instance of datetime.")
		if  not(stop_time is None) and not(isinstance(stop_time, datetime)):
			raise ValueError("stop_time should be an instance of datetime.")
		if type(cycles) is not int:
			raise ValueError("cycles should be an integer.")
		self.__title = title
		self.__start_time = start_time
		self.__stop_time = stop_time
		self.__no_of_pomodoro_cycles = cycles

	def start_task(self):
		self.__start_time = datetime.now()

	def stop_task(self):
		self.__stop_time = datetime.now()

	def increament_no_of_cycles_by_one(self):
		self.__no_of_pomodoro_cycles += 1

	def increament_no_of_cycles(self, cycles):
		if type(cycles) is not int:
			raise ValueError("cycles must be an integer greater than or equal to zero.")
		elif cycles < 0:
			raise ValueError("cycles must be an integer greater than or equal to zero.")

		self.__no_of_pomodoro_cycles += cycles

	def __format_date_time(self, date_time):
		if date_time is None:
			return "" 
		return date_time.strftime("%A %d %B %Y %H:%M:%S")

	def get_title(self):
		return self.__title

	def get_start_time(self):
		return self.__start_time

	def get_start_time_formated(self):
		return str(self.__format_date_time(self.__start_time))

	def get_stop_time(self):
		return self.__stop_time

	def get_stop_time_formated(self):
		return str(self.__format_date_time(self.__stop_time))

	def get_no_of_cycles(self):
		return self.__no_of_pomodoro_cycles

	def __str__(self):
		return "Task : " + self.__title + "\n" + "\t" + "Start Time : " + self.__format_date_time(self.__start_time) + "\n" + "\t" + "Stop Time : " + self.__format_date_time(self.__stop_time) + "\n" + "\t" + "# of Cycles : " + str(self.__no_of_pomodoro_cycles)

