#!/usr/bin/env python
import asyncio
from libTerm import Coord, Ansi
from libTerm.modules.class_display import LineDisplay
from libTerm.modules.class_frame import Frame
from libTerm.modules.class_controls import Controls
from libTerm.modules.class_context import  Context

async def DEMODATA(f):
	from random import randint
	for i in range(1, 1500000):
		f.display.print(''.join([f'abcdefghijklmnopqrstuvwxyz '[randint(0, 26)] for i in range(randint(1, 150))]))
		await asyncio.sleep(randint(0,100)/100000)



def setControls(ctx,control):
	CSI=Ansi.CSI
	def disp(func,val):
		def scroll(*a):
			ctx.frame.display.scroll(val)
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
	control.regkey(CSI+'B',disp('scroll',+1))
	control.regkey(CSI+'A',disp('scroll',-1))
	control.regkey(CSI+'F',disp('scroll',0))
	control.regkey(CSI+'C',disp('shift',+1))
	control.regkey(CSI+'D',disp('shift',-1))
	control.regkey('4',frame('movex',-1))
	control.regkey('6',frame('movex',+1))
	control.regkey('8',frame('movey',-1))
	control.regkey('2',frame('movey',+1))
#
# 		elif key==CSI+'1;5C':		ctx.frame.move(Coord(1,0))
# 		elif key==CSI+'1;5D':		ctx.frame.move(Coord(-1,0))
# 		elif key==CSI+'1;5A':		ctx.frame.move(Coord(0,-1))
# 		elif key==CSI+'1;5B':		ctx.frame.move(Coord(0,1))
# 		elif key=='\t'      :       ctx.focusnext()
#
# 		elif key=='+'    :			ctx.frame.h_resize(1)
# 		elif key=='-'    :			ctx.frame.h_resize(-1)
#
# 		elif key=='q':
# 			loop = asyncio.get_running_loop()
# 			loop.stop()
# 	return control









def main(term):
	print('done')
	print(repr(term))
	print(repr(term.size))
	print(repr(term.size.xy.x))
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
	# print('done')
	# t.ANSI.cls()
	# print('done')

	atexit.register(ExitProcedure,t)
	# print('done')

	main(t)

