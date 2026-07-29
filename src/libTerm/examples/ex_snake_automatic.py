# /usr/bin/env python
import asyncio
import time

from libTerm import Mode
from libTerm.components.enums import StoreStop


class Context:
	def __init__(s,term,snakespeed=1000):
		s.term=term
		s.speed=snakespeed
		s.keyseq=''
		s.end=False
		s.started=False
		s.snake=None
		s.loop=None
		s.growsnake=None
		s.makeloop()
		s.initsnake()
		s.addcontol()

	def controls(s):
		def qq():
			s.keyseq += 'q'
			if s.keyseq == 'qq':
				s.end()


		key = s.term.tty.input.read()
		if key == 'q':
			qq()
			s.snake.die()
		ctrlmapping = {
			'\x1b[A': s.snake.up,
			'\x1b[B': s.snake.down,
			'\x1b[D': s.snake.left,
			'\x1b[C': s.snake.right,
		}
		action = ctrlmapping.get(key, lambda: None)
		action()


	def makeloop(s):
		s.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(s.loop)

	def addcontol(s):
		s.loop.add_reader(s.term.tty.input.fd, s.controls)

	def initsnake(s):
		s.snake=Snake(s, s.term, s.speed)
		s.growsnake = s.loop.create_task(s.snake.grow())

	def play(s):
		s.loop.run_forever()

	def end(s):
		s.loop.stop()

class Snake:
	def __init__(s,ctx,term,speed=1000):
		s.ctx=ctx
		s.term=term
		s.speed=1 / (speed//2)
		s.health=100
		s.heading=''
		s.tail=[]
		s.event=asyncio.Event()

	def up(s):
		s.heading='\x1b[2D\x1b[A'
	def down(s):
		s.heading='\x1b[2D\x1b[B'
	def left(s):
		s.heading='\x1b[4D'
	def right(s):
		s.heading=''
	async def turn(s):
		import time
		for item in [s.down, s.right, s.down, s.right, s.up, s.right]:
				item()
				# asyncio.sleep(0.8)
				time.sleep(1)
				await s.event()
				# print('dd')

				# asyncio.sleep(2)
	async def grow(s):
		while s.health!=0 :
			print(s.heading+'██', end='', flush=True)
			no,coord=list(*s.term.cursor.save().items())
			if coord in s.tail:
				s.growsnake = s.loop.create_task(s.snake.die())
				break
			else:
				s.tail+=[coord]
			await asyncio.sleep(s.speed)

	async def die(s):
		while s.health > 0:
			current = s.rempiece()
			if not current == Stop.FIRST_OF_STORE:
				s.term.cursor.quicksave()
				print(f'\x1b[{2};1H', repr(s.term.cursor.xy), end='', flush=True)
				s.term.cursor.quickload()
				await asyncio.sleep(s.speed)
			else:
				s.health=0


	def rempiece(s):
		current=s.term.cursor.undo()
		print('\x1b[2D ... ', end='', flush=True)
		if s.term.cursor._coordstore.stop==Stop.FIRST_OF_STORE:
			return Stop.FIRST_OF_STORE
		return current

def main(term):
	term.buffer = term.BUFFER.ALTERNATE
	term.ANSI.cls()
	ctx=Context(term,snakespeed=10)
	ctx.loop.create_task(ctx.snake.turn())

	ctx.play()


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


