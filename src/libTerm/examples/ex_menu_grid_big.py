#!/usr/bin/env python
import time,sys,os
from libTerm import Term
from libTerm import Mode,Coord,Color,ColorSet,Context
from libTerm.modules.class_frame import Frame
from libTerm.modules.class_menu import Grid,Formatting
from libTerm.modules.class_controls import Controls
import asyncio
from random import randint

def controls(term,M):
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


	return M

def main(term):
	from libTerm.components.enums import Ansi
	CSI=Ansi.CSI
	items = []
	fmt=Formatting()
	fmt.pad_pre=' '
	fmt.pad_post=' '
	fmt.sep_nrlabel=':'
	fmt.pad_sep=' '
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	ctx = Context('Main',term, loop)

	frame=Frame(
		ctx,
		name='frmGridMenu',
		location=Coord(5, 5))
	fmt.mnu_maxwidth=frame.size.x
	opts={'direction':'horizontal', 'maxhoritems':7,'fmt':fmt}
	frame.addMenu(Grid,**opts)
	# for i in range(50):
	# 	frame.display.addItem(chr(randint(65, 89)) + chr(randint(65 + 32, 89 + 32)) + chr(randint(65 + 32, 68 + 32)) + chr(randint(65 + 32, 68 + 32)))
	def add50():
		for i in range(50):
			frame.display.addItem(chr(randint(65, 89)) + chr(randint(65 + 32, 89 + 32)) + chr(randint(65 + 32, 68 + 32)) + chr(randint(65 + 32, 68 + 32)))
	add50()

	#
	# loop = asyncio.new_event_loop()
	# asyncio.set_event_loop(loop)
	# ctrl=Controls(term=term,loop=loop)
	# ctrl.regkey(CSI+'B',frame.display.down)
	# ctrl.regkey(CSI+'A',frame.display.up)
	# ctrl.regkey(CSI+'D',frame.display.left)
	# ctrl.regkey(CSI+'C',frame.display.right)
	# ctrl.regkey('+',add50)
	# ctrl.regkey('\n',frame.display.choose)
	# ctrl.regseq('qq',sys.exit)
	# loop.run_forever()




if __name__ == '__main__':
	import atexit
	from libTerm import Term
	def ExitProcedure(t):
		t.ANSI.cls()
		t.mode = t.MODE.NORMAL
		t.buffer = t.BUFFER.DEFAULT
	t=Term()
	main(t)







