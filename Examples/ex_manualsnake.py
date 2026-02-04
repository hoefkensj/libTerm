# /usr/bin/env python

import time
from libTerm import Term, Mode
from libTerm import Coord, Color

class Snake:
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
term.mode=Mode.CONTROL
term.buffer.switch()


# time.sleep(5)
snake=Snake(term)
print('\x1b[J\x1b[1;1HPress one of up,down,left,right to start and  q to quit!')
while True:
	if term.stdin.event:
		key=term.stdin.read()
		if key=='\x1b[A':
			snake.piece='\x1b[A\x1b[D░'
		elif key=="\x1b[B":
			snake.piece='\x1b[B\x1b[D░'
		elif key=='\x1b[C':
			snake.piece='░'
		elif key=='\x1b[D':
			snake.piece = '\x1b[D\x1b[D░'
		elif key=='q':
			while term.cursor.store.selected:
				snake.rempiece()
				print(f'\x1b[s\x1b7\x1b[{2};1H', repr(term.cursor.xy), '\x1b[u\x1b8', end='', flush=True)

				time.sleep(snake.speed)
			break
	if snake.piece!='':
		snake.addpiece()
	print(f'\x1b[s\x1b7\x1b[{2};1H',repr(term.cursor.xy),'\x1b[u\x1b8',end='',flush=True)

	time.sleep(snake.speed)



term.buffer.default()
