#/usr/bin/env python
from collections import namedtuple
from dataclasses import dataclass, field
from enum import IntEnum
from os import get_terminal_size
from time import time_ns


# class Selector():
#
# 	def __init__(s,n,start=1):
# 		s.selection = start
# 		s.n=n
# 		s.prev = lambda:
# 		s.next = lambda: s.selector(+1)
# 		s.read = lambda: s.selector(0)
# 		s.write = s.setval
# 	def prev(s):
# 		return s.selector(-1)
# 	def next(s):
# 		return s.selector(11)
# 	def prev(s):
# 		return s.selector(-1)
#
# 	def wrap(s, ss):
# 		return  ~(~ss * -~-s.n) % s.n
#
# 	def selector(s,i):
# 		s.selection = s.wrap(s.selection + i)
# 		return s.selection
#
# 	def setval(s,i):
# 		s.selection = s.wrap(i)
# 		return s.selection
# 	@property
# 	def ceiling(s):
# 		return s.n
#
# 	@ceiling.setter
# 	def ceiling(s,value):
# 		s.n=value


@dataclass(frozen=True)
class Color:
	R: int = field(default=0, metadata={'range': (0, 4294967296)})
	G: int = field(default=0, metadata={'range': (0, 4294967296)})
	B: int = field(default=0, metadata={'range': (0, 4294967296)})
	BIT: int = field(default=8, metadata={'set': (4, 8, 16, 32)})

	def __post_init__(self):
		if self.BIT not in (4, 8, 16, 32):
			raise ValueError(f"BIT must be one of 4,8,16,32. Got {self.BIT}")

		max_val = (1 << self.BIT) - 1

		for ch in ("R", "G", "B"):
			v = getattr(self, ch)
			if not isinstance(v, int) or not (0 <= v <= max_val):
				raise ValueError(f"{ch} must be 0..{max_val} for {self.BIT}-bit input")

		# convert input into internal 32-bit by left-shifting
		shift = 32 - self.BIT
		object.__setattr__(self, "R", self.R << shift)
		object.__setattr__(self, "G", self.G << shift)
		object.__setattr__(self, "B", self.B << shift)
		object.__setattr__(self, "BIT", 32)

	def __invert__(s):
		R=4294967296-s.R
		G=4294967296-s.G
		B=4294967296-s.B
		return Color(R,G,B,32)
	# ----- Internal storage -----
	@property
	def RGB32(self):
		return self.R, self.G, self.B

	# ----- Truncated outputs -----
	@property
	def RGB16(self):
		return tuple(v >> 16 for v in self.RGB32)

	@property
	def RGB8(self):
		return tuple(v >> 24 for v in self.RGB32)

	@property
	def RGB4(self):
		return tuple(v >> 28 for v in self.RGB32)

	# ----- ANSI decimal output -----
	def ansi(self, bits: int = 8) -> str:
		if bits == 32:
			rgb = self.RGB32
		elif bits == 16:
			rgb = self.RGB16
		elif bits == 8:
			rgb = self.RGB8
		elif bits == 4:
			rgb = self.RGB4
		else:
			raise ValueError("bits must be 4,8,16,32")

		return ";".join(str(v) for v in rgb)
	@property
	def neg(s):
		return s.__invert__()


@dataclass(frozen=True)
class Coord(namedtuple('Coord', ['x', 'y'])):
	__module__ = None
	__qualname__='Coord'
	_x: int = field(default=0)
	_y: int = field(default=0)



	def __str__(s):
		return f'\x1b[{s.y + 1};{s.x + 1}H'

	def __repr__(s):
		return f'{s.__class__.__name__}({s.x}, {s.y})'

	def __len__(s):
		return 2
	def __iter__(s):
		yield s.x
		yield s.y
	def __getitem__(s, index):
		value=None
		if isinstance(index, int):
			value=(((index == 0)*s.x)+((index == 1)*s.y))
		elif isinstance(index, str):
			value = (((index == 'x') * s.x) + ((index == 'y') * s.y))
		if value is None:
			raise KeyError('index must be int 0 or 1 or str "x" or "y" ')
		return value
	def __add__(s, other):
		if isinstance(other,Coord):
			x=s.x+other.x
			y=s.y+other.y
		elif isinstance(other,complex):
			x=s.x+other.real
			y=s.y+other.imag

		elif isinstance(other,str):
			return f'{s.__str__()}{other}'
		else:
			raise TypeError(f'cannot add {type(s)} to {type(other)}{{EXTRA}}')

		return Coord(x, y)

	def __eq__(s,other):
		error=lambda :f'cannot compare {type(s)} to {type(other)}'
		if isinstance(other,Coord):
			result=(s.x==other.x)*(s.y==other.y)
		elif isinstance(other,complex):
			result=(s.real==other.real)*(s.imag==other.imag)
		elif isinstance(other,tuple):
			if len(other)!=2:
				raise error().format(EXTRA=f' of length {len(other)}')
			result=(s.x==other[0])*(s.y==other[1])
		elif isinstance(other,list):
			if len(other)!=2:
				raise TypeError(error().format(EXTRA=f' of length {len(other)}'))
			result=(s.x==other[0])*(s.y==other[1])
		elif isinstance(other,set):
			if len(other)!=2:
				raise TypeError(error().format(EXTRA=f' of length {len(other)}'))
			result=(s.x==other[0])*(s.y==other[1])
		else:
			raise TypeError(error().format(EXTRA=''))
		return result

	def __complex__(s):
		return complex(real=s.x,imag=s.y)

	@property
	def real(s):
		return s.x

	@property
	def imag(s):
		return s.y

	def keys(s):
		return ('x', 'y')


	@property
	def xy(s) -> tuple[int, int]:
		return (s.x, s.y)

	@property
	def y(s):
		return s._y

	@property
	def x(s):
		return s._x


class Mode(IntEnum):
	NONE	= 0
	none	= 1
	NRML	= 1
	nrml	= 1
	NORMAL  = 1
	normal  = 1
	DEFAULT = 1
	default = 1
	CTL	 = 2
	ctl	 = 2
	CTRL	= 2
	ctrl	= 2
	CONTROL = 2
	control = 2
	inp     = 3
	Inp     = 3
	Input   = 3
	INP      = 3
	INPUT      = 3


class Selector:
	"""Cyclic Selector,configurable range and step-size
		note: a range of (1,10) includes both 1 and 10:
		10 <- 1 2 3 4 5 6 7 8 9 10 ->1
	"""
	def __init__(s,rnge,dn=-1,up=1,start=0,parent=None):
		s.parent=parent
		s.step={}
		s.step['dn']= None
		s.step['up']= None
		s._shift = 0
		s._rnge = 0
		if isinstance(rnge,float|int):
			rnge=(0,rnge)
		s.setrange(rnge)
		s.setstep(dn,up)
		s._up=s._wrapper(s.step['up'])
		s._dn=s._wrapper(s.step['dn'])
		s._wr=s._wrapper(0)
		s._value = s._wr(start-s._shift)

	def _update_wrappers(s):
		s._up=s._wrapper(s.step['up'])
		s._dn=s._wrapper(s.step['dn'])
		s._wr=s._wrapper(0)

	def _wrapper(s,i):
		def wrap(v):
			return ~(~(v + i) * -~-s._rnge) % (s._rnge)
		return wrap
	@property
	def range(s):
		o=s._shift
		r=s._rnge-1
		rnge=(o,r+o)
		return rnge

	def setrange(s,span):
		bot,top=span
		top+=1
		s._rnge=top-bot
		s._shift=bot
		s._update_wrappers()

	def setstep(s,dn=None,up=None):
		if dn is None and s.step['dn'] is None:
			s.step['dn']=-1
		else:
			s.step['dn']=int(dn) or s.step['dn']
		if up is None and s.step['up'] is None:
			s.step['up']=1
		else:
			s.step['up']=int(up) or s.step['up']
		s._update_wrappers()
	def expand(s,size=1):
		if size>=0:
			s._rnge+=size
		else:
			s._shift+=size
		s._update_wrappers()

	def contract(s,size=1):
		if size>=0:
			s._rnge-=size
		else:
			s._shift-=size
		s._update_wrappers()

	def next(s):
		s._value = s._up(s._value)
		selected=s._value+s._shift
		if s.parent is not None:
			s.parent.selected=selected
			s.parent.value=s.parent.store.get(selected)
		return selected

	def prev(s):
		s._value = s._dn(s._value)
		selected=s._value+s._shift
		if s.parent is not None:
			s.parent.selected=selected
			s.parent.value=s.parent.store.get(selected)
		return selected

	def read(s):
		return s._value+s._shift

	def write(s, val):
		nval=val
		s._value = s._wr(nval)
		selected=s._value+s._shift
		if s.parent is not None:
			s.parent.selected=selected
			s.parent.value=s.parent.store.get(selected)
		return selected



class Size():
	def __init__(s, **k):
		from libTerm import Coord

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


class Store():
	def __init__(s, **k):
		"""Simple contiguous store backed by a list of values.

		Keys are 1-based integers (1..n). Internally values are stored in
		`s._values` where index 0 corresponds to key 1.

		By default the store has unlimited size; use `setmax` to bound it.
		"""
		s.store = {0:None,}
		s.size=1
		s.tail=1
		s.cursor=1
		s._max = None
		s.selected=None
		s.value=None
		s._selector=Selector((1,s.size+1),start=1,parent=s)
		s._selector.write(1)
		s._keys=[]

	def max(s, mx=None):
		if mx is not None :
			if not isinstance(mx, int) or mx < 1:
				raise ValueError('maximum must be a positive int or None')
			s._max=mx

		if s._max is None and mx is None:
			s._max = 4294967295
		return s._max

	def save(s, value):
		s._selector.write(s.tail)
		if not (s.tail>=s.max()):
			idx=s.tail
			s.store[idx]=value
			s._keys+=[idx]
			s.size+=1
			s.tail+=1
			s._selector.expand()
			s._selector.write(s.tail)
			return idx,s.store.get(idx)

	def clear(s):
		s.store.clear()
		s.store={0:None,}
		s.tail = 1
		s._selector=Selector(s.size)
		s.read()
		return

	def prev(s):
		s._selector.prev()
		return s.selected,s.value

	def next(s):
		s._selector.next()
		return s.selected,s.value

	def __len__(s):
		result = len(s.store.values()-1)
		return result

	def keys(s):
		return s._keys




