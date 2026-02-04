# /usr/bin/env pyhthon
from os import get_terminal_size
from time import time_ns

from libTerm.types.coord import Coord


class Size():
	def __init__(s, **k):
		s.term = k.get('term')
		s.getsize = get_terminal_size
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
		return (s.cols, s.rows)

	def __kwargs__(s, **k):
		s.term = k.get('term')

	def __update__(s):
		if s.time is None:
			s.last = time_ns()
		size = Coord(*s.getsize())
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
