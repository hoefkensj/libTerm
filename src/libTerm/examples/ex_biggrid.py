#!/usr/bin/env python
import time,sys,os
from libTerm import Term,Color,Coord,Mode,Selector
from libTerm.libextra.class_menu import Grid
import asyncio
from random import randint

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
			term.buffer.default()
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
	M=Grid(term,items ,direction='horizontal', location=Coord(10,10),maxwidth=13)
	M.draw()
	return M
def main(items):
	term = Term()
	term.buffer.alternate()
	term.mode = Mode.CONTROL

	menu=makeMenu(term,items)
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.fd, Controls(term,menu))
	loop.run_forever()

if __name__=='__main__':
	items=[]
	for i in range(50):
		items += [chr(randint(65,68))+chr(randint(65,68))]
	main([*items,*items,*items])







