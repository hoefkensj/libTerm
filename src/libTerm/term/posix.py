#!/usr/bin/env python
import termios,os,sys,atexit
from libTerm.term.base import baseTerm
from libTerm.components import TermAttrs,TermBuffers,TermSize,TermModes,TermColors,Cursor,Stdin
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
		s.stdfd = [sys.stdin.fileno(),
				   sys.stdout.fileno(),
				   sys.stderr.fileno()]
		s.tty = os.ttyname(s.stdfd[0])
		s._echo = True
		s._canon = True
		# Components
		s.stdin = Stdin(term=s)
		s.attr = TermAttrs(term=s)
		s.buffers = TermBuffers(term=s)
		s.colors = TermColors(term=s)
		s.cursor = Cursor(term=s)
		s.modes = TermModes(term=s)
		s.size = TermSize(term=s)
		atexit.register(s.modes.set, s.MODE.NORMAL)






	def _update_(s, when=TCSAFLUSH):
		s.attr.set(s.attr.staged, when)
		s.attr.update(s.attr.get())


	@property
	def mode(s):
		return s.modes.current

	@mode.setter
	def mode(s, mode):
		s.modes.set(mode)
	@property
	def buffer(s):
		return s.buffers._buffer

	@buffer.setter
	def buffer(s,buffer):
		s.buffers.set(buffer)

	@property
	def echo(s):
		s._echo=s.attr.active[LFLAG] & ECHO != 0
		return s._echo

	@echo.setter
	def echo(s, enable=False):
		s.attr.stage()
		s.attr.staged[3] &= ~ECHO
		if enable:
			s.attr.staged[3] |= ECHO
		s._update_()
		s._echo=enable

	@property
	def canonical(s):
		s._canon = s.attr.active[LFLAG] & ICANON != 0
		return s._canon

	@canonical.setter
	def canonical(s, enable=True):
		s.attr.stage()
		s.attr.staged[3] &= ~ICANON
		if enable:
			s.attr.staged[3] |= ICANON
		s._update_()
		s._canon=enable

