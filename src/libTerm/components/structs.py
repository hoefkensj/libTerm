 #!/usr/bin/env python
import sys
from os import get_terminal_size
from time import time_ns
from libTerm.types.color import Color
from libTerm.types.enums import Ansi

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

	COLOR=Color
	ANSI=Ansi
	def __init__(s, **k):
		s.term = k.get('term')
		s.grounds={'fg': s.ANSI.COLFG,'bg':s.ANSI.COLBG}
		s._swaped=False
		s.fg = s.COLOR(192,192,192)
		s.bg = s.COLOR(16, 16, 16)
		s.init = s._update_()

	@staticmethod
	def _ansiparser_():
		buf = ''
		try:
			for i in range(23):
				buf += sys.stdin.read(1)
			rgb = buf.split(':')[1].split('/')
			rgb = [int(i, base=16) for i in rgb]
			rgb = TermColors.COLOR.Color(*rgb, 16)
		except Exception as E:
			# print(E)
			rgb = None
		return rgb

	def _update_(s):

		for ground in s.grounds:
			result = None
			while not result:
				result = s.term.stdin.query(s.grounds[ground])
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
	from libTerm.types.enums import Buffer,Ansi
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
	from libTerm.types.enums import Mode
	MODE=Mode
	def __init__(s,term):
		s.term=term
		s.mode=s.MODE.NONE

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
	from libTerm.types.base import Coord
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
