# /usr/bin/env python

import time
from libTerm import Term
from libTerm.types import Mode
from libTerm.types.enums import StoreStop as Stop
from libTerm import Term
from libTerm.types import Mode
import time
import asyncio

from libTerm.types.enums import StoreStop
# class Snake:
# 	def __init__(s,t,speed=10):
# 		s.speed=1 / (speed or 1)
# 		s.term=t
# 		s.piece='█'
# 		s.dir='C'
# 	def addpiece(s):
# 		print(f'\x1b[{s.dir}\x1b[D{s.piece}', end='', flush=True)
# 		s.term.cursor.save()
#
# 	def rempiece(s):
# 		current=s.term.cursor.undo()
# 		print('\x1b[D ', end='', flush=True)
# 		if s.term.cursor._coordstore.stop==Stop.FIRST_OF_STORE:
# 			return Stop.FIRST_OF_STORE
# 		return current

class Context:
	def __init__(s,term):
		s.term=term
		s.snake=None
		s.controls=None
		s.loop=None
		s.movesnake=None
		s.keycontrol=None
		s.keyseq=''
		s.end=False
		s.started=False
		s.snake=Snake(s,s.term,1000)
		s.setloop()
		s.startup()

	def run(s):
		s.loop.add_reader(s.term.stdin.fd, s.snake.control)
		s.movesnake = s.loop.create_task(s.snake.grow())
		s.loop.run_forever()


	def startup(s):
		# initialize terminal
		s.term=Term()
		s.term.echo = False
		s.term.cursor.hide()
		s.term.buffer.switch()
		# print('\x1b[J\x1b[1;1HPress one of up,down,left,right to start and  q to quit!\x1b[2;2H')
		s.term.mode = Mode.CONTROL


	def setloop(s):
		if s.loop is None:
			s.loop = asyncio.new_event_loop()
			asyncio.set_event_loop(s.loop)
		else:
			s.loop = asyncio.get_running_loop()



class Snake:
	def __init__(s,ctx,t,speed=100):
		s.ctx=ctx
		s.speed=100 / (speed or 1)
		s.term=t
		s.state='ALIVE'
		s.heading=''
		s.piece='██'
		s.tail=[]
		s._started=False
		s._moving=False
	def control(s):
		key = s.term.stdin.read()
		if key == '\x1b[A':
			s.heading='\x1b[2D\x1b[A'
		if key == '\x1b[B':
			s.heading='\x1b[2D\x1b[B'
		if key == '\x1b[C':
			s.heading=''
		if key == '\x1b[D':
			s.heading='\x1b[4D'
		if key == 'q':
			s.ctx.keyseq+='q'
	#
	def die(s):
		current = s.rempiece()
		if not current == StoreStop.FIRST_OF_STORE:
			s.term.cursor.quicksave()
			print(f'\x1b[{2};1H', repr(s.term.cursor.xy), end='', flush=True)
			s.term.cursor.quickload()
			time.sleep(s.speed//2)
		return 'DEAD'

	async def grow(s):
		while s.state == 'ALIVE' :
			print(s.heading+s.piece, end='', flush=True)
			no,coord=list(*s.term.cursor.save().items())
			if coord in s.tail:
				s.state=s.die()
			else:
				s.tail+=[coord]
			await asyncio.sleep(0.1)

	def rempiece(s):
		current=s.term.cursor.undo()
		print('\x1b[D ', end='', flush=True)
		if s.term.cursor._coordstore.stop==StoreStop.FIRST_OF_STORE:
			return StoreStop.FIRST_OF_STORE
		return current







term=Term()
ctx=Context(term)

ctx.run()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_forever()




	# elif seq=='q':
	# 	current=snake.rempiece()
	# 	if not current==Stop.FIRST_OF_STORE:
	# 		print(f'\x1b[s\x1b7\x1b[{2};1H', repr(term.cursor.xy), '\x1b[u\x1b8', end='', flush=True)
	# # 		time.sleep(snake.speed)
	#
	# 	else:
	# 		end=True
	# if seq=='qq' or end:
	# 	term.sync.default()
	# 	exit()
	# else:
	# 	if snake.piece != '' and not 'q'in seq:
	# 		snake.addpiece()

	# print(f'\x1b[s\x1b7\x1b[{2};1H',repr(term.cursor.xy),'\x1b[u\x1b8',end='',flush=True)

	# time.sleep(snake.speed)




