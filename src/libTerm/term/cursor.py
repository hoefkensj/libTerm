

from collections import namedtuple
import re
from libTerm.term.types import Coord
from time import time_ns
import sys

from dataclasses import dataclass
from enum import Enum
@dataclass()
class Move(str,Enum):
	abs= '\x1b[{Y};{X}H'
	up= '\x1b[{Y}A'
	down= '\x1b[{Y}B'
	right= '\x1b[{X}C'
	left= '\x1b[{X}D'
	prev= '\x1b[{Y}E'
	next= '\x1b[{Y}F'
	col= '\x1b[{X}G'

	def __str__(self):
		return self.value
	def __repr__(self):
		return repr(self.value)
	def __call__(self, *a, **k):
		X=k.get('X')
		Y=k.get('Y')
		if 'X' in str(self.value):
			if X is None:
				X=(1*(len(a)==0)) or a[0]

		if 'Y' in str(self.value):
			if Y is None:
				Y=((a[1]*(len(a)>1))+
				   (a[0]*(len(a)==1)))

		tplvars={'X':X,'Y':Y}
		string=str(self.value).format(**tplvars)
		return string

@dataclass()
class ANSI_Cursor(str, Enum):
	show = '\x1b[?25h'
	hide = '\x1b[?25l'
	scrup= '\x1bM'
	getxy= '\x1b[6n'
	# savxy= '7','[s'
	# rstxy= '8','[u'

	def __str__(self):
		return self.value
	def __repr__(self):
		return repr(self.value)
	def __call__(self):
		print(str(self.value), end='', flush=True)

class Cursor():
	def __init__(__s, term):
		super().__init__()
		__s.term = term
		__s.ansi = ANSI_Cursor
		__s.move = Move
		__s.re = re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R", re.VERBOSE)
		__s._xy=Coord(0,0)
		__s.store=Store()
		__s.visible=True
		__s.hidden=False
#TODO:		__s.stamp=time_ns()
#TODO:		__s.moved=False
#TODO:		__s._history = [*(None,) * 64]
		__s.init = __s.__update__()

	@property
	def xy(__s):
		return __s.__update__()

	@xy.setter
	def xy(__s,coord):
		print('\x1b[{y};{x}H'.format(**coord), end='', flush=True)
		__s.__update__()

	def stored(__s):
		return __s.store.stored

	def __update__(__s):
		def Parser():
			buf = ' '
			while buf[-1] != "R":
				buf += sys.stdin.read(1)
			# reading the actual values, but what if a keystroke appears while reading
			# from stdin? As dirty work around, getpos() returns if this fails: None
			try:
				groups = __s.re.search(buf).groupdict()
				result = Coord(int(groups['X']), int(groups['Y']))
			except AttributeError:
				result = None
			return result

		result = None
		timeout = {}
		timeout['limit'] = 500
		timeout['start'] = time_ns() // 1e6
		timeout['running'] = 0
		while not result:
			result = __s.term.ansi(__s.ansi.getxy, Parser)
		__s._xy =result
		return result

	def show(__s, state=True):
		if __s.hidden and state:
			__s.ansi.show()
			__s.hidden=False
			__s.visible=True
		if __s.visible and not state:
			__s.ansi.hide()
			__s.hidden=True
			__s.visible=False


	def hide(__s, state=True):
		if __s.visible and state:
			__s.show(False)
		if __s.hidden and not state:
			__s.show(True)

	@property
	def x(__s):
		x=__s.xy.x
		return x

	@property
	def y(__s):
		y=__s.xy.y
		return y


#TODO: class vCursor(Cursor):
# 	def __init__(__s, term,cursor):
# 		__s.term = term
# 		__s.realcursor=cursor
# 		__s.position = Coord(__s.realcursor.x,__s.realcursor.y)
# 		__s.history = [*(None,) * 64]
# 		__s.controled = False
# 		__s.bound = True
# 		__s.frozen = False
# 		__s.init = __s.__update__()#
# 	def freeze(__s, state=True):
# 		if state:
# 			__s.frozen = True
# 			__s.bind(False)
# 			__s.control(False)
# 		else:
# 			__s.frozen = False#
# 	def __update__(__s, get='XY'):
# 		pass#
# 	def show(__s, state=True):
# 		if state:
# 			print('\x1b[?25h', end='', flush=True)
# 		else:
# 			__s.hide()#
# 	def hide(__s, state=True):
# 		if state:
# 			import atexit
# 			print('\x1b[?25l', end='', flush=True)
# 			atexit.register(__s.show)
# 		else:
# 			__s.show()
#
