# /usr/bin/env pyhthon
from collections import namedtuple
from dataclasses import dataclass, field


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
