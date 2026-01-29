# /usr/bin/env pyhthon

from libTerm import Term,Mode
import sys
buf = b""
term=Term()
term.mode=Mode.CONTROL
print('Press Q to quit, Press arrowkeys to Test')
while True:
	if term.stdin.event:
		key=term.stdin.read()
		if key == '\x1b[D':
			print("LEFT")
		elif key == '\x1b[C':
			print("RIGHT")
		elif key == '\x1b[A':
			print("UP")
		elif key == '\x1b[B':
			print("DOWN")
		elif key == 'q':
			sys.exit(0)
		print(repr(key))
