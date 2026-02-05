# /usr/bin/env pyhthon
import io
import os
import termios
import atexit
import sys
from contextlib import suppress
from libTerm.types.base import Size
from libTerm.types.base import Mode
from libTerm.term.cursor import  Cursor
from libTerm.term.input import  Stdin


# Indices for termios list.
IFLAG = 0
OFLAG = 1
CFLAG = 2
LFLAG = 3
ISPEED = 4
OSPEED = 5
CC = 6
TCSAFLUSH = termios.TCSAFLUSH
ECHO = termios.ECHO
ICANON = termios.ICANON

VMIN = 6
VTIME = 5
from libTerm.term.posix import Term
class VirtTermAttrs():
	def __init__(s,term,**k):
		s.stored=[0,0,0,0,0,0,[0,0,0,0,0,0,0,0]]
		s.term=term
		s.stack=[]
		s.active=[0,0,0,0,0,0,[0,0,0,0,0,0,0,0]]
		s.init=list([*s.active])
		s.stack+= [list(s.active)]
		s.staged=None

	def stage(s):
		s.staged=list(s.active)
	def update(s,new=None):
		if new is None:
			new=s.staged
		s.stack+=[list(s.active)]
		s.active=new
		s.staged=None
	def restore(s):
		if s.stack:
			s.staged=s.stack.pop()
		return s.staged


class VirtTerm(Term):
	MODE = Mode

	def __init__(s, *a, **k):
		s.pid = os.getpid()
		s.ppid = os.getpid()
		s.fd = sys.__stdin__.fileno()
		s.attr = None
		with suppress(io.UnsupportedOperation, OSError):
			s.tty = os.ttyname(s.fd)
		s.attr = VirtTermAttrs(term=s)

		s._mode = s.MODE.NONE
		s._echo = True
		s.cursor = Cursor(term=s)
		# s.vcursors  = {0:vCursor(s,s.cursor)}
		s.size = Size(term=s)
		s.stdin = Stdin(term=s)
		s.color = TermColors(term=s)
		s.buffer = TermBuffers(term=s)
		atexit.register(s.setmode, s.MODE.NORMAL)

	def tcgetattr(s):
		return

	def tcsetattr(s, attr, when=TCSAFLUSH):
		pass

	def setraw(s, when=TCSAFLUSH):
		"""Put terminal into raw mode."""
		from termios import IGNBRK, BRKINT, IGNPAR, PARMRK, INPCK, ISTRIP, INLCR, IGNCR, ICRNL, IXON, IXANY, IXOFF, OPOST, PARENB, CSIZE, CS8, ECHO, ECHOE, ECHOK, ECHONL, ICANON, IEXTEN, ISIG, NOFLSH, TOSTOP
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

	def setcbreak(s, when=TCSAFLUSH):
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

	@property
	def echo(s):
		return s._echo

	@echo.setter
	def echo(s, enable=False):
		s.attr.stage()
		s.attr.staged[3] &= ~ECHO
		if enable:
			s.attr.staged[3] |= ECHO
		s._update_()

	def canonical(s, enable=True):
		s.attr.stage()
		s.attr.staged[3] &= ~ICANON
		if enable:
			s.attr.staged[3] |= ICANON
		s._update_()

	@property
	def mode(s):
		return s._mode

	@mode.setter
	def mode(s, mode):
		s.setmode(mode)

	def setmode(s, mode=Mode.NONE):
		def Normal():
			s.cursor.show(True)
			s.echo = True
			s.canonical(True)
			s.tcsetattr(s.attr.init)
			s._mode = Mode.NORMAL

		def Ctl():
			s.cursor.show(False)
			s.echo = False
			s.canonical(False)
			s._mode = Mode.CONTROL

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

#

# Expose a Term symbol so importing `Term` from this module works in tests

