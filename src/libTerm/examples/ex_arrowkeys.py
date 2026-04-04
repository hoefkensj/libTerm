# /usr/bin/env python

from libTerm import Term
from libTerm import Mode
import asyncio

tpl_arrowkeys = '\x1b[10G\x1b[0;31m{ANSI}\x1b[m \x1b[20G:\x1b[25G\x1b[0;32m{SYMBOL}\x1b[0;2m\x1b[45G({HEX})'
tpl_matched = '\x1b[9;10H\x1b[1;31m{MATCH}\x1b[25G\x1b[1;32m{KEY}\x1b[m'

arrows = {
	'\x1b[A': '▲',
	'\x1b[B': '▼',
	'\x1b[C': '▶',
	'\x1b[D': '◀',
}


def init():
	print("\x1b[2J\x1b[1;1H\x1b[1mDetecting and Matching arrow keys:\x1b[m")
	print('-' * 80)
	print_index()
	print('\x1b[8;1H\x1b[mPress arrow keys to Test:', '\x1b[9;3HInput:\x1b[20GKey:')
	print('\x1b[15;1HPress \x1b[31mq\x1b[m to quit')

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
def tohex(stdin):
	hex = ''
	for char in stdin:
		hex += f'{ord(char):02x} '
	return hex.strip()

def print_index():
	for ansi in arrows:
		print(tpl_arrowkeys.format(
			ANSI=repr(ansi),
			HEX=tohex(ansi),
			SYMBOL=arrows.get(ansi))
		)
def ArrowKeys(key):
	if key in [*arrows.keys()]:
		print(tpl_matched.format(MATCH=repr(key), KEY=arrows.get(key)))
	elif key in 'qQ':
		loop=asyncio.get_running_loop()
		loop.stop()


def CheckInput(term):
	def checkinput():
		key = term.stdin.read()
		ArrowKeys(key)
	return checkinput

def main(term):
	init()

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.stdin.fd, CheckInput(term))
	loop.run_forever()



if __name__ == '__main__':
	import atexit
	def ExitProcedure(t):
		t.ANSI.cls()
		t.mode = t.MODE.NORMAL
		t.buffer = t.BUFFER.DEFAULT
	t=Term()
	t.mode=t.MODE.CONTROL
	t.buffer = t.BUFFER.ALTERNATE
	t.ANSI.cls()
	atexit.register(ExitProcedure,t)
	main(t)

