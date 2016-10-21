from ..events.event import Event
from abc import ABCMeta, abstractmethod


class Handler(object):

	__metaclass__ = ABCMeta

	def __init__(self):
		super(Handler, self).__init__()

	@abstractmethod
	def handle_event(self, event):
		if not(isinstance(event, Event)):
			raise ValueError("event has to be an instance of subclass of Event.")
	