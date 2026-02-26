# /usr/bin/env python

import time
from libTerm import Term
from libTerm.types import Mode
from libTerm.types.enums import StoreStop as Stop
from libTerm import Term
from libTerm.types import Mode
import time

from libTerm.types.enums import StoreStop
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

class Context:
	def __init__(s):
		s.term-None
		s.snake=None
		s.controls=None
		s.startup()
		s.keyseq=''
		s.end=False
		s.started=False


	def startup(s):
		# initialize terminal
		s.term=Term()
		s.term.echo = False
		s.term.cursor.hide()
		s.term.buffer.alternate()
		print('\x1b[J\x1b[1;1HPress one of up,down,left,right to start and  q to quit!')
		s.term.mode = Mode.CONTROL

		# initialize the Snake:
		s.snake=Snake(s.term)

class Snake:
	def __init__(s,t,speed=100):
		s.speed=1 / (speed or 1)
		s.term=t
		s.state=None
		s.pieces=['█','▄']
		s.tail=[]
		s.dir='C'
		s._task=None
		s._loop=None
		s._started=False
		s._moving=False

	def dead(s):
		current = snake.rempiece()
		if not current == StoreStop.FIRST_OF_STORE:
			s.term.cursor.quicksave()
			print(f'\x1b[{2};1H', repr(s.term.cursor.xy), end='', flush=True)
			s.term.cursor.quickload()
			time.sleep(snake.speed//2)
		return 'DEAD'

	@property
	def piece(s):
		if s.dir in 'AB':
			return s.pieces[0]
		elif s.dir in 'CD':
			return s.pieces[1]
		else:
			return ''

	def addpiece(s):
		print(f'\x1b[{s.dir}\x1b[D{s.piece}', end='', flush=True)
		no,coord=s.term.cursor.save()
		if coord not in s.tail:
			s.tail+=[coord]
		else:
			s.state=s.dead()

	def rempiece(s):
		current=s.term.cursor.undo()
		print('\x1b[D ', end='', flush=True)
		if s.term.cursor.store.stop==StoreStop.FIRST_OF_STORE:
			return StoreStop.FIRST_OF_STORE
		return current
	async def move(s):
		if s._started:
			while not s._end:
				s.addpiece()
				await asyncio.sleep(s.speed)
			s.cleanup()

	def start(s):
		if s.loop is None:
			s.loop=asyncio.new_event_loop()
			asyncio.set_event_loop(s.loop)
		s.loop=asyncio.get_running_loop()
		s.task=s.loop.create_task(s.move())
		s._started=True

class controls():
	def __init__(s,term):
		s.term=term



		rm.stdin.event:
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




