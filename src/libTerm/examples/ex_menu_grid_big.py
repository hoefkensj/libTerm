#!/usr/bin/env python
import time,sys,os
from libTerm import Term
from libTerm import Mode,Coord,Color,ColorSet
from libTerm.modules.class_menu import Grid
import asyncio
from random import randint

def Controls(term,M):
	prev=''
	def controls():
		nonlocal prev

		def select():
			nonlocal prev
			if prev != '':
				M.select(int(prev))
				prev=''
			else:
				print('\x1b[1;1H chosen:',M.choose())
		def numeric():
			nonlocal prev
			if key in '0123456789':
				prev+=key
				M.select(int(prev))
		def end():
			loop.stop()
			return True

		loop=asyncio.get_running_loop()
		key=term.stdin.read()
		mapping={
		'\x1b[B':M.down,
		'\x1b[A':M.up,
		'\x1b[D':M.left,
		'\x1b[C':M.right,
		'\t':M.prev,
		'q': end,
		'\n': select,
		}
		action=mapping.get(key,numeric)
		done=action()
		if done:
			return
	return controls

# 	return control
#
def makeMenu(term,items):
	fg=Color(0,196,196)
	mycolors=ColorSet(fg=fg)

	M=Grid(term,items ,direction='horizontal', location=Coord(10,10),maxwidth=13,colors=mycolors)
	M.draw()
	return M
def main(term):
	items = []
	for i in range(250):
		items += [chr(randint(65, 68)) + chr(randint(65, 68))]
	menu=makeMenu(term,items)
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.stdin.fd, Controls(term,menu))
	loop.run_forever()




if __name__ == '__main__':
	import atexit
	from libTerm import Term
	def ExitProcedure(t):
		t.ANSI.cls()
		t.mode = t.MODE.NORMAL
		t.buffer = t.BUFFER.DEFAULT
	t=Term()
	t.mode=t.MODE.CONTROL
	t.buffer = t.BUFFER.ALTERNATE
	t.ANSI.cls()
	atexit.register(ExitProcedure,t)

	main(t)







