# /usr/bin/env python

import time
from libTerm import Term, Mode, Color, Coord
from libTerm.types.enums import StoreStop as Stop

class Snake:
	def __init__(s,t,speed=10):
		s.speed=1 / (speed or 1)
		s.term=t
		s.piece='█'
		s.dir='C'
	def addpiece(s):
		print(f'\x1b[{s.dir}\x1b[D{s.piece}', end='', flush=True)
		s.term.cursor.save()

	def rempiece(s):
		current=s.term.cursor.undo()
		print('\x1b[D ', end='', flush=True)
		if s.term.cursor.store.stop==Stop.FIRST_OF_STORE:
			return Stop.FIRST_OF_STORE
		return current


term=Term()
term.mode=Mode.CONTROL
term.buffer.switch()


# time.sleep(5)
snake=Snake(term)
print('\x1b[J\x1b[1;1HPress one of up,down,left,right to start and  q to quit!')
seq=''
end=False
while True:
	if term.stdin.event:
		key=term.stdin.read()
		if not seq=='q':
			if key=='\x1b[A':
				snake.dir='A'
			elif key=="\x1b[B":
				snake.dir='B'
			elif key=='\x1b[C':
				snake.dir='C'
			elif key=='\x1b[D':
				snake.dir='D'
			elif key=='q':
				seq+='q'

	elif seq=='q':
		current=snake.rempiece()
		if not current==Stop.FIRST_OF_STORE:
			print(f'\x1b[s\x1b7\x1b[{2};1H', repr(term.cursor.xy), '\x1b[u\x1b8', end='', flush=True)
			time.sleep(snake.speed)

		else:
			end=True
	if seq=='qq' or end:
		term.buffer.default()
		exit()
	else:
		if snake.piece != '' and not 'q'in seq:
			snake.addpiece()

	print(f'\x1b[s\x1b7\x1b[{2};1H',repr(term.cursor.xy),'\x1b[u\x1b8',end='',flush=True)

	time.sleep(snake.speed)




