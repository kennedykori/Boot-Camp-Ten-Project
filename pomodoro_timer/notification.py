import os
import subprocess
from threading import Thread

def sound_notification():
	play_notif = Thread(target=__play)
	play_notif.run()

def __play():
	bell = os.path.realpath('pomodoro_timer/resources/Ding_Dong.mp3')
	FNULL = open(os.devnull, 'w')
	subprocess.call(['play', bell], stdout=FNULL, stderr=subprocess.STDOUT)
