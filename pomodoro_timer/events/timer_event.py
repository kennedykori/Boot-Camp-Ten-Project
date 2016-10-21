from event import Event


class Timer_Event(Event):

	def __init__(self, old_timer, new_timer):
		super(Timer_Event, self).__init__("Timer_Changed_Event")
		
		self.__old_timer = old_timer
		self.__new_timer = new_timer

	def get_old_timer(self):
		return self.__old_timer

	def get_new_timer(self):
		return self.__new_timer
