import sqlite3
import os
from ..model.pomodoro_task import Pomodoro_Task


def connect_to_db():
	global conn, cursor
	db = os.path.realpath('pomodoro_timer/data/db/pomodoro.db')
	conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
	cursor = conn.cursor()
	conn.commit()

def create_tasks_table_if_absent():
	cursor.execute("CREATE TABLE IF NOT EXISTS tasks (title text NOT NULL, start timestamp NOT NULL, stop timestamp, pomodoro_cycles integer DEFAULT 0, primary key(title, start))")
	conn.commit()

def create_config_table_if_absent():
	cursor.execute("CREATE TABLE IF NOT EXISTS config (sound boolean, long_break real, short_break real, pomodoro_time real)")
	conn.commit()

def insert_new_task(task):
	if not(isinstance(task, Pomodoro_Task)):
		raise ValueError("task should be an instance of Pomodoro_Task")
	if task.get_start_time() is None:
		raise ValueError("start time of task shouldn't be None")
	cursor.execute("INSERT INTO tasks (title, start, stop) VALUES (?,?,?)", (task.get_title(), task.get_start_time(), task.get_stop_time()))
	conn.commit()

def set_no_of_cycles(task):
	if not(isinstance(task, Pomodoro_Task)):
		raise ValueError("task should be an instance of Pomodoro_Task")
	cursor.execute("UPDATE tasks SET pomodoro_cycles=? WHERE title=? AND start=?", (task.get_no_of_cycles(), task.get_title(), task.get_start_time()))
	conn.commit()

def set_task_stop_time(task):
	if not(isinstance(task, Pomodoro_Task)):
		raise ValueError("task should be an instance of Pomodoro_Task")
	if task.get_stop_time() is None:
		raise ValueError("stop time of task shouldn't be None")
	cursor.execute("UPDATE tasks SET stop=? WHERE title=? AND start=?", (task.get_stop_time(), task.get_title(), task.get_start_time()))
	conn.commit()

def list_all_tasks():
	tasks = []
	cursor.execute('SELECT title, start as "[timestamp]", stop as "[timestamp]", pomodoro_cycles FROM tasks')
	for row in cursor:
		task = Pomodoro_Task(str(row[0]), row[1], row[2], int(row[3]))
		tasks.append(task)

	return tasks


def config_sound(enable_disable):
	if type(enable_disable) is not bool:
		raise ValueError("This function only accepts a boolean value as its argument.")
	cursor.execute("UPDATE config SET sound=?", (enable_disable,))
	conn.commit()

def config_long_break_duration(duration):
	if not(type(duration) is float or type(duration) is int):
		raise ValueError("duration has to be a numeric value greater than 0")
	if duration < 0:
		raise ValueError("duration has to be a numeric value greater than 0")
	cursor.execute("UPDATE config SET long_break=?", (duration,))
	conn.commit()

def config_short_break_duration(duration):
	if not(type(duration) is float or type(duration) is int):
		raise ValueError("duration has to be a numeric value greater than 0")
	if duration < 0:
		raise ValueError("duration has to be a numeric value greater than 0")
	cursor.execute("UPDATE config SET short_break=?", (duration,))
	conn.commit()

def config_pomodoro_time_duration(duration):
	if not(type(duration) is float or type(duration) is int):
		raise ValueError("duration has to be a numeric value greater than 0")
	if duration < 0:
		raise ValueError("duration has to be a numeric value greater than 0")
	cursor.execute("UPDATE config SET pomodoro_time=?", (duration,))
	conn.commit()

def config_duration(duration, duration_for):
	if not(type(duration) is float or type(duration) is int):
		raise ValueError("duration has to be a numeric value greater than 0")
	if duration < 0:
		raise ValueError("duration has to be a numeric value greater than 0")
	if duration_for == "short_break":
		cursor.execute("UPDATE config SET short_break=?", (duration,))
	elif duration_for == "long_break":
		cursor.execute("UPDATE config SET long_break=?", (duration,))
	else:
		cursor.execute("UPDATE config SET pomodoro_time=?", (duration,))

	conn.commit()


def close_connection():
	conn.commit()
	conn.close()

def config_default():
	cursor.execute("SELECT count(*) FROM config")
	if cursor.fetchone()[0] == 0:
		cursor.execute("INSERT INTO config VALUES (?,?,?,?)", (True, 15, 5, 25))
	else:
		cursor.execute("UPDATE config SET sound=?, short_break=?, long_break=?, pomodoro_time=?", (True, 5, 15, 25))
	conn.commit()

def load_config():
	cursor = conn.execute("SELECT * FROM config")
	for row in cursor:
		return {"sound" : row[0], "short_break": row[2] * 60, "long_break" : row[1] * 60, "pomodoro_time" : row[3] * 60}
	
	return {"sound" : True, "short_break" : 5 * 60, "long_break" : 15 * 60, "pomodoro_time" : 25 * 60}

def _init_module():
	connect_to_db()
	create_tasks_table_if_absent()
	create_config_table_if_absent()
	config_default()

# Initialize this module
_init_module()
