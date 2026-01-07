# /usr/bin/env pyhthon

import time
from libTerm import Term
from libTerm import Coord,Mode,Color

class Snake():
	def __init__(s,t,speed=10):
		s.speed=1 / (speed or 1)
		s.term=t
		s.piece=''

	def addpiece(s):
		print(s.piece, end='', flush=True)
		s.term.cursor.save()

	def rempiece(s):
		s.term.cursor.undo()
		print('\x1b[D ', end='', flush=True)

term=Term()
term.mode(Mode.CONTROL)
snake=Snake(term)
print('\x1b[J\x1b[1;1HPress Q to quit!')
while True:
	if term.stdin.event:
		key=term.stdin.read()
		# print('\x1b[3;1HKey:\x1b[32m {KEY}\x1b[m'.format(KEY=key),end='',flush=True)

		if key=='w':
			snake.piece='\x1b[A\x1b[D░'
		elif key=="s":
			snake.piece='\x1b[B\x1b[D░'
		elif key=='d':
			snake.piece='░'
		elif key=='a':
			snake.piece = '\x1b[D\x1b[D░'
		elif key=='q':
			while term.cursor.store.selected:
				snake.rempiece()
				time.sleep(snake.speed)
			break
	if snake.piece!='':
		snake.addpiece()
	time.sleep(snake.speed)
