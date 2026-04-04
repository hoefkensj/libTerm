#!/usr/bin/env python
from collections import namedtuple
from dataclasses import dataclass, field
from os import get_terminal_size
from time import time_ns
from libTerm.components.enums import StoreStop


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

def makeCoord(a):
		if isinstance(a, tuple | set | list):
			try:
				c = Coord(*a)
			except Exception:
				c = None
		elif isinstance(a, dict):
			try:
				c = Coord(*[*a.values()])
			except Exception:
				c=None
		else:
			raise TypeError('Expected a Coord, tuple or set of length 2, got {EXTRA}'.format(EXTRA=coord))
		return c




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
		elif isinstance(other, list|tuple|set):
			x=s.x+other[0]
			y=s.y+other[1]

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
# TODO:	def __matmul__(self, other):

	def __truediv__(s, other):
		x=s.x/other
		y=s.y/other
		x=int(x) if int(x)==x else x
		y=int(y) if int(y)==y else y
		return Coord(x,y)
	def __floordiv__(s, other):
		x=s.x//other
		y=s.y//other
		return Coord(x,y)
	@property
	def real(s):
		return s.x

	@property
	def imag(s):
		return s.y

	def keys(s):
		return ('X', 'Y')


	@property
	def xy(s) -> tuple[int, int]:
		return (s.x, s.y)

	@property
	def y(s):
		return s._y

	@property
	def x(s):
		return s._x
	@property
	def X(s):
		return s.x
	@property
	def Y(s):
		return s.y


class Selector:
	"""Cyclic Selector,configurable range and step-size
		note: a range of (1,10) includes both 1 and 10:
		10 <- 1 2 3 4 5 6 7 8 9 10 ->1
	"""
	def __init__(s,rnge=(1,10),dn=-1,up=1,start=None,offset=0):

		s._offset=0
		s.step={}
		s.step_dn= dn
		s.step_up= up
		s._shift = 0
		s._start = start
		s._range_min = 1
		s._range_max = 1
		s.range=rnge
		s.val=start or 1
		s._wr(start or s._range_min)

	def _wrap(s,val):
		if s._range_max==s._range_min:
			val= s._range_max
		while val > s._range_max:
			rest=val-s._range_max
			rest-=1
			val=s._range_min+rest
		while val < s._range_min:
			under=val-s._range_min
			under+=1
			val=s._range_max+under
		assert s._range_min<=val <=s._range_max
		# print(s._range_min,val,s._range_max)

		return val

	def _up(s):
		s.value=s._wrap(s.value+s.step_up)
	def _dn(s):
		s.value=s._wrap(s.value+s.step_dn)
	def _wr(s,val):
		s.value=s._wrap(val)
	def _rd(s):
		return s.value
	@property
	def range(s):
		rnge=(s._range_min,s._range_max)
		return rnge
	@range.setter
	def range(s,rnge):
		assert isinstance(rnge,float|int|list|tuple|set|range)
		if isinstance(rnge,float|int):
			s._range_min=1
			s._range_max=rnge
		elif isinstance(rnge,tuple|list|set):
			s._range_min=rnge[0]
			s._range_max=rnge[1]
		elif isinstance(rnge,range):
			s._range_min = rnge.start()
			s._range_max = rnge.stop()
		if s._range_min > s._range_max:
			s._range_min=s._range_min^s._range_max
			s._range_max=s._range_min^s._range_max
			s._range_min=s._range_min^s._range_max



	def setstep(s,dn=None,up=None):
		if dn is not None:
			s.step_dn=dn
		if up is not None:
			s.step_up=up

	def expand(s,size=1):
		if size>=0:
			s._range_max+=size
		else:
			s._range_min+=size

	def contract(s,size=1):
		if size>=0:
			s._range_max-=size
		else:
			s._range_min-=size


	def next(s):
		s._up()
		return s.value

	def \
			   prev(s):
		s._dn()
		return s.value

	def read(s):
		return s.value

	def write(s, val):
		s._wr(val)
		return s.value


	def preset(s,val):
		return lambda :s._wr(val)

class Store():
	def __init__(s,term=None, **k):
		"""Simple contiguous store backed by a list of values.

		Keys are 1-based integers (1..n). Internally values are stored in
		`s._values` where index 0 corresponds to key 1.

		By default the store has unlimited size; use `setmax` to bound it.
		"""
		s.term=term
		s.store = {0:StoreStop.FIRST_OF_STORE,1:StoreStop.LAST_OF_STORE}
		s.tail=1
		s._max = None
		s.selected=None
		s._value=None
		s.cursor=1
		s._keys=[]
		s.stop=False

	@property
	def value(s):
		# print(s.cursor,repr(s._value))
		s._value=s.store.get(s.cursor)
		# print(s.cursor,repr(s._value))
		return s._value

	def size(s):
		return len(s.store)-2

	def max(s, mx=None):
		if mx is not None :
			if not isinstance(mx, int) or mx < 1:
				raise ValueError('maximum must be a positive int or None')
			s._max=mx

		if s._max is None and mx is None:
			s._max = 4294967295
		return s._max

	def save(s, value):
		"""

		:param value:
		:return: {newkey:value}
		"""
		if not (s.tail>=s.max()):
			s.cursor=s.tail
			newkey = s.tail
			lastkey = [*s.store.keys()][-1]
			lastval=s.store[lastkey]
			pair={newkey : value}
			s.store[newkey]=value
			s._keys+=[newkey]
			s.tail+=1
			s.store[s.tail]=lastval
			return pair

	def prev(s):
		def isfirst(val):
			return bool((val is StoreStop.FIRST_OF_STORE)+
						(s.stop is StoreStop.FIRST_OF_STORE))

		if isfirst(s.value):
			s.stop = StoreStop.FIRST_OF_STORE
		else:
			s.stop = False
			s.cursor -= 1
		return s.cursor,s.value

	def next(s):
		def islast(val):
			return bool((val is StoreStop.LAST_OF_STORE) +
						(s.stop is StoreStop.LAST_OF_STORE))

		if islast(s.value):
			s.stop=StoreStop.LAST_OF_STORE
		else:
			s.stop = False
			s.cursor += 1
		return s.cursor, s.value

	def __len__(s):
		result = len(s.store.values())-2
		return result

	def keys(s):
		store={k:'' for k in s._keys}
		return store.keys()

	def values(s):
		store={**s.store}
		# store.pop(0)
		# store.pop(-1)
		return store.values()



