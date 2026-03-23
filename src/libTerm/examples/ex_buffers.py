#!/usr/bin/env python
from libTerm import Term
from libTerm.types import Buffer
from time import sleep


def main(term):
	print(term.buffer)
	sleep(2)
	term.buffer=Buffer.ALTERNATE
	print(term.buffer)
	sleep(2)
	term.buffer=Buffer.DEFAULT
	print(term.buffer)
	sleep(2)


if __name__	== '__main__':
	t=Term()
	main(t)