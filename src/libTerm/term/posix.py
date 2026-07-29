#!/usr/bin/env python
import termios,os,sys,atexit

from libTerm.components.structs import TermTty
from libTerm.term.base import baseTerm
from libTerm.components import TermAttrs,TermBuffers,TermSize,TermModes,TermColors,Cursor
from libTerm.components import Buffer,Mode,Ansi
# Indices for termios list.
IFLAG = 0;OFLAG = 1;CFLAG = 2;LFLAG = 3;ISPEED = 4;OSPEED = 5;CC = 6
TCSAFLUSH = termios.TCSAFLUSH;ECHO = termios.ECHO;ICANON = termios.ICANON
VMIN = 6;VTIME = 5


class Term(baseTerm):
	MODE = Mode
	BUFFER = Buffer
	ANSI = Ansi

	def __init__(s,*a,**k):
		s.pid = os.getpid()
		s.ppid = os.getppid()


		s.tty=None
		s.attr=None
		s.buffers=None
		s.colors=None
		s.cursor=None
		s.modes=None
		s.size=None


		# Components
		s.tty = TermTty(term=s)
		s.attr = TermAttrs(term=s)
		s.buffers = TermBuffers(term=s)
		s.modes = TermModes(term=s)
		s.colors = TermColors(term=s)
		s.size = TermSize(term=s)
		s.cursor = Cursor(term=s)

		# shortcuts





	def __cleanup__(s):
		if s.mode is not None:
			s.modes.set(s.MODE.NORMAL)


	@property
	def mode(s):
		return s.modes.current

	@mode.setter
	def mode(s, mode):
		s.modes.set(mode)

	@property
	def buffer(s):
		return s.buffers.name

	@buffer.setter
	def buffer(s,buffer):
		s.buffers.set(buffer)


