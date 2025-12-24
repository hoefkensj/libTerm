import select
from dataclasses import dataclass,field
from collections import namedtuple
from os import get_terminal_size
from  time import sleep, time_ns
import sys


@dataclass()
class Coord(namedtuple('Coord', ['x', 'y'])):
	__module__ = None
	__qualname__='Coord'
	_x: int = field(default=0)
	_y: int = field(default=0)

	def __str__(s):
		return f'\x1b[{s.y + 1};{s.x + 1}H'

	def __repr__(s):
		return f"{s.__class__.__name__}({s.x}, {s.y})"

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


	def keys(s):
		return ('x', 'y')

	def __add__(s, other):
		if isinstance(other,Coord):
			x=s.x+other.x
			y=s.y+other.y
			return Coord(x,y)
		elif isinstance(other,complex):
			x=s.x+other.real
			y=s.y+other.imag
			return Coord(x,y)
		elif isinstance(other,str):
			return f'{s.__str__()}{other}'
		else:
			raise TypeError(f"cannot add {type(s)} to {type(other)}")

	@property
	def xy(s) -> tuple[int, int]:
		return (s.x, s.y)

	@property
	def y(s):
		return s._y

	@property
	def x(s):
		return s._x


@dataclass(frozen=True)
class color:
	R: int = field(default=0, metadata={"range": (0, 65535)})
	G: int = field(default=0, metadata={"range": (0, 65535)})
	B: int = field(default=0, metadata={"range": (0, 65535)})
	BIT: int = field(default=8, metadata={"set": (4, 8, 16, 32)})

	def __post_init__(self):
		for attr_name in ("R", "G", "B"):
			value = getattr(self, attr_name)
			if not isinstance(value, int):
				raise ValueError(f"{attr_name.upper()} must be an integer between 0 and 65535. Got {value}.")
		if not isinstance(getattr(self, "BIT"), int):
			raise ValueError(f"{attr_name.upper()} must be one of 4,8,16,32. Got {value}.")

	@property
	def RGB(self) -> tuple[int, int, int]:
		return (self.R, self.G, self.B)

# @dataclass()
# class TermCo(namedtuple('Co',['x','y'])):
# 	x:int=field(default=0)
# 	y:int=field(default=0)
# class Line(namedtuple('Line',['a','b'])):
# 	a:Co=field(default_factory=Co)
# 	b:Co=field(default_factory=Co)
# 	@classmethod
# 	def __add__(s, o):
# 		if isinstance(o,Line):
# 			if len(s.a)!=0 and len(s.b)!=0:
# 				lenx=abs(s.b.x-s.a.x)+abs(o.b.x-o.a.x)
# 				leny=abs(s.b.y-s.a.y)+abs(o.b.y-o.a.y)
# 				L=Line(s.a,Co(s.a.x+lenx,s.a.y+leny))
# 			else:
# 				return 0
#
# 	def __len__(s):
# 		if len(s.a) != 0 and len(s.b) != 0:
# 			lenx = abs(s.b.x - s.a.x) + abs(o.b.x - o.a.x)
# 			leny = abs(s.b.y - s.a.y) + abs(o.b.y - o.a.y)
# 			return ((lenx**2+leny**2)**(1/2))

class Size():
	def __init__(__s, **k):
		__s.parent = k.get('parent')
		__s.getsize = get_terminal_size
		__s.time = None
		__s.last = None
		__s.xy = Coord(1, 1)
		__s._tmp = Coord(1, 1)
		__s.rows = 1
		__s.cols = 1

		__s.history = []
		__s.changed = False
		__s.changing = False

		__s.__kwargs__(**k)
		__s.__update__()

	@property
	def width(__s):
		__s.__update__()
		return __s.cols
	@property
	def height(__s):
		__s.__update__()
		return __s.rows
	@property
	def rc(__s):
		__s.__update__()
		return (__s.cols, __s.rows)

	def __kwargs__(__s, **k):
		__s.term = k.get('parent')

	def __update__(__s):
		if __s.time is None:
			__s.last = time_ns()
		size = Coord(*__s.getsize())
		if size != __s.xy:
			if size != __s._tmp:
				__s.changing = True
				__s._tmp = size
				__s._tmptime = time_ns()
			if size == __s._tmp:
				if (time_ns() - __s._tmptime) * 1e6 > 500:
					__s.changing = False
					__s.changed = True
					__s.history += [__s.xy]
					__s.xy = size
					__s.rows = __s.xy.y
					__s.cols = __s.xy.x
				else:
					__s._tmp = size
		if size == __s.xy:
			__s.changed = False

class Colors():
	def __init__(__s, **k):
		__s.parent = None
		__s.specs = {'fg': 10, 'bg': 11}
		__s._ansi = '\x1b]{spec};?\a'
		__s.__kwargs__(**k)
		__s.fg = color(255, 255, 255)
		__s.bg = color(0, 0, 0)
		__s.init = __s.__update__()

	def __kwargs__(__s, **k):
		__s.term = k.get('parent')

	@staticmethod
	def _ansiparser_():
		buf = ''
		try:
			for i in range(23):
				buf += sys.stdin.read(1)
			rgb = buf.split(':')[1].split('/')
			rgb = [int(i, base=16) for i in rgb]
			rgb = color(*rgb, 16)
		except Exception as E:
			# print(E)
			rgb = None
		return rgb

	def __update__(__s):
		for ground in __s.specs:
			result = None
			while not result:
				result = __s.term.ansi(__s._ansi.format(spec=__s.specs[ground]), __s._ansiparser_)
			__s.__setattr__(ground, result)

		return {'fg': __s.fg, 'bg': __s.bg}

class Selector():

	def __init__(s,n, **k):
		s.selection = k.get('start', 0)
		s.n=n
		s.prev = lambda: s.selector(-1)
		s.next = lambda: s.selector(1)
		s.read = lambda: s.selector(0)
		s.write = s.setval

	def wrap(s,ss):
		return  ~(~ss * -~-s.n) % s.n

	def selector(s,i):
		s.selection = s.wrap(s.selection + i)
		return s.selection

	def setval(s,i):
		s.selection = s.wrap(i)
		return s.selection





class Store():
	def __init__(__s, **k):
		"""Simple contiguous store backed by a list of values.

		Keys are 1-based integers (1..n). Internally values are stored in
		`__s._values` where index 0 corresponds to key 1.

		Pointer semantics:
		- __s._pointer ranges from -1 .. len(__s._values)
		- -1 means before-first
		- 0..len-1 means index into values (current)
		- len means after-last

		By default the store has unlimited size; use `setmax` to bound it.
		"""
		__s._store = {0:None,}
		__s.tail=1
		__s.size=lambda:len(__s._store)
		__s._current= 0
		__s._pointer = lambda:__s._values.get(__s._current)
		__s._max = None

		__s.select=Selector(__s.size())
		__s.selected = __s.select.read()

	def _next_key(__s):
		"""Return next integer key (1-based) without inserting."""
		result = len(__s._values) + 1
		return result

	def setmax(__s, maximum: int | None):
		"""Set maximum number of stored items (None = unlimited)."""
		result = None
		if maximum is not None:
			if not isinstance(maximum, int) or maximum < 1:
				raise ValueError("maximum must be a positive int or None")
		__s._max = maximum
		return result

	def save(__s, value):
		__s._store[__s.size()]=value
		__s.tail+=1
		current=__s.select.read()
		__s.select=Selector(__s.tail)
		__s.select.write(current+1)
		__s.selected = __s.select.read()
		return __s.selected

	def load(__s):
		__s.selected=__s.select.read()
		return __s._store[__s.selected]
	def remove(__s, index: int):
		result = None
		pos = index - 1
		if 0 <= pos < len(__s._values):
			val = __s._values.pop(pos)
			# adjust pointer
			if __s._pointer > pos:
				__s._pointer -= 1
			elif __s._pointer == pos:
				__s._pointer = max(pos - 1, -1)
			if __s._pointer > len(__s._values):
				__s._pointer = len(__s._values)
			result = val
		return result

	def pop(__s, index: int | None = None):
		"""Pop last inserted item if index is None, else remove by key.
		Return popped value or None."""
		result = None
		if not __s._values:
			result = None
		else:
			if index is None:
				val = __s._values.pop()
				if __s._pointer >= len(__s._values):
					__s._pointer = len(__s._values)
				result = val
			else:
				result = __s.remove(index)
		return result

	def clear(__s):
		"""Clear the store."""
		result = None
		__s._values.clear()
		__s._pointer = 0
		return result

	def prev(__s):
		__s.selected=__s.select.prev()
		return __s._store[__s.selected]


	def next(__s):
		__s.selected=__s.select.next()
		return __s._store[__s.selected]

	def replace(__s, index: int, value):
		"""Replace value in-place at given key. Return True if replaced else False."""
		result = False
		pos = index - 1
		if 0 <= pos < len(__s._values):
			__s._values[pos] = value
			result = True
		return result

	def __len__(__s):
		result = len(__s._values)
		return result

	def keys(__s):
		"""Return the list of integer keys (1-based)."""
		result = list(range(1, len(__s._values) + 1))
		return result
