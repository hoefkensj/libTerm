#!/usr/bin/env python
import time,sys,os
from libTerm import Term
from libTerm.types import Mode,Coord,Color,ColorSet
from libTerm.libTypes_extra.class_menu import Menu
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
			end=1
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

def main():
	items = ['xxxx', 'xxxx', 'yyyy', 'dasdf', 'dasdf', 'erwrsdd', 'sdf', 'pppfpf']
	term = Term()
	term.buffers.alternate()
	theme=ColorSet(Color(192,192,0))
	term.mode = Mode.CONTROL
	M=Menu(term,items ,location=Coord(10,4),nums=True,colors=theme)
	M.draw()
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.stdin.fd, Controls(term,M))
	loop.run_forever()


main()







