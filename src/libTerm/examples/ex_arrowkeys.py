# /usr/bin/env python

from libTerm import Term
from libTerm.types import Mode
import asyncio

def main(t):
	def tohex(stdin):
		hex = ''
		for char in stdin:
			hex += f'{ord(char):02x} '
		return hex.strip()

	def print_index():
		for ansi in arrowkeys:
			print(tpl_arrowkeys.format(
				ANSI=repr(ansi),
				HEX=tohex(ansi),
				SYMBOL=arrowkeys[ansi])
			)
	# setting the terminal to control mode, this will allow us to read the input events and control the output
	t.mode=Mode.CONTROL

		#
	# Print Templates:
	tpl_arrowkeys ='\x1b[10G\x1b[0;31m{ANSI}\x1b[m \x1b[20G:\x1b[25G\x1b[0;32m{SYMBOL}\x1b[0;2m\x1b[45G({HEX})'
	tpl_matched   ='\x1b[9;10H\x1b[1;31m{MATCH}\x1b[25G\x1b[1;32m{KEY}\x1b[m'

	arrowkeys={
		'\x1b[A': '▲',
		'\x1b[B': '▼',
		'\x1b[C': '▶',
		'\x1b[D': '◀',
	}


	async def checkinput():
		loop=asyncio.get_running_loop()
		event=t.stdin.sync
		while True:
			await asyncio.wait_for(event)
			key = t.stdin.read()
			print(repr(key))
			if key in [*arrowkeys.keys()]:
				print(tpl_matched.format(MATCH=repr(key), KEY=arrowkeys[key]))
			elif key in 'qQ':
				break

	print("\x1b[2J\x1b[1;1H\x1b[1;4mDetecting and Matching arrow keys:\x1b[m")
	print('-' * 40)
	print_index()
	print('\x1b[8;1H\x1b[mPress arrow keys to Test:', '\x1b[9;3HInput:\x1b[20GKey:')
	print('\x1b[15;1HPress \x1b[31mq\x1b[m to quit')
	loop=asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	asyncio.run(checkinput())
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

if __name__=='__main__':
	T=Term()
	# Switch to the alternate buffer, so we don't mess with the main buffer of the terminal,
	# and we can easily switch back to it when we are done.
	T.buffers.alternate()
	main(T)
