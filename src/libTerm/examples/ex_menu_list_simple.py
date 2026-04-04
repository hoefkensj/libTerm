#!/usr/bin/env python
import time,sys,os
from libTerm import Term
from libTerm import Coord,Color,ColorSet
from libTerm.modules.class_menu import Menu
import asyncio


def Controls(term,M):
	prev=''
	def controls():
		nonlocal prev
		key=term.stdin.read()
		if key == '\x1b[B':
			M.next()
		elif key == '\x1b[A':
			M.prev()
		elif key == 'q':
			term.mode=Mode.default
			loop=asyncio.get_running_loop()
			loop.stop()
		elif key == '\n':
			prev=''
			print('\x1b[1;1H chosen:',M.choose())
		elif key in '0123456789':
			prev+=key
			if int(prev)>len(M)+1:
				prev=str(1)
			M.select(int(prev))
	return controls

# 	return control
#

def main(term):
	items = ['xxxx', 'xxxx', 'yyyy', 'dasdf', 'dasdf', 'erwrsdd', 'sdf', 'pppfpf']
	theme=ColorSet(Color(192,192,0))
	M=Menu(term,items ,location=Coord(10,4),nums=True,colors=theme)
	M.draw()
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.stdin.fd, Controls(term,M))
	loop.run_forever()

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


