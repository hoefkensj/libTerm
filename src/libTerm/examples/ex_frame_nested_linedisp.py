#!/usr/bin/env python
import asyncio
from libTerm import Coord, Ansi
from libTerm.modules.class_display import LineDisplay
from libTerm.modules.class_frame import Frame

async def DEMODATA(f):
	from random import randint
	for i in range(1, 1500):
		f.display.print(''.join([f'abcdefghijklmnopqrstuvwxyz '[randint(0, 26)] for i in range(randint(1, 150))]))
		await asyncio.sleep(randint(0,100)/1000)



def Controls(ctx):
	CSI=Ansi.CSI
	def control():
		key=ctx.term.tty.input.read()
		print('\x1b[3;1H'+repr(key),end='', flush=True)
		if  ctx.frame.display is not None:
			if   key==CSI+'B':			ctx.frame.display.scroll(+1)
			elif key==CSI+'A':			ctx.frame.display.scroll(-1)
			elif key==CSI+'C':			ctx.frame.display.shift(+1)
			elif key==CSI+'D':			ctx.frame.display.shift(-1)
			elif key==CSI+'F':			ctx.frame.display.scroll(0)

		elif key==CSI+'1;5C':		ctx.frame.move(Coord(1,0))
		elif key==CSI+'1;5D':		ctx.frame.move(Coord(-1,0))
		elif key==CSI+'1;5A':		ctx.frame.move(Coord(0,-1))
		elif key==CSI+'1;5B':		ctx.frame.move(Coord(0,1))
		elif key=='\t'      :       ctx.focusnext()

		elif key=='+'    :			ctx.frame.h_resize(1)
		elif key=='-'    :			ctx.frame.h_resize(-1)

		elif key=='q':
			loop = asyncio.get_running_loop()
			loop.stop()
	return control
class Context():
	def __init__(s,term,loop=None):
		s.term=term
		s.loop=loop
		s.frames={}
		s.focusid=0
		s.frame=None

	def addFrame(s,frame):
		fid=len(s.frames)+1
		s.frames[fid]=frame
		if fid==1 and s.focusid==0:
			s.focusid=1
		if s.frame is None:
				s.frame=frame
		return fid

	def selectFrame(s,n=1):
		s.frame=s.frames.get(n)
		if s.frame is not None:
			s.frame.focus(True)
			s.frame.draw()
			s.focusid=n

	def focusnext(s):
		if s.frame is not None:
			s.frame.focus(False)
		s.focusid+=1
		if s.focusid>len(s.frames):
			s.focusid=0
		s.selectFrame(s.focusid)



	def initloop(s):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		s.loop=loop
		return loop
	def addControls(s,controls):
		s.controls=controls
		s.loop.add_reader(
			s.term.tty.input.fd,
			s.controls(s)
		)

def main(term):
	print('done')
	ctx=Context(term,None)
	firstrame=Frame(term,
				  name='frm_First',
				  location=Coord(5, 5),
				  size=Coord(80, 15),
				  )
	secondframe=Frame(term,
				  name='frm_Second',
				  location=Coord(90, 5),
				  size=Coord(80, 15),
				  )
	id1=ctx.addFrame(firstrame)
	id2=ctx.addFrame(secondframe)
	ctx.frames[id2].focus()

	ldisp=LineDisplay
	did=secondframe.addDisplay('demo',ldisp)
	secondframe.selectDisplay(did)
	secondframe.draw()
	secondframe.display.show(True)
	ctx.initloop()
	# ctx.addControls(Controls)


	ctx.loop.create_task(DEMODATA(secondframe))
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

	t=Term(controls=True)
	# print('done')

	t.mode=t.MODE.CONTROL
	# t.buffer = t.BUFFER.ALTERNATE
	# print('done')
	# t.ANSI.cls()
	# print('done')

	atexit.register(ExitProcedure,t)
	# print('done')

	main(t)

