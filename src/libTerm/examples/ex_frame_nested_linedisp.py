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



def Controls(term,frame):
	CSI=Ansi.CSI
	def control():
		key=term.stdin.read()
		print('\x1b[3;1H'+repr(key),end='', flush=True)
		if   key==CSI+'B':			frame.display.scroll(+1)
		elif key==CSI+'A':			frame.display.scroll(-1)
		elif key==CSI+'C':			frame.display.shift(+1)
		elif key==CSI+'D':			frame.display.shift(-1)
		elif key==CSI+'1;2C':		frame.move(Coord(1,0))
		elif key==CSI+'1;2D':		frame.move(Coord(-1,0))
		elif key==CSI+'1;2A':		frame.move(Coord(0,-1))
		elif key==CSI+'1;2B':		frame.move(Coord(0,1))

		elif key==CSI+'F':			frame.display.scroll(0)
		elif key=='+'    :			frame.h_resize(1)
		elif key=='-'    :			frame.h_resize(-1)

		elif key=='q':
			loop = asyncio.get_running_loop()
			loop.stop()
	return control

def main(term):
	print('done')

	frame = Frame(term,
				  name='test',
				  location=Coord(5, 5),
				  size=Coord(80, 15),
				  )
	ldisp=LineDisplay
	frame.addDisplay(ldisp)
	frame.draw()


	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)

	loop.add_reader(
		term.stdin.fd,
		Controls(term,frame)
	)
	loop.create_task(DEMODATA(frame))
	loop.run_forever()




if __name__ == '__main__':
	import atexit
	# print('done')

	from libTerm import Term
	def ExitProcedure(t):
		t.ANSI.cls()
		t.mode = t.MODE.DEFAULT
		t.buffer = t.BUFFER.DEFAULT
	# print('done')

	t=Term()
	# print('done')

	t.mode=t.MODE.CONTROL
	t.buffer = t.BUFFER.ALTERNATE
	# print('done')
	t.ANSI.cls()
	# print('done')

	atexit.register(ExitProcedure,t)
	# print('done')

	main(t)

