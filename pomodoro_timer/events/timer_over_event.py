from event import Event


class Timer_Over_Event(Event):

	def __init__(self, timer):
		super(Timer_Over_Event, self).__init__("Timer_Over_Event")
		self.__timer = timer

	def get_timer(self):
		return self.__timer

