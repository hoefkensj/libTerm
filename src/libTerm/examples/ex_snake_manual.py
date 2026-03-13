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
	def __init__(s,term,snakespeed=1000):
		s.term=term
		s.term.mode = Mode.CONTROL
		s.term.buffer.alternate()
		s.keyseq=''
		s.end=False
		s.started=False
		s.snake=Snake(s,s.term,snakespeed)
		s.loop = asyncio.new_event_loop()
		asyncio.set_event_loop(s.loop)
		s.growsnake = s.loop.create_task(s.snake.grow())
		s.loop.add_reader(s.term.stdin.fd, s.snake.control)
		s.loop.run_forever()
	def end(s):
		s.ctx.loop.stop()

class Snake:
	def __init__(s,ctx,term,speed=1000):
		s.ctx=ctx
		s.term=term
		s.speed=1 / (speed//2)
		s.health=100
		s.heading=''
		s.tail=[]

	def control(s):
		def qq():
			s.ctx.keyseq+='q'
			if s.ctx.keyseq=='qq':
				s.ctx.end()
		key = s.term.stdin.read()
		if key =='q':
			qq()
			s.die()
		ctrl = {
			'\x1b[A':'\x1b[2D\x1b[A',
			'\x1b[B':'\x1b[2D\x1b[B',
		 	'\x1b[C':'',
		 	'\x1b[D':'\x1b[4D',
		}
		s.heading=ctrl.get(key,s.heading)
	async def grow(s):
		while s.health!=0 :
			print(s.heading+'██', end='', flush=True)
			no,coord=list(*s.term.cursor.save().items())
			if coord in s.tail:
				s.die()
				break
			else:
				s.tail+=[coord]
			await asyncio.sleep(s.speed)

	def die(s):
		while s.health > 0:
			current = s.rempiece()
			if not current == StoreStop.FIRST_OF_STORE:
				s.term.cursor.quicksave()
				print(f'\x1b[{2};1H', repr(s.term.cursor.xy), end='', flush=True)
				s.term.cursor.quickload()
				time.sleep(s.speed)
			else:
				s.health=0
	def rempiece(s):
		current=s.term.cursor.undo()
		print('\x1b[2D  ', end='', flush=True)
		if s.term.cursor._coordstore.stop==StoreStop.FIRST_OF_STORE:
			return StoreStop.FIRST_OF_STORE
		return current







term=Term()
ctx=Context(term,snakespeed=10)

ctx.run()






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




