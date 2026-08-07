#!/usr/bin/env python
import time,sys,os
from libTerm import Term
from libTerm import Mode,Coord,Color,ColorSet
from libTerm.modules.class_menu import Grid
import asyncio
from random import randint
from libTerm.modules.class_frame import Frame
def Controls(term,M):
	from libTerm.components.enums import Ansi
	CSI=Ansi.CSI
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
		CSI+'B':M.down,
		CSI+'A':M.up,
		CSI+'D':M.left,
		CSI+'C':M.right,
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
	M=Grid(term=term,items=items ,location=Coord(10,10),maxheight=5,colors=mycolors)
	M.draw()
	return M


def main(term):
	items = ['a'*10, 'b'*5, 'c'*12, 'd'*11,'#'*9, 'K'*5, 'V'*10, '@'*15]
	frm=Frame(term=term)
	frm.location=Coord(1,1)
	frm.size=Coord(200,20)
	frm.show(True)

	fg=Color(0,196,196)
	mycolors=ColorSet(fg=fg)

	frm.addMenu(Grid,items=items,location=Coord(10,10),maxheight=5,colors=mycolors)
	for item in items:
		frm.display.addItem(item)
	print(str(frm.display))
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	# loop.add_reader(term.tty.input.fd, Controls(term,menu))
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
	# t.buffer = t.BUFFER.ALTERNATE
	t.ANSI.cls()
	# atexit.register(ExitProcedure,t)
	main(t)




