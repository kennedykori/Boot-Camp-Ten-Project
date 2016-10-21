from handler import Handler
from ..events.event import Event


class Timer_Handler(Handler):

	def __init__(self, timer_text_widget, app_main_loop):
		super(Timer_Handler, self).__init__()
		self.__timer_widget = timer_text_widget
		self.__main_loop = app_main_loop

	def handle_event(self, event):
		super(Timer_Handler, self).handle_event(event)

		#Working progress
		#print(event.get_new_timer().get_seg_time())
		self.__timer_widget.set_text(('I say', u"" + str(event.get_new_timer().get_seg_time_as_string())))
		self.__main_loop.draw_screen()
