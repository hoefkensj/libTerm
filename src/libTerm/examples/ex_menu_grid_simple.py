#!/usr/bin/env python
import time,sys,os
from libTerm import Term
from libTerm import Mode,Coord,Color
from libTerm.modules.class_menu import Grid
import asyncio


def Controls(term,M):
	prev=''
	def controls():
		nonlocal prev
		loop=asyncio.get_running_loop()
		key=term.stdin.read()
		if key == '\x1b[B':
			M.down()
		elif key == '\x1b[A':
			M.up()
		elif key == '\x1b[D':
			M.left()
		elif key == '\x1b[C':
			M.right()
		elif key == '\t':
			M.prev()
		elif key == 'q':
			term.sync.default()
			loop.stop()
			sys.exit()
		elif key == '\n':

			if prev != '':
				M.select(int(prev))
				prev=''
			else:
				print('\x1b[1;1H chosen:',M.choose())
		elif key in '0123456789':
			prev+=key
			M.select(int(prev))
	return controls

# 	return control
#
def makeMenu(term,items):
	M=Grid(term,items ,location=Coord(10,10),maxheight=5)
	M.draw()
	return M
def main(term):
	items = ['a'*10, 'b'*5, 'c'*12, 'd'*11,'#'*9, 'K'*5, 'V'*10, '@'*15]

	menu=makeMenu(term,items)
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.fd, Controls(term,menu))
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




