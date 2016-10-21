__commands = [["pomodoro", "start"], 
		["pomodoro", "config", "time"],
		["pomodoro", "config", "short_break"],
		["pomodoro", "config", "long_break"],
		["pomodoro", "config", "sound"],
		["pomodoro", "stop"],
		["pomodoro", "list"]]

def __words(data):
	if type(data) is not str:
		raise ValueError("Input provided must be a string.")
	
	l_data = data.split() 					#Split the string and store the resulting list in l_data.
	
	output = []         					#The dict where the out put is stored.
	for word in l_data:
		try:
			word = float(word)
		except ValueError:
			pass

		output.append(word)

	return output

def parse_command(command):
	command = __words(command)
	action = {}

	for index in xrange(len(__commands)):
		temp_command = command[:len(__commands[index])]
		if temp_command == __commands[index]:
			return __process_command(index, command)

	return {-1: "Unknown command, type help to get a list of valid commands."}

def __process_command(index, command):
	if index == 0:
		args = command[len(__commands[index]):]
		if len(args) == 0:
			return {-2: "You need to provide the title of the task."}
		if len(args) > 1:
			return {index: ' '.join(args)}
		else:
			return {index: args[0]}
	elif index == 1 or index == 2 or index == 3:
		args = command[len(__commands[index]):]
		if len(args) == 0:
			return {-2: "You need to provide the time in minutes of the task."}
		elif not(type(args[0]) is int or type(args[0]) is float):
			return {-2: "duration should be a numeric value."}
		return {index: args[0]}
	elif index == 4:
		args = command[len(__commands[index]):]
		if len(args) == 0:
			return {-2: "You need to provide on or off for config sound."}
		elif not(args[0] == "on" or args[0] == "off"):
			return {-2: "You need to provide on or off for config sound."}
		return {index: args[0]}

	else:
		return {index: "valid"}
