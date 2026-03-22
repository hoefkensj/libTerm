#!/usr/bin/env python
import asyncio


def Controls(term):
	Qs=[]
	def controls():
		key = term.stdin.read()
		if key in 'qQ':
			nonlocal Qs
			Qs+='q'
			if Qs=='qq':
				loop=asyncio.get_running_loop()
				loop.stop()
		else:
			print(repr(key))

	return controls

def main(term):
	print('press qq(double q) to quit!')
	Qs=[]
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.stdin.fd, Controls(term))
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
	t.buffer = t.BUFFER.ALTERNATE
	t.ANSI.cls()
	atexit.register(ExitProcedure,t)
	main(t)
