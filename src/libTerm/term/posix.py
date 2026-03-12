#!/usr/bin/env python
import os
import termios
import atexit
import sys
from abc import ABCMeta, abstractmethod
from libTerm.types import Mode
from libTerm.types.enums import Ansi
from libTerm.term.cursor import Cursor
from libTerm.term.input import Stdin
from libTerm.term.structs import TermAttrs, TermBuffers, TermColors, TermSize

# Indices for termios list.
IFLAG = 0;OFLAG = 1;CFLAG = 2;LFLAG = 3;ISPEED = 4;OSPEED = 5;CC = 6
TCSAFLUSH = termios.TCSAFLUSH;ECHO = termios.ECHO;ICANON = termios.ICANON
VMIN = 6;VTIME = 5


class baseTerm(metaclass=ABCMeta):
	Ansi= Ansi
	MODE= Mode

	def __init__(s,*a,**k):
		s.pid       = os.getpid()
		s.ppid      = os.getppid()
		s.stdfd     = [None, None, None]
		s.tty       = None
		s.attr      = None
		if s.isatty():
		# with suppress(io.UnsupportedOperation,OSError):
			s.stdfd        = [sys.stdin.fileno(),sys.stdout.fileno(),sys.stderr.fileno()]
			s.tty     	  = os.ttyname(s.stdfd[0])
		else:
			sys.__stdin__.fileno()
		s.attr = TermAttrs(term=s)

		s._mode     = s.MODE.NONE
		s._echo		= True
		s._canon    = True
		s.stdin		= Stdin(term=s)
		# s.stdout	= Stdout(term=s)
		s.cursor    = Cursor(term=s)
		# s.vcursors  = {0:vCursor(s,s.cursor)}
		s.size      = TermSize(term=s)
		s.color     = TermColors(term=s)
		s.buffer	= TermBuffers(term=s)
		atexit.register(s.setmode,Mode.NORMAL)

	def isatty(s):
		s._isatty=[sys.stdin.isatty(),sys.stdout.isatty(),sys.stderr.isatty()]
		return any(s._isatty)

	@abstractmethod
	def tcgetattr(s):
		pass

	@abstractmethod
	def tcsetattr(s, attr, when):
		pass

	@abstractmethod
	def setraw(s, when):
		"""Put terminal into raw mode."""
		pass

	@abstractmethod
	def setcbreak(s, when):
		"""Put terminal into cbreak mode."""
		pass

	@abstractmethod
	def setmode(s, mode):
		pass

	@abstractmethod
	def _update_(s, when):
		pass

	@abstractmethod
	def _ansi_(s, ansi, parser):
		pass

	@property
	def mode(s):
		return s._mode

	@mode.setter
	def mode(s, mode):
		s.setmode(mode)

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


class Term(baseTerm):

	def tcgetattr(s):
		return termios.tcgetattr(s.stdfd[0])

	def tcsetattr(s,attr,when=TCSAFLUSH):
		termios.tcsetattr(s.stdfd[0],when,attr)

	def setraw(s, when=TCSAFLUSH):
		"""Put terminal into raw mode."""
		from termios import IGNBRK,BRKINT,IGNPAR,PARMRK,INPCK,ISTRIP,INLCR,IGNCR,ICRNL,IXON,IXANY,IXOFF,OPOST,PARENB,CSIZE,CS8,ECHO,ECHOE,ECHOK,ECHONL,ICANON,IEXTEN,ISIG,NOFLSH,TOSTOP
		s.attr.stage()
		# Clear all POSIX.1-2017 input mode flags.
		# See chapter 11 "General Terminal Interface"
		# of POSIX.1-2017 Base Definitions.
		s.attr.staged[IFLAG] &= ~(IGNBRK | BRKINT | IGNPAR | PARMRK | INPCK | ISTRIP | INLCR | IGNCR | ICRNL | IXON
								  | IXANY | IXOFF)
		# Do not post-process output.
		s.attr.staged[OFLAG] &= ~OPOST
		# Disable parity generation and detection; clear character size mask;
		# let character size be 8 bits.
		s.attr.staged[CFLAG] &= ~(PARENB | CSIZE)
		s.attr.staged[CFLAG] |= CS8
		# Clear all POSIX.1-2017 local mode flags.
		s.attr.staged[LFLAG] &= ~(ECHO | ECHOE | ECHOK | ECHONL | ICANON | IEXTEN | ISIG | NOFLSH | TOSTOP)
		# POSIX.1-2017, 11.1.7 Non-Canonical Mode Input Processing,
		# Case B: MIN>0, TIME=0
		# A pending read shall block until MIN (here 1) bytes are received,
		# or a signal is received.
		s.attr.staged[CC] = list(s.attr.staged[CC])
		s.attr.staged[CC][VMIN] = 1
		s.attr.staged[CC][VTIME] = 0
		s._update_(when)

	def setcbreak(s,when=TCSAFLUSH):
		"""Put terminal into cbreak mode."""
		# this code was lifted from the tty module and adapted for being a method
		s.attr.stage()
		# Do not echo characters; disable canonical input.
		s.attr.staged[LFLAG] &= ~(ECHO | ICANON)
		# POSIX.1-2017, 11.1.7 Non-Canonical Mode Input Processing,
		# Case B: MIN>0, TIME=0
		# A pending read shall block until MIN (here 1) bytes are received,
		# or a signal is received.
		s.attr.staged[CC] = list(s.attr.staged[CC])
		s.attr.staged[CC][VMIN] = 1
		s.attr.staged[CC][VTIME] = 0
		s._update_(when)

	def setmode(s, mode=None):
		def Normal():
			s.cursor.show(True)
			s.echo = True
			s.canonical = True
			s.tcsetattr(s.attr.init)
			s._mode = Mode.NORMAL

		def Ctl():
			s.cursor.show(False)
			s.echo = False
			s.canonical = False
			s._mode = Mode.CONTROL

		if mode is None:
			mode = s._mode
		if isinstance(mode, str):
			if mode.casefold().startswith('n'):
				mode = Mode.NORMAL
			elif mode.casefold().startswith('c'):
				mode = Mode.CONTROL

		if mode is not None and mode != Mode.NONE:
			{1: Normal, 2: Ctl}.get(mode)()
		return s._mode

	def _update_(s, when=TCSAFLUSH):
		s.tcsetattr(s.attr.staged, when)
		s.attr.update(s.tcgetattr())

	def _ansi_(s, ansi, parser):
		s.setcbreak()
		try:
			sys.stdout.write(ansi)
			sys.stdout.flush()
			result = parser()
		finally:
			s.tcsetattr(s.attr.restore())
		return result
#
