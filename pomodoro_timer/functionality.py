from model.pomodoro_task import Pomodoro_Task
from model.pomodoro_timer import Pomodoro_Timer
from handlers.timer_handler import Timer_Handler
from handlers.timer_over_handler import Timer_Over_Handler, Custom_Timer_Over_Handler
from data import database


_current_task = None
_current_timer = None
_sound_enabled = True

def start_task(task_title, timer_widget, mainloop, pomodoros_widget, current_activity_widget):
	if _current_task is None:
		config = database.load_config()

		task = Pomodoro_Task(task_title)
		timer = Pomodoro_Timer(config["pomodoro_time"], True, True)
		task.start_task()
		timer.start_timer()
		
		#Create Event handlers
		timer_handler = Timer_Handler(timer_widget, mainloop)
		timer_over_handler = Timer_Over_Handler(enable_disable_sound=config["sound"])
		custom_timer_over_handler = Custom_Timer_Over_Handler(task, timer, config, timer_widget, mainloop, pomodoros_widget, current_activity_widget)

		#Register handlers
		timer.register_handler(timer_handler)
		timer.register_timer_over_handler(timer_over_handler)
		timer.register_timer_over_handler(custom_timer_over_handler)

		database.insert_new_task(task)
		global _current_task, _current_timer
		_current_task = task
		_current_timer = timer
		_sound_enabled = config["sound"]

		return 1
	else:
		return 0

def stop_task():
	#print("About to stop")
	global _current_timer, _current_task
	if _current_task is not None:
		_current_task.stop_task()
		_current_timer.stop_timer()
		database.set_task_stop_time(_current_task)
		database.set_no_of_cycles(_current_task)

	_current_timer = None
	_current_task = None

def config_duration(duration_for, duration):
	if duration_for == 1:
		database.config_pomodoro_time_duration(duration)
	elif duration_for == 2:
		database.config_short_break_duration(duration)
	elif duration_for == 3:
		database.config_long_break_duration(duration)

def config_sound(enable_disable):
	_sound_enabled = enable_disable
	database.config_sound(enable_disable)

def is_sound_enabled():
	return _sound_enabled

def list_all_tasks():
	return database.list_all_tasks()
	