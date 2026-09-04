 #!/usr/bin/env python
import sys,os,termios
from os import get_terminal_size
from libTerm.components.rgbcolor import RGBColor
from libTerm.components.enums import Ansi
from libTerm.components import Input,Output
import asyncio
from abc import ABCMeta, abstractmethod
from enum import IntEnum
import pty
import subprocess

# Indices for termios list.
IFLAG = 0;OFLAG = 1;CFLAG = 2;LFLAG = 3;ISPEED = 4;OSPEED = 5;CC = 6
TCSAFLUSH = termios.TCSAFLUSH;ECHO = termios.ECHO;ICANON = termios.ICANON
VMIN = 6;VTIME = 5


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
		s.active=[]
		s.init=[]
		s.staged=[]
		s.attrs={}
		if s.term.tty.isatty:
			s.__startup__()
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
	def __startup__(s):
		s.active=s.get()
		s.init=list([*s.active])
		s.stack+= [list(s.active)]

	def get(s):
		return termios.tcgetattr(s.term.tty.input.fileno())

	def set(s,attr,when=TCSAFLUSH):
		termios.tcsetattr(s.term.tty.input.fd,when,attr)

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

	@property
	def echo(s):
		s._echo=s.active[LFLAG] & ECHO != 0
		return s._echo

	@echo.setter
	def echo(s, enable=False):
		s.stage()
		s.staged[3] &= ~ECHO
		if enable:
			s.staged[3] |= ECHO
		s._update_()
		s._echo=enable

	@property
	def canonical(s):
		s._canon = s.active[LFLAG] & ICANON != 0
		return s._canon

	@canonical.setter
	def canonical(s, enable=True):
		s.stage()
		s.staged[3] &= ~ICANON
		if enable:
			s.staged[3] |= ICANON
		s._update_()
		s._canon=enable

class TermColors():

	COLOR=RGBColor
	ANSI=Ansi
	def __init__(s, **k):
		s.term = k.get('term')
		s._specs = {'_fg': s.ANSI.COLFG, '_bg': s.ANSI.COLBG,'swap':7,'unswap':27}
		s._ansi_a = '\x1b[{spec}m'
		s._swapped=False
		s._fg = None
		s._bg = None
		s._colors=None



	def _postinit(s):
		if s.term.tty.isatty:
			s._update_()


	def _update_(s):
		s._colors={'fg': s.fg, 'bg': s.bg}

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
		s._fg = s.term.tty.input.query(s._specs['_fg'])
		return s._fg
	@property
	def bg(s):
		s._bg = s.term.tty.input.query(s._specs['_bg'])
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
	def __init__(s,**k):
		s.term=k.get('term')
		s._buffer=None
		s._name=None
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
	@property
	def name(s):
		return '.'.join([s.buffer.__class__.__name__, s._buffer.name])
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
		s.current=None

	@property
	def mode(s):
		return s.current
	@mode.setter
	def mode(s,mode):
		s.set(mode)

	def modeNormal(s):
		s.term.cursor.show=True
		s.term.attr.echo = True
		s.term.attr.canonical = True
		s.term.attr.set(s.term.attr.init)
		s.term.buffer=s.term.BUFFER.DEFAULT
		s.current = s.MODE.NORMAL
		s.term._mode = s.current

	def modeCtl(s):
		s.term.cursor.show(False)
		s.term.attr.echo = False
		s.term.attr.canonical = False
		s.current=s.MODE.CONTROL
		s.term._mode = s.current

	def set(s,mode=None):
		if s.term.tty.isatty:
			if mode is None:
				mode = s.current
			elif mode == s.MODE.NONE:
				pass
				# s.modeNormal()
			elif mode==s.MODE.NORMAL:
				s.modeNormal()
			elif mode==s.MODE.CONTROL:
				s.modeCtl()
			return s.current

class TermSize(metaclass=ABCMeta):
	from libTerm.components.base import Coord
	COORD=Coord

	def __new__(cls, **k):
		if cls is TermSize:
			if k.get('term').tty.output.isatty:
				cls=LiveTermSize
			else:
				cls=FixedTermSize
		return super().__new__(cls)

	def __init__(s, **k):
		s.term = k.get('term')
		s._timestamp=None
		s._livestamp=None
		s._timestamps=[]
		s._size = None

		s
		s.history={}
		s.changing=False
		s.changed=asyncio.Event()

	@property
	@abstractmethod
	def size(s):...

class LiveTermSize(TermSize):
	def __init__(s,**k):
		super().__init__(**k)
		s._fps=k.get('fps', 2)
		s._period= 1000*(s._fps**-1)
		s._oldsize=None
		s._rawsize=None
		s._livesize=None
		s.time=None

	@property
	def xy(s):
		return s.getsize()

	@property
	def size(s):
		s._rawsize=[*list(get_terminal_size())]
		s._size=s.COORD(*s._rawsize)
		return s._size

	def getsize(s):
		s._rawsize=[*list(get_terminal_size())]
		s._size=s.COORD(*s._rawsize)
		return s._size

class FixedTermSize(TermSize):
	def __init__(s,**k):
		super().__init__(**k)
		s._fixedsize=k.get('fixedsize',s.COORD(k.get('cols',80),k.get('rows',24)))
	def fixsize(s,size):
		s._fixedsize=size

	@property
	def size(s):
		s._size=s.COORD(*s._fixedsize)
		return s._size

	@property
	def xy(s):
		return s.getsize()

	def getsize(s):
		s._size=s._fixedsize
		return s._size

class VirtTTY:
	def __init__(s,**k):
		s.term=k.get('term')
		s.fdin=None
		s.fdout=None
		s.in_name=None
		s.out_name=None
		s.proc=None
		s.makepty()
		s.spawnshell()
		s.input=os.fdopen(s.fdin,'rb',0)
		s.output=os.fdopen(s.fdout,'wb',0)

	def makepty(s):
		s.fdin, s.fdout = pty.openpty()
		s.in_name = os.ttyname(s.fdin)
		s.out_name = os.ttyname(s.fdout)

	def spawnshell(s):
		s.proc = subprocess.Popen(
			['/bin/bash'],
			stdin=s.fdin,
			stdout=s.fdout,
			stderr=s.fdout,
			close_fds=True
		)
		# os.close(s.fdout)



	def close(s):
		# Terminate the shell
		os.write(s.fdin, b'exit\n')
		s.proc.wait()
		os.close(s.fdin)
	def cleanup(s):
		# Clean up
			os.close(s.fdin)
			os.close(s.fdout)
	# print("Shell Output:", output.decode().strip())
class RealTTY:
	def __init__(s,**k):
		s.term = k.get('term')
		s.fdin = sys.stdin.fileno()
		s.fdout = sys.stdout.fileno()
		s.in_name = os.ttyname(s.fdin)
		s.out_name = os.ttyname(s.fdout)
		s.input	=	sys.stdin
		s.output = sys.stdout

class TermTty:
	def __init__(s,**k):
		s.term=k.get('term')
		# s.virtual=VirtTTY(term=s.term)
		# if s.outistty and s.inistty:
		# 	s.tty = RealTTY(term=s.term)
		# else:
		# 	s.tty = s.virtual
		s.input=Input(term=s.term,tty=s)
		s.output=Output(term=s.term,tty=s)


	@property
	def isatty(s):
		return s.input.isatty and s.output.isatty

	def query(s,query):
		s.output.write(query)
		return s.input.read()

