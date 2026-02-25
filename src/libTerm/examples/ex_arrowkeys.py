# /usr/bin/env python

from libTerm import Term
from libTerm.types import Mode

# initializing the terminal to be the active terminal:
term=Term()

# setting the terminal to control mode, this will allow us to read the input events and control the output
term.mode=Mode.CONTROL

# Switch to the alternate buffer, so we don't mess with the main buffer of the terminal,
# and we can easily switch back to it when we are done.
term.buffer.switch()
#

print("\x1b[2J\x1b[1;1H\x1b[1mDetecting and Matching arrow keys:\x1b[m")
print('-'*40)

arrowkeys={
	'\x1b[D':'◀',
	'\x1b[C':'▶',
	'\x1b[A':'▲',
	'\x1b[B':'▼'}

for match in arrowkeys:
	print(f"\x1b[10G\x1b[0;31m{repr(match)}\x1b[m \x1b[20G:\x1b[25G\x1b[0;32m{arrowkeys[match]}\x1b[m")
print('-'*40)
print('\x1b[8;1HPress arrow keys to Test:','\x1b[9;3HInput:\x1b[20GKey:','\x1b[15;1HPress \x1b[31mQ\x1b[m to quit' )
while True:
	if term.stdin.check:
		key=term.stdin.read()
		if key in ['\x1b[D','\x1b[C','\x1b[A','\x1b[B']:
			print(f'\x1b[9;10H\x1b[1;31m{repr(key)}\x1b[25G\x1b[1;32m{arrowkeys[key]}\x1b[m')
		elif key == 'q':
			break
"""	
	WARNING:
	  	DON'T USE THIS IN PRODUCTION, THIS IS JUST A DEMO OF HOW TO READ ARROW KEYS, IT USES A LOT OF CPU
"""
"""
	NOTE: 
		you can/should use : 
		- asyncio: events,tasks and loops 
		- Signals: Signal,pause and SIGUSR1
		they are less CPU intensive, but that is out of the scope of this example,
		libTerm is independent of any paradigm you want to use.
"""

