 #!/usr/bin/env python
import sys
from os import get_terminal_size
from time import time_ns

from libTerm.types import Coord,Color
from libTerm.types.enums import Ansi,Buffer,Mode


class TermAttrs():
	def __init__(s,**k):
		s.term=k.get('term')
		s.stack=[]
		s.active=s.term.tcgetattr()
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


class TermColors():
	def __init__(s, **k):
		s.term = k.get('term')
		s._specs = {'fg': 10, 'bg': 11,'swap':7,'unswap':27}
		s._ansi_q = '\x1b]{spec};?\a'
		s._ansi_a = '\x1b[{spec}m'
		s._swaped=False
		s.fg = Color(192,192,192)
		s.bg = Color(16, 16, 16)
		s.init = s._update_()

	@staticmethod
	def _ansiparser_():
		buf = ''
		try:
			for i in range(23):
				buf += sys.stdin.read(1)
			rgb = buf.split(':')[1].split('/')
			rgb = [int(i, base=16) for i in rgb]
			rgb = Color(*rgb, 16)
		except Exception as E:
			# print(E)
			rgb = None
		return rgb

	def _update_(s):
		for ground in ['fg','bg']:
			result = None
			while not result:
				result = s.term._ansi_(s._ansi_q.format(spec=s._specs[ground]), s._ansiparser_)
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


class TermBuffers:
	def __init__(s,term):
		s.term=term
		s.current=0

	def bufDefault(s):
		Ansi.DEFBUF()
	def bufAlternate(s):
		Ansi.ALTBUF()

	@property
	def buffer(s):
		return s.current

	@buffer.setter
	def buffer(s,buffer):
		s.set(buffer)

	def set(s,buffer=None):
		if buffer==0:
			s.bufDefault()
		elif buffer==Buffer.SWITCH:
			s.switch()
		elif buffer==Buffer.DEFAULT:
			s.bufDefault()
		elif buffer==Buffer.ALTERNATE:
			s.bufAlternate()
		return s.current

	def switch(s):
		if s.current==Buffer.DEFAULT:
			s.bufAlternate()
		if s.current==Buffer.ALTERNATE:
			s.bufDefault()



class TermModes:
	def __init__(s,term):
		s.term=term
		s.current=Mode.NONE


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
		s.term.tcsetattr(s.term.attr.init)
		s.current = Mode.NORMAL
		s.term._mode = s.current

	def modeCtl(s):
		s.term.cursor.show(False)
		s.term.echo = False
		s.term.canonical = False
		s.current=Mode.CONTROL
		s.term._mode = s.current

	def set(s,mode=None):

		if mode is None:
			mode = s.current
		elif mode == Mode.NONE:
			s.modeNormal()
		elif mode==Mode.NORMAL:
			s.modeNormal()
		elif mode==Mode.CONTROL:
			s.modeCtl()
		return s.current


class TermSize():
	def __init__(s, **k):

		s.term = k.get('term')
		s.time = None
		s.last = None
		s.xy = Coord(1, 1)
		s._tmp = Coord(1, 1)
		s.rows = 1
		s.cols = 1

		s.history = []
		s.changed = False
		s.changing = False
		s.__kwargs__(**k)
		s.__update__()

	def getsize(s):
		try:
			size = get_terminal_size()
			return size.columns, size.lines
		except OSError:
			return 80, 24

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
		return Coord(s.rows,s.cols )

	def __kwargs__(s, **k):
		s.term = k.get('term')

	def __update__(s):
		if s.time is None:
			s.last = time_ns()
		size = Coord(*s.getsize())
		if size == Coord(0, 0):
			size=Coord(80, 24)
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
