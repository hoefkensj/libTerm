#!/usr/bin/env python
import time,sys,os
import asyncio
from libTerm import Coord, Ansi
from libTerm.modules.class_display import LineDisplay
from libTerm.modules.class_frame import Frame
from libTerm.modules.class_controls import Controls
from libTerm.modules.class_context import  Context

from libTerm import Term
from libTerm import Coord,Color,ColorSet
from libTerm.modules.class_menu import Menu
import asyncio

def setControls(ctx,control):
	CSI=Ansi.CSI
	def disp(func,val):
		def next(*a):
			ctx.frame.display.next()
		def shift(*a):
			ctx.frame.display.shift(val)
		fn={'scroll':scroll,
			'shift':shift
			}
		return fn.get(func)
	def frame(func,val):
		def movex(*a):
			ctx.frame.move(Coord(val,0))
		def movey(*a):
			ctx.frame.move(Coord(0,val))
		fn={'movex':movex,
			'movey':movey}
		return fn.get(func)

	control.regkey('\t',ctx.focusNext)
	control.regkey(CSI+'B',disp('next',+1))
	control.regkey(CSI+'A',disp('prev',-1))
	control.regkey(CSI+'F',disp('scroll',0))
	control.regkey(CSI+'C',disp('shift',+1))
	control.regkey(CSI+'D',disp('shift',-1))
	control.regkey('4',frame('movex',-1))
	control.regkey('6',frame('movex',+1))
	control.regkey('8',frame('movey',-1))
	control.regkey('2',frame('movey',+1))

def Controls(term,M):
	prev=''
	def controls():
		nonlocal prev
		key=term.tty.input.read()
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
	ctx=Context(term,loop)
	ctx.addFrame(name='frm_First',
				  location=Coord(1,1),
				  size=Coord(term.size.xy.x//2 or 80,term.size.xy.y//2 or 10),
				  )
	ctx.addFrame(name='frm_Second',
				  location=Coord(1, term.size.xy.y//2),
				  size=Coord(term.size.xy.x//2 or 80, term.size.xy.y//2-2),
				  )


	did=ctx.frm_First.addDisplay('demo1',LineDisplay)
	did=ctx.frm_Second.addDisplay('demo2',LineDisplay)
	# firstframe.selectDisplay(did)
	# secondframe.selectDisplay(did)
	# secondframe.draw()
	# firstframe.draw()

	ctx.enableControls(True)
	setControls(ctx, ctx.controls)
	ctx.loop.create_task(DEMODATA(ctx.frm_First))
	ctx.loop.create_task(DEMODATA(ctx.frm_Second))
	ctx.loop.run_forever()



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



