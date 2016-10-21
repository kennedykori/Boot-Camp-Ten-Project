from handler import Handler
from ..events.event import Event
from ..notification import sound_notification

class Timer_Over_Handler(Handler):

	def __init__(self, timer_text_widget=None, app_main_loop=None, enable_disable_sound=True):
		super(Timer_Over_Handler, self).__init__()
		self.__timer_widget = timer_text_widget
		self.__main_loop = app_main_loop
		self.__enable_disable = enable_disable_sound

	def handle_event(self, event):
		super(Timer_Over_Handler, self).handle_event(event)
		if self.__enable_disable:
			sound_notification()

class Custom_Timer_Over_Handler(Timer_Over_Handler):

	def __init__(self, task, timer, config, timer_text_widget, app_main_loop, pomodoros_widget, current_activity_widget):
		super(Custom_Timer_Over_Handler, self).__init__(timer_text_widget, app_main_loop)
		self.__task = task
		self.__timer = timer
		self.__config = config
		self.__pomodoros = pomodoros_widget
		self.__current_activity = current_activity_widget

	def handle_event(self, event):
		if self.__task.get_stop_time() is not None:
			return

		config = self.__config
		if self.__timer.get_max_time() == config["pomodoro_time"]:
			self.__timer.reset_timer(config["short_break"])
			self.__current_activity.set_text(u"Activity : " + "Short break")
			self.__timer.start_timer()
			return
		elif self.__timer.get_max_time() == config["short_break"]:
			if ((self.__task.get_no_of_cycles() / 4.0 )+ 1).is_integer():
				self.__timer.reset_timer(config["long_break"])
				self.__current_activity.set_text(u"Activity : " + "Long break")
				self.__timer.start_timer()
				return
			else:
				self.__timer.reset_timer(config["pomodoro_time"])
				self.__current_activity.set_text(u"Activity : " + "Pomodoro")
				self.__timer.start_timer()
		else:
			self.__timer.reset_timer(config["pomodoro_time"])
			self.__current_activity.set_text(u"Activity : " + "Pomodoro")
			self.__timer.start_timer()

		self.__task.increament_no_of_cycles_by_one()
		self.__pomodoros.set_text(u"Pomodoros : " + str(self.__task.get_no_of_cycles()))
