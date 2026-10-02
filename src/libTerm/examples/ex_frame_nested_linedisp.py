#!/usr/bin/env python
import asyncio,sys
from libTerm import Coord, Ansi
from libTerm.modules.class_display import LineDisplay
from libTerm.modules.class_frame import Frame
from libTerm.modules.class_controls import Controls
from libTerm.modules.class_context import  Context

async def DEMODATA(f):
	from random import randint
	for i in range(1, 1500000):
		f.display.print(str(i)+''.join([f'abcdefghijklmnopqrstuvwxyz '[randint(0, 26)] for i in range(randint(1, 150))]))
		await asyncio.sleep(randint(0,1000)/randint(100,1000))

def setControls(ctx):
	CSI=Ansi.CSI
	def disp(action,value):
		def function(*a):
			getattr(ctx.frame.display, action)(value)
		return function
	def frame(action,value):
		def function(*a):
			getattr(ctx.frame,action)(value)
		return function
	ctx.controls.regkey('\t',ctx.focusNext)
	ctx.controls.regkey('q',sys.exit)
	ctx.controls.regkey(CSI+'A',disp('scroll',-1))
	ctx.controls.regkey(CSI+'B',disp('scroll',+1))
	ctx.controls.regkey(CSI+'F',disp('scroll',0))
	ctx.controls.regkey(CSI+'C',disp('shift',+1))
	ctx.controls.regkey(CSI+'D',disp('shift',-1))
	ctx.controls.regkey('4',frame('move',Coord(-1,0)))
	ctx.controls.regkey('6',frame('move',Coord(+1,0)))
	ctx.controls.regkey('8',frame('move',Coord(0,-1)))
	ctx.controls.regkey('2',frame('move',Coord(0,+1)))
	return ctx





def main(term):
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	framejoin_y=term.size.xy.y//2 or 10
	locframeFirst=Coord(1,1)
	sizeframeFirst=Coord(term.size.xy.x//2 or 80,framejoin_y)
	locframeSecond=locframeFirst.y+sizeframeFirst.y+Coord(1,1).y
	locframeSecond=Coord(1,locframeSecond)
	ctx=Context(term,loop)
	ctx.addFrame(name='frm_First',
				  location=locframeFirst,
				  size=sizeframeFirst,
				  )
	ctx.addFrame(name='frm_Second',
				  location=locframeSecond,
				  size=Coord(term.size.xy.x//2 or 80, (term.size.xy.y//2 or sizeframeFirst.y)-2	),
				  )
	ctx.frm_First.addDisplay('demo1',LineDisplay)
	ctx.frm_Second.addDisplay('demo2',LineDisplay)
	ctx.enableControls(True)
	ctx=setControls(ctx)
	ctx.loop.create_task(DEMODATA(ctx.frm_First))
	ctx.loop.create_task(DEMODATA(ctx.frm_Second))
	ctx.loop.run_forever()



if __name__ == '__main__':
	import atexit
	# print('done')

	from libTerm import Term
	def ExitProcedure(t):
		# t.ANSI.cls()
		t.mode = t.MODE.DEFAULT
		t.buffer = t.BUFFER.DEFAULT
	# print('done')

	t=Term()
	# print('done')

	t.mode=t.MODE.CONTROL
	# t.buffer = t.BUFFER.ALTERNATE


	atexit.register(ExitProcedure,t)

	main(t)

