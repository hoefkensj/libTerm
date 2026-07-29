#!/usr/bin/env python
#!/usr/bin/env python
import asyncio
from libTerm import Coord, Ansi
from libTerm.modules.class_display import LineDisplay
from libTerm.modules.class_frame import Frame
from libTerm.modules.class_controls import Controls
from libTerm.modules.class_context import  Context


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

