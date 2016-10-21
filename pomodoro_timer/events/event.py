from abc import ABCMeta


class Event(object):
	"""docstring for Event"""

	__metaclass__ = ABCMeta
	
	def __init__(self, event_type = "UNKNOWN"):
		super(Event, self).__init__()
		if type(event_type) is not str:
			raise ValueError("event_type must be of type string.") 
		self.__type = event_type

	def get_event_type(self):
		return self.__type
