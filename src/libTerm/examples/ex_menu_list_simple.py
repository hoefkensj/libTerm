#!/usr/bin/env python
import time,sys,os
from libTerm import Term,Color,Coord,Mode,Selector
from libTerm.libextra.class_menu import Menu
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
			term.buffer.default()
			sys.exit()
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
	term.buffer.alternate()
	term.mode = Mode.CONTROL
	M=Menu(term,items ,location=Coord(10,4),nums=True,fgcolor=Color(192,192,0))
	M.draw()
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.fd, Controls(term,M))
	loop.run_forever()

if __name__=='__main__':
	main()







