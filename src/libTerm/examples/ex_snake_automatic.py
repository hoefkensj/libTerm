# /usr/bin/env python
from libTerm import Term,Coord,Mode
import time

from libTerm.types.enums import StoreStop


class Snake:
	def __init__(s,t,speed=100):
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
		if s.term.cursor.store.stop==StoreStop.FIRST_OF_STORE:
			return StoreStop.FIRST_OF_STORE
		return current

term=Term()
term.echo=False
term.cursor.show(False)
print('\n\n\n\n\n\n\n')
vert=term.size.height
cols=term.size.width
hor=cols//8
term.mode=Mode.CONTROL
term.buffer.alternate()

# time.sleep(5)
snake=Snake(term)
print('\x1b[J\x1b[1;1HPress one of up,down,left,right to start and  q to quit!')
seq=''
end=False
up = False
right = False
down = True
while True:
	if term.stdin.event:
		key=term.stdin.read()
		if key == 'q':
			seq += 'q'

	if not seq=='q':
		if term.cursor.xy.y>=5 and up:
			snake.dir='A'
			if term.cursor.xy.y==5:
				up=False
				right=True
		if term.cursor.xy.y<=vert and down:
			snake.dir='B'
			if term.cursor.xy.y==vert:
				down=False
				right=True
		if term.cursor.xy.x%hor>=0 and right:
			snake.dir='C'
			if term.cursor.xy.x%hor==0:
				right=False
				down=term.cursor.xy.y==5
				up=term.cursor.xy.y==vert
		if term.cursor.xy.x==term.size.width and term.cursor.xy.y==5:
			down=False
			up=False
			right=False
			seq+='q'

	elif seq=='q':
		current=snake.rempiece()
		if not current==StoreStop.FIRST_OF_STORE:
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
			time.sleep(snake.speed)

