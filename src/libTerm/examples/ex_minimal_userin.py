import atexit, asyncio
from libTerm import Term,Mode,Buffer


def ExitProcedure(t):
	t.ANSI.cls()
	t.mode = t.MODE.NORMAL
	t.buffer = t.BUFFER.DEFAULT

def PrintUserIn():
	no=0
	def printuserin(txt):
		nonlocal no
		no+=1
		print(f'\x1b[{10+no};5H{no}{txt}')
	return printuserin


def CheckInput(term):
	printer=PrintUserIn()
	def checkinput():
		key = term.tty.input.read()
		if key == 'q':
			loop=asyncio.get_event_loop()
			loop.stop()
		elif key =='i':
			term.mode = Mode.NORMAL
			userin = input('\x1b[15;20Hplease enter your input: ')
			print('\x1b[15;20H\x1b[2K')
			term.mode =Mode.CONTROL
			printer(userin)

	return checkinput


def main(term):
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.tty.input.fd, CheckInput(term))
	loop.run_forever()


if __name__ == '__main__':
	term = Term()
	term.mode = Mode.CONTROL
	term.buffer = Buffer.ALTERNATE
	term.ANSI.cls()
	atexit.register(ExitProcedure, term)
	print('\x1b[1;1Hpress "i" for input "q" for quit')

	main(term)

