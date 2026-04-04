#!/usr/bin/env python
from libTerm import Color
def main(term):
	print("Get terminal colors for the cursor char cell: ")
	print("Using Term().color: ")
	print(f"ForeGround(fg) color in 8bit rgb values {term.color.fg.RGB8=}")
	print(f"Same but 4 bit RGB {term.color.fg.RGB4=}")
	print(f"BackGround(bg) color in  16Bit RGB {term.color.bg.RGB16=}")
	print(f"these are Color Objects, they dont color things or do markup they just represent a color,in most common formats" )
	print(f'red=Color(255,0,0) :  {Color(255,0,0,)=}')

	print(f"{term.color.bg.neg.RGB8=}")
	print(f"{term.color.bg.neg.RGB32=}")
	print(f"{term.color.fg.RGB4=}")


async def qscan(term):
	import asyncio
	loop=asyncio.get_running_loop()
	event = t.stdin.sync
	print('press n for next example')
	while True:
		await asyncio.wait_for(event)
		key = t.stdin.read()
		print('\x1b[3;1HKey:\x1b[32m {KEY}\x1b[m'.format(KEY=key), end='', flush=True)
		if key == 'q':
			print('continuing')
			break


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

