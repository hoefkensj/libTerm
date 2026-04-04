 #!/usr/bin/env python
import sys,os,termios
from os import get_terminal_size
from time import time_ns
from libTerm.components.color import Color
from libTerm.components.enums import Ansi
# Indices for termios list.
IFLAG = 0;OFLAG = 1;CFLAG = 2;LFLAG = 3;ISPEED = 4;OSPEED = 5;CC = 6
TCSAFLUSH = termios.TCSAFLUSH;ECHO = termios.ECHO;ICANON = termios.ICANON
VMIN = 6;VTIME = 5

from enum import IntEnum

class IOFlag(IntEnum):
	IFLAG  = 0
	OFLAG  = 1
	CFLAG  = 2
	LFLAG  = 3
	ISPEED = 4
	OSPEED = 5
	CC     = 6

class TermAttrs():
	def __init__(s,**k):
		s.term=k.get('term')
		s.stack=[]
		s.active=s.get()
		s.init=list([*s.active])
		s.stack+= [list(s.active)]
		s.staged=None

		s.attrs={}

		# for attr in zip(IOFlag.)
		#
		#
		#
		# IFLAG:1280,
		# 		 OFLAG:5,
		# 		 CFLAG:983231,
		# 		LFLAG:35387,
		# 		ISPEED:15,
		# 		 OSPEED:15,
		# 		  CC:'[b'\x03',
		# 		   b'\x1c',
		# 		   b'\x7f',
		# 		   b'\x15',
		# 		   b'\x04',
		# 		   b'\x00',
		# 		   b'\x01',
		# 		   b'\x00',
		# 		   b'\x11',
		# 		   b'\x13',
		# 		   b'\x1a',
		# 		   b'\x00',
		# 		   b'\x12',
		# 		   b'\x0f',
		# 		   b'\x17',
		# 		   b'\x16',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00',
		# 		   b'\x00']]}

	def get(s):
		return termios.tcgetattr(s.term.stdfd[0])

	def set(s,attr,when=TCSAFLUSH):
		termios.tcsetattr(s.term.stdfd[0],when,attr)

	def setcbreak(s,when=TCSAFLUSH):
		"""Put terminal into cbreak mode."""
		# this code was lifted from the tty module and adapted for being a method
		s.stage()
		# Do not echo characters; disable canonical input.
		s.staged[LFLAG] &= ~(ECHO | ICANON)
		# POSIX.1-2017, 11.1.7 Non-Canonical Mode Input Processing,
		# Case B: MIN>0, TIME=0
		# A pending read shall block until MIN (here 1) bytes are received,
		# or a signal is received.
		s.staged[CC] = list(s.staged[CC])
		s.staged[CC][VMIN] = 1
		s.staged[CC][VTIME] = 0
		s.set(s.staged, when)
		s.update(s.get())

	def setraw(s, when=TCSAFLUSH):
		"""Put terminal into raw mode."""
		from termios import IGNBRK,BRKINT,IGNPAR,PARMRK,INPCK,ISTRIP,INLCR,IGNCR,ICRNL,IXON,IXANY,IXOFF,OPOST,PARENB,CSIZE,CS8,ECHO,ECHOE,ECHOK,ECHONL,ICANON,IEXTEN,ISIG,NOFLSH,TOSTOP
		s.stage()
		# Clear all POSIX.1-2017 input mode flags.
		# See chapter 11 "General Terminal Interface"
		# of POSIX.1-2017 Base Definitions.
		s.staged[IFLAG] &= ~(IGNBRK | BRKINT | IGNPAR | PARMRK | INPCK | ISTRIP | INLCR | IGNCR | ICRNL | IXON | IXANY | IXOFF)
		# Do not post-process output.
		s.staged[OFLAG] &= ~OPOST
		# Disable parity generation and detection; clear character size mask;
		# let character size be 8 bits.
		s.staged[CFLAG] &= ~(PARENB | CSIZE)
		s.staged[CFLAG] |= CS8
		# Clear all POSIX.1-2017 local mode flags.
		s.staged[LFLAG] &= ~(ECHO | ECHOE | ECHOK | ECHONL | ICANON | IEXTEN | ISIG | NOFLSH | TOSTOP)
		# POSIX.1-2017, 11.1.7 Non-Canonical Mode Input Processing,
		# Case B: MIN>0, TIME=0
		# A pending read shall block until MIN (here 1) bytes are received,
		# or a signal is received.
		s.staged[CC] = list(s.staged[CC])
		s.staged[CC][VMIN] = 1
		s.staged[CC][VTIME] = 0
		s._update_(when)

	def _update_(s, when=TCSAFLUSH):
		s.set(s.staged, when)
		s.update(s.get())

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


class TermColors():

	COLOR=Color
	ANSI=Ansi
	def __init__(s, **k):
		s.term = k.get('term')
		s._specs = {'_fg': s.ANSI.COLFG, '_bg': s.ANSI.COLBG,'swap':7,'unswap':27}
		s._ansi_a = '\x1b[{spec}m'
		s._swaped=False
		s._fg = s.COLOR(192,192,192)
		s._bg = s.COLOR(16, 16, 16)

	@staticmethod
	def _ansiparser_():
		buf = ''
		try:
			for i in range(23):
				buf += sys.stdin.read(1)
			rgb = buf.split(':')[1].split('/')
			rgb = [int(i, base=16) for i in rgb]
			rgb = TermColors.COLOR(*rgb, 16)
		except Exception as E:
			# print(E)
			rgb = None
		return rgb

	def _update_(s):
		for ground in ['_fg','_bg']:
			result = None
			while not result:
				result = s.term.stdin.query(s._specs[ground])
			s.__setattr__(ground, result)

		return {'fg': s.fg, 'bg': s.bg}

	def swap(s):
		swap=(7*(not s._swap))+(27*(s._swap))
		s._swap= not s._swap
		return '\x1b[{SWAP}m'.format(SWAP=swap)

	def invert(s):
		return '\x1b[{SWAP}m'.format(SWAP=7)

	def revert(s):
		return '\x1b[{SWAP}m'.format(SWAP=27)

	@property
	def fg(s):
		s._update_()
		return s._fg
	@property
	def bg(s):
		s._update_()
		return s._bg
	@fg.setter
	def fg(s,buffer):
		s.setfg(buffer)

	@bg.setter
	def bg(s, color):
		s.setbg(color)

	def setfg(s,color):
		s._fg=color
		print(color.ansifg,end='',flush=True)

	def setbg(s,color):
		s._bg=color
		print(color.ansibg,end='',flush=True)


class TermBuffers:
	from libTerm.components.enums import Buffer,Ansi
	BUFFER=Buffer
	ANSI=Ansi
	def __init__(s,term):
		s.term=term
		s._buffer=s.BUFFER.NONE

	def bufDefault(s):
		s._buffer=s.BUFFER.DEFAULT
		s.ANSI.DEFBUF()
	def bufAlternate(s):
		s._buffer=s.BUFFER.ALTERNATE
		s.ANSI.ALTBUF()

	@property
	def buffer(s):
		return s._buffer

	@buffer.setter
	def buffer(s,buffer):
		s.set(buffer)

	def set(s,buffer=None):
		if buffer==0:
			s.bufDefault()
		elif buffer==s.BUFFER.SWITCH:
			s.switch()
		elif buffer==s.BUFFER.DEFAULT:
			s.bufDefault()
		elif buffer==s.BUFFER.ALTERNATE:
			s.bufAlternate()
		return s._buffer

	def switch(s):
		if s._buffer==s.BUFFER.DEFAULT:
			s.bufAlternate()
		if s._buffer==s.BUFFER.ALTERNATE:
			s.bufDefault()



class TermModes:
	from libTerm.components.enums import Mode
	MODE=Mode
	def __init__(s,term):
		s.term=term
		s.mode=s.MODE.NONE
		s.current=None

	@property
	def mode(s):
		return s.current
	@mode.setter
	def mode(s,mode):
		s.set(mode)

	def modeNormal(s):
		s.term.cursor.show(True)
		s.term.echo = True
		s.term.canonical = True
		s.term.attr.set(s.term.attr.init)
		s.current = s.MODE.NORMAL
		s.term._mode = s.current

	def modeCtl(s):
		s.term.cursor.show(False)
		s.term.echo = False
		s.term.canonical = False
		s.current=s.MODE.CONTROL
		s.term._mode = s.current

	def set(s,mode=None):

		if mode is None:
			mode = s.current
		elif mode == s.MODE.NONE:
			s.modeNormal()
		elif mode==s.MODE.NORMAL:
			s.modeNormal()
		elif mode==s.MODE.CONTROL:
			s.modeCtl()
		return s.current


class TermSize():
	from libTerm.components.base import Coord
	COORD=Coord
	def __init__(s, **k):

		s.term = k.get('term')
		s.getsize = lambda:s.COORD(*list(get_terminal_size()))
		s.time = None
		s.last = None
		s.xy = s.COORD(1, 1)
		s._tmp = s.COORD(1, 1)
		s.rows = 1
		s.cols = 1

		s.history = []
		s.changed = False
		s.changing = False
		s.__kwargs__(**k)
		s.__update__()

	@property
	def width(s):
		s.__update__()
		return s.cols

	@property
	def height(s):
		s.__update__()
		return s.rows

	@property
	def rc(s):
		s.__update__()
		return s.COORD(s.rows,s.cols )

	def __kwargs__(s, **k):
		s.term = k.get('term')

	def __update__(s):
		if s.time is None:
			s.last = time_ns()
		size = s.COORD(*s.getsize())
		if size == s.COORD(0, 0):
			size=s.COORD(80, 24)
		if size != s.xy:

			if size != s._tmp:
				s.changing = True
				s._tmp = size
				s._tmptime = time_ns()
			if size == s._tmp:
				if (time_ns() - s._tmptime) * 1e6 > 500:
					s.changing = False
					s.changed = True
					s.history += [s.xy]
					s.xy = size
					s.rows = s.xy.y
					s.cols = s.xy.x
				else:
					s._tmp = size
		if size == s.xy:
			s.changed = False
