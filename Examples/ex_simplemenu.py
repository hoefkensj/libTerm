# /usr/bin/env pyhthon
import time,sys,os
from libTerm import Term,Color,Coord,Mode,Selector
from libextra.class_menu import Menu
import asyncio


def Controls(term,M):
	def controls():
		key=term.stdin.read()
		if key == '\x1b[B':
			M.next()
		elif key == '\x1b[A':
			M.prev()
		elif key == 'q':
			term.buffer.default()
			sys.exit()
		elif key == '\n':
			print('\x1b[1;1H chosen:',M.choose())
	return controls

# 	return control
#
def makeMenu(term,items):
	M=Menu(term,items ,xy=Coord(10,10))
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
	items = ['a'*90, 'b'*95, 'c'*120, 'd'*115,'#'*90, 'K'*95, 'V'*120, '@'*115]
	main([*items,*items,*items])







