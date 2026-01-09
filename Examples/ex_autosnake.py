# /usr/bin/env pyhthon
from libTerm import Term
from libTerm import Coord



def snake(t,speed=100):
	import time
	def addpiece(piece):
		print(piece, end='', flush=True)
		t.cursor.save();

	def rempiece():
		t.cursor.undo()
		print('\x1b[D ', end='', flush=True)

	t.echo(True)
	t.cursor.show(False)
	t.cursor.hide(True)
	vert=t.size.xy.y
	print(vert)
	time.sleep(5)
	print('\x1b[B\x1b[D▌', flush=True)
	for i in range(8):
		for i in range(vert):
			addpiece('\x1b[B\x1b[D░')
			time.sleep(1/(speed or 1))
		for i in range(6):
			addpiece('░')
			time.sleep(1 / (speed or 1))
		for i in range(vert):
			addpiece('\x1b[A\x1b[D░')
			time.sleep(1 / (speed or 1))
		for i in range(6):
			addpiece('░')
			time.sleep(1 / (speed or 1))

	while t.cursor.store.selected:
		rempiece()
		time.sleep(1 / (speed or 1))


snake(Term(),speed=1000)