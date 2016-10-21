import urwid
from pyfiglet import Figlet
from colorama import init, Fore, Back, Style
from pomodoro_timer.model.pomodoro_timer import Pomodoro_Timer
from pomodoro_timer.handlers.timer_handler import Timer_Handler
from pomodoro_timer.handlers.timer_over_handler import Timer_Over_Handler
from pomodoro_timer.events.event import Event
from pomodoro_timer.events.timer_event import Timer_Event
from pomodoro_timer import functionality
from pomodoro_timer import commands

def on_exit_clicked(exit_button):
	raise urwid.ExitMainLoop()

def on_start_clicked(start_button):
	title = "New Task" if len(commands_input.edit_text) == 0 else str(commands_input.edit_text)
	functionality.start_task(title, timer_widget, mainloop)

def on_stop_clicked(exit_button):
	functionality.stop_task()

def update_on_content(input):
	if input != 'enter':
		return
	input_txt = str(commands_input.edit_text)
	commands_input.set_edit_text('')

	if input_txt == "help":
		show_help()
		return

	focus_widget, position = listbox.get_focus()
	content.append(urwid.Text(('I say', u"" + input_txt)))
	listbox.set_focus(position + 1)
	if process_command(input_txt) == 1:
		append_txt("\tOK")
	else:
		append_txt("\tNOT OK")

def append_txt(txt):
	focus_widget, position = listbox.get_focus()
	content.append(urwid.Text(u"" + txt))
	listbox.set_focus(position + 1)

def process_command(command):
	output = commands.parse_command(command)
	for k,v in output.items():
		if k == 0:
			functionality.start_task(v, timer_widget, mainloop, pomodoros_widget, current_activity_widget)
			task_name_widget.set_text(u"Task : " + v)
			current_activity_widget.set_text(u"Activity : " + "Pomodoro")
			pomodoros_widget.set_text(u"Pomodoros : " + "1")
			return 1
		elif k == 1 or k == 2 or k == 3:
			functionality.config_duration(k, v)
			return 1
		elif k == 4:
			functionality.config_sound(True if v == "on" else False)
			return 1
		elif k == 5:
			functionality.stop_task()
			task_name_widget.set_text(u"Task : ")
			timer_widget.set_text(u"00:00:00")
			current_activity_widget.set_text(u"Activity : ")
			pomodoros_widget.set_text(u"Pomodoros : ")
			return 1
		elif k == 6:
			data = functionality.list_all_tasks()
			for task in data:
				append_txt(".   " + "Title: " + str(task.get_title()) + "              Stared: " + task.get_start_time_formated() + "  Stopped: " + task.get_stop_time_formated() + "  Cycles: " + str(task.get_no_of_cycles()))

			return 1
		else:
			pass

		return 0

def show_help():
	append_txt("Usage:")
	append_txt("   " + "pomodoro start <task_title>...")
	append_txt("   " + "pomodoro config time <duration-in-minutes>")
	append_txt("   " + "pomodoro config short_break <duration-in-minutes>")
	append_txt("   " + "pomodoro config long_break <duration-in-minutes>")
	append_txt("   " + "pomodoro config sound (off|on)")
	append_txt("   " + "pomodoro stop")
	append_txt("   " + "pomodoro list")

if __name__ == "__main__":
	#print "Starting the scipt."
	figlet = Figlet(font='3-d')
	global timer_widget, commands_input, mainloop, content, task_name_widget, current_activity_widget, pomodoros_widget, listbox, palette

	palette = [('I say', 'default,bold', 'default', 'bold'), ('banner', 'black', 'light gray'),
    		('My red', 'black', 'dark red'),
    		('My Blue', 'black', 'dark blue'),]

	welcome_widget = urwid.Text(('I say', u"Welcome to Pomodoro Timer.\n" + str(figlet.renderText("Pomodoro Timer"))))
	task_name_widget = urwid.Text(u"Task :")
	timer_widget = urwid.Text(u"00:00:00")
	current_activity_widget = urwid.Text(u"Activity : ")
	pomodoros_widget = urwid.Text(u"Pomodoros : ")
	commands_input = urwid.Edit(u"Type your commands here.(Click here to type and type help for a list of available commands).\n")
	start_button = urwid.Button(u'Start')
	stop_button = urwid.Button(u'Stop')
	exit_button = urwid.Button(u'Exit')
	content = urwid.SimpleListWalker([urwid.Text(u"")])
	listbox = urwid.ListBox(content)
	divider = urwid.Divider("-")
	pile = urwid.Pile([welcome_widget, divider, urwid.Columns([task_name_widget, timer_widget, current_activity_widget, pomodoros_widget]), divider, urwid.BoxAdapter(listbox, 10), divider, commands_input, divider, exit_button])
	filler = urwid.Filler(pile, valign='top')

	urwid.connect_signal(start_button, 'click', on_start_clicked)
	urwid.connect_signal(stop_button, 'click', on_stop_clicked)
	urwid.connect_signal(exit_button, 'click', on_exit_clicked)
	mainloop = urwid.MainLoop(filler, palette, unhandled_input=update_on_content)

	mainloop.run()
