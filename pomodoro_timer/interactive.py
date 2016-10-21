"""
Pomodoro Timer

Usage:
	pomodoro_main
	pomodoro_main pomodoro start <task_title>...
	pomodoro_main pomodoro config time <duration-in-minutes>
	pomodoro_main pomodoro config short_break <duration-in-minutes>
	pomodoro_main pomodoro config long_break <duration-in-minutes>
	pomodoro_main pomodoro config sound (off|on)
	pomodoro_main pomodoro stop
	pomodoro_main pomodoro list

"""

import cmd
import sys
from docopt import docopt, DocoptExit


def docopt_cmd(func):
	print("Dec")

	def fn(self, arg):
		print("fn")
		try:
			opt = docopt(fn.__doc__, arg)
		except DocoptExit as e:
			print("Invalid Comamand!")
			print(e)
			return
		except SystemExit:
			return

		return func(self, opt)

	fn.__name__ = func.__name__
	fn.__doc__ = func.__doc__
	fn.__dict__.update(func.__dict__)

	return fn

def go_interactive():
	global opt
	opt = docopt(__doc__)
	print(opt)
	return
	try:
		Pomodoro_Interactive().cmdloop()
	except SystemExit:
		pass
	except KeyboardInterrupt:
		pass

class Pomodoro_Interactive(cmd.Cmd):
	intro = "Welcome to my pomodoro timer! (type help for a list of commands.)"
	prompt = "pm_timer :- "
	file = None

	#@docopt_cmd
	def do_start_task(self,arg):
		"""Usage: pomodoro start <task_title>..."""
		
		print("do start")
		doc = self.do_start_task.__doc__ 
		try:
			opt = docopt(doc,arg)
		except:
			print(opt)

		return
            
        #print(opt)

	#@docopt_cmd
	def do_config_time(self, arg):
		"""Usage: pomodoro config_time <duration-in-secs>"""
		
		print(arg)
