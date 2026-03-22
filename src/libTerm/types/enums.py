#!/usr/bin/env python
from enum import IntEnum,StrEnum

class Mode(IntEnum):
	NONE	= 0
	none	= 0
	NRML	= 1
	nrml	= 1
	NORMAL  = 1
	normal  = 1
	DEFAULT = 1
	default = 1
	CTL	 = 2
	ctl	 = 2
	CTRL	= 2
	ctrl	= 2
	CONTROL = 2
	control = 2
	inp     = 3
	Inp     = 3
	Input   = 3
	INP      = 3
	INPUT      = 3

class StoreStop(StrEnum):
	FIRST_OF_STORE	= "FIRST_OF_STORE"
	LAST_OF_STORE	= "LAST_OF_STORE"

class Buffer(IntEnum):
	NONE     = 0
	DEFAULT  = 1
	Default  = 1
	default  = 1
	DEF      = 1
	Def      = 1
	BUFFER0  = 1
	Buffer0  = 1
	buffer0  = 1
	BUF0     = 1
	Buf0     = 1
	buf0     = 1
	ALTERNATE= 2
	Alternate= 2
	alternate= 2
	ALT      = 2
	Alt      = 2
	alt      = 2
	BUFFER1  = 2
	Buffer1  = 2
	buffer1  = 2
	BUF1     = 2
	Buf1     = 2
	buf1     = 2
	SWITCH   = 3
	Switch   = 3
	switch   = 3

class Ansi(StrEnum):
	ESC     = '\x1b'
	CSI     = ESC+'['
	OSC     = ESC+']'
	APC     = ESC+'_'
	ST      = ESC+'\\'
	show    = CSI+'?25h'
	hide    = CSI+'?25l'
	SCROLL  = ESC+'M'
	LOC     = CSI+'6n'
	save    = ESC+'7'+CSI+'s'
	load    = ESC+'8'+CSI+'u'
	cls     = ESC+'2J'
	DEFBUF  = CSI+'?1049h'
	ALTBUF  = CSI+'?1049l'

	def __str__(s):
		return s.value
	def __repr__(s):
		return repr(s.value)
	def parser(s,term):
		from libTerm.types.parsers import LOCparser
		parsers={
			'LOC': LOCparser(term)
		}
		return parsers.get(s.name)

	def __call__(self, *args, **kwargs):
		print(self.value, end='', flush=True)


class Move(StrEnum):
	CSI   = Ansi.CSI
	UP    = CSI+'{N}A'
	DOWN  = CSI+'{N}B'
	RIGHT = CSI+'{N}C'
	PREV  = CSI+'{N}E'
	LEFT  = CSI+'{N}D'
	NEXT  = CSI+'{N}F'
	COL   = CSI+'{X}G'
	ABS   = CSI+'{Y};{X}H'

	def __str__(s):
		return s()
	def __repr__(s):
		return repr(s.value)
	def __call__(s, *a):
		from libTerm.types import Coord
		CSI=s.CSI
		if s.value == Move.ABS:
			if not isinstance(a[0],Coord):
				coord=Coord(a[0],a[1])
			else:
				coord=a[0]
			result=s.value.format(CSI=CSI,**coord)
		else:
			N = a[0]
			result=s.value.format(CSI=CSI,N=N)
		return result


