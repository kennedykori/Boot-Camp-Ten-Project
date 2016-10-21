#from abc import ABCMeta, abstractmethod
from ..handlers.handler import Handler
from ..events.event import Event


class Listener(object):

	#__metaclass__ = ABCMeta

	def __init__(self):
		super(Listener, self).__init__()
		self._handlers = []

	def register_handler(self, handler):
		if not(isinstance(handler, Handler)):
			raise ValueError("handler must be a sublclass of Handler.")
		self._handlers.append(handler)

	def fire_handlers(self, event):
		if not(isinstance(event, Event)):
			raise ValueError("event must be a sublclass of Event.")
		for handler in self._handlers:
			handler.handle_event(event)
