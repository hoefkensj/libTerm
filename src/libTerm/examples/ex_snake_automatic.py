# /usr/bin/env python
import asyncio
import time

from libTerm import Mode
from libTerm.components.enums import StoreStop


class Example:
	def __init__(s):
		s.term=None
		s.snake=None
		s.controls=None
		s.cols=None
		s.hor=None
		s.vert=None
		s.seq=''
		s.up=False
		s.down=False
		s.right=False
		s.end=False
		s.loop = None
		s.task = None
		s._started = False
		s.startup()
		s.start()

	def startup(s):
		# initialize terminal
		s.term=Term()
		s.term.echo = False
		s.term.cursor.hide()
		s.term.mode=Mode.CONTROL
		s.term.buffer.alternate()
		s.cols=s.term.size.width
		s.hor=s.cols//8
		s.vert=s.term.size.rows
		s.right=True
		s.down=True
		# initialize the Snake:
		s.snake=Snake(s.term)

	def start(s):
		if s.loop is None:
			s.loop = asyncio.new_event_loop()
			asyncio.set_event_loop(s.loop)
		else:
			s.loop = asyncio.get_running_loop()
		s.task = s.loop.create_task(s.snake.move())
		s._started = True

	def input(s):
		while True:
			if s.term.stdin.event:
				key = s.term.stdin.read()
				if key == 'q':
					s.seq += 'q'
				else:
					s.snake.start()
			if not s.seq == 'q':
				if s.term.cursor.xy.y >= 5 and s.up:
					s.snake.dir = 'A'
					if s.term.cursor.xy.y == 5:
						s.up = False
						s.right = True
				if s.term.cursor.xy.y <= s.vert and s.down:
					s.snake.dir = 'B'
					if s.term.cursor.xy.y == s.vert:
						s.down = False
						s.right = True
				if s.term.cursor.xy.x % s.hor >= 0 and s.right:
					s.snake.dir = 'C'
					if s.term.cursor.xy.x % s.hor == 0:
						s.right = False
						s.down = s.term.cursor.xy.y == 5
						s.up = s.term.cursor.xy.y == s.vert
				if s.term.cursor.xy.x == s.term.size.width and s.term.cursor.xy.y == 5:
					s.down = False
					s.up = False
					s.right = False
					s.seq += 'q'
			elif s.seq == 'q':
				current = s.snake.rempiece()
				if not current == StoreStop.FIRST_OF_STORE:
					print(f'\x1b[s\x1b7\x1b[{2};1H', repr(s.term.cursor.xy), '\x1b[u\x1b8', end='', flush=True)
					time.sleep(s.snake.speed)

				else:
					s.end = True
			elif s.seq == 'qq' or s.end:
				s.term.sync.default()
				break
			else:
				if s.snake.piece != '' and not 'q' in s.seq:
					s.snake.addpiece()
					time.sleep(s.snake.speed)


class Snake:
	def __init__(s,t,speed=100):
		s.state=None
		s.speed=1 / (speed or 1)
		s.term=t
		s.pieces=['█','▄']
		s.tail=[]
		s.task=None
		s.loop=None
		s.dir='B'
		s._started=False
		s._moving=False
		s._end=False

	def dead(s):
		current = s.rempiece()
		if not current == StoreStop.FIRST_OF_STORE:
			print(f'\x1b[s\x1b7\x1b[{2};1H', repr(s.term.cursor.xy), '\x1b[u\x1b8', end='', flush=True)
			time.sleep(s.speed)
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
		print(f'\x1b[{s.dir}{s.piece}', end='', flush=True)
		pair=s.term.cursor.save()
		no,coord=list(*pair.items())
		if coord not in s.tail:
			s.tail+=[coord]
		else:
			s.state=s.dead()

	def rempiece(s):
		current=s.term.cursor.undo()
		print('\x1b[D ', end='', flush=True)
		if s.term.cursor._coordstore.stop==StoreStop.FIRST_OF_STORE:
			return StoreStop.FIRST_OF_STORE
		return current
	async def move(s):
		if s._started:
			while not s._end:
				s.addpiece()
				await asyncio.sleep(s.speed)
			s.cleanup()




def main(term):
	ex = Example()
	ex.start()


if __name__ == '__main__':
	import atexit
	from libTerm import Term
	def ExitProcedure(t):
		t.ANSI.cls()
		t.mode = t.MODE.DEFAULT
		t.buffer = t.BUFFER.DEFAULT
	t=Term()
	t.mode=t.MODE.CONTROL
	t.buffer = t.BUFFER.ALTERNATE
	t.ANSI.cls()
	atexit.register(ExitProcedure,t)
	main(t)

# time.sleep(5)


