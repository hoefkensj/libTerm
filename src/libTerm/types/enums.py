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
		CSI=s.CSI
		if s.value == Move.ABS:
			X=a[0]
			Y=a[1]
			result=s.value.format(CSI=CSI,X=X,Y=Y)
		else:
			N = a[0]
			result=s.value.format(CSI=CSI,N=N)
		return result


