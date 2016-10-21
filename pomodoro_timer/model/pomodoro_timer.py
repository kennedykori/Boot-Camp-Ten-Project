import time
import threading
from ..events.timer_event import Timer_Event
from ..events.timer_over_event import Timer_Over_Event
from ..handlers.handler import Handler
from ..listeners.listener import Listener


class Pomodoro_Timer(object):

	def __init__(self, max_time, reverse=False, enable_threading=False): #max_time is in secs
		super(Pomodoro_Timer, self).__init__()
		if not(type(max_time) is int or type(max_time) is float):
			raise ValueError("max_time should be numeric and greater or equal to zero.")
		elif type < 0:
			raise ValueError("max_time should be numeric and greater or equal to zero.")

		if type(reverse) is not bool:
			raise ValueError("reverse should be a boolean value.")
		if type(enable_threading) is not bool:
			raise ValueError("enable_threading should be a boolean value.")

		self.__reverse = reverse
		self.__threading = enable_threading
		self.__max_time = max_time
		self._stop = False
		self._listener = Listener()
		self._timer_over_listener = Listener()
		if reverse:
			self._total_secs = max_time
		else:
			self._total_secs = 0

	def start_timer(self):
		if self.__threading:
			timer_thread = _Timer_Thread(self)
			timer_thread.start()
		else:
			self._stop = False
			if self.__reverse:
				self._total_secs = self.__max_time
				while self._total_secs > 0 and not(self._stop):
					time.sleep(1)
					self._total_secs -= 1
					self._fire_handlers()
					#print "Total Sec", self._total_secs
			else:
				self._total_secs = 0
				while self._total_secs < self.__max_time and not(self._stop):
					time.sleep(1)
					self._total_secs += 1
					self._fire_handlers()
					#print "Total Sec", self._total_secs
			self.stop_timer()
			self._fire_timer_over_handelers()

	def stop_timer(self):
		if self.__threading:
			threadLock = threading.Lock()
			threadLock.acquire()
			self._stop = True
			threadLock.release()
		else:
			self._stop = True

	def reset_timer(self, max_time=None):
		if max_time is not None:
			self.__max_time = max_time
		if self.__threading:
			threadLock = threading.Lock()
			threadLock.acquire()
			if self.__reverse:
				self.__total_secs = self.__max_time
			else:
				self.__total_secs = 0
			threadLock.release()
		else:	
			if self.__reverse:
				self.__total_secs = self.__max_time
			else:
				self.__total_secs = 0

	def _fire_handlers(self):
		timer_event = Timer_Event(None, self)
		self._listener.fire_handlers(timer_event)

	def _fire_timer_over_handelers(self):
		timer_over_event = Timer_Over_Event(self)
		self._timer_over_listener.fire_handlers(timer_over_event)

	def register_handler(self, handler):
		self._listener.register_handler(handler)

	def register_timer_over_handler(self, handler):
		self._timer_over_listener.register_handler(handler)

	def get_total_sec(self):
		return self._total_secs

	def is_reverse(self):
		return self.__reverse

	def get_max_time(self):
		return self.__max_time

	def is_threading(self):
		return self.__threading

	def is_stoped(self):
		return self._stop

	#segmented time
	def get_seg_time(self):
		secs = self._total_secs % 60
		hours = (self._total_secs // 60) // 60
		minutes = self._total_secs // 60
		if minutes > 59:
			minutes = (minutes // 60) % 60
		
		return {"hours" : int(hours), "minutes" : int(minutes), "seconds" : int(secs)}

	def get_seg_time_as_string(self):
		seg_time = self.get_seg_time()
		hours = str(seg_time["hours"]) if seg_time["hours"]>9 else "0" + str(seg_time["hours"])
		minutes = str(seg_time["minutes"]) if seg_time["minutes"]>9 else "0" + str(seg_time["minutes"])
		seconds = str(seg_time["seconds"]) if seg_time["seconds"]>9 else "0" + str(seg_time["seconds"])

		return hours + ":" + minutes + ":" + seconds


class _Timer_Thread(threading.Thread):

	def __init__(self, pomodoro_timer):
		super(_Timer_Thread, self).__init__()
		self.__timer = pomodoro_timer

	def run(self):
		threadLock = threading.Lock()
		threadLock.acquire()
		self.__timer._stop = False
		threadLock.release()
		if self.__timer.is_reverse():
			self.__timer._total_secs = self.__timer.get_max_time()
			while self.__timer._total_secs > 0:
				threadLock.acquire()
				if self.__timer.is_stoped():
					break
				threadLock.release()
				time.sleep(1)
				self.__timer._total_secs -= 1
				self.__timer._fire_handlers()
		else:
			self.__timer._total_secs = 0
			while self.__timer._total_secs < self.__timer.get_max_time():
				threadLock.acquire()
				if self.__timer.is_stoped():
					break
				threadLock.release()
				time.sleep(1)
				self.__timer._total_secs += 1
				self.__timer._fire_handlers()
		self.__timer.stop_timer()
		self.__timer._fire_timer_over_handelers()
