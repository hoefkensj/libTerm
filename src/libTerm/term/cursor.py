import sys
import re
import asyncio
from enum import Enum
from dataclasses import dataclass
from time import time_ns

from libTerm.types.base import Coord,Store
from libTerm.types.enums import StoreStop as Stop
from enum import StrEnum,auto






class Ansi(StrEnum):
	ESC     = '\x1b'
	CSI     = ESC+'['
	OSC     = ESC+']'
	APC     = ESC+'_'
	ST      = ESC+'\\'
	show    = CSI+'?25h'
	hide    = CSI+'?25l'
	SCROLL  = ESC+'M'
	LOC     = CSI+'6n'
	save    = ESC+'7'+CSI+'s'
	load    = ESC+'8'+CSI+'u'

	def __str__(s):
		return s.value
	def __repr__(s):
		return repr(s.value)

	def __call__(self, *args, **kwargs):
		print(self.value, end='', flush=True)




class Move(StrEnum):
	CSI   = Ansi.CSI
	UP    = CSI+'{N}A'
	DOWN  = CSI+'{N}B'
	RIGHT = CSI+'{N}C'
	PREV  = CSI+'{N}E'
	LEFT  = CSI+'{N}D'
	NExT  = CSI+'{N}F'
	COL   = CSI+'{X}G'
	ABS   = CSI+'{Y};{X}H'

	def __str__(s):
		return s()
	def __repr__(s):
		return repr(s.value)
	def __call__(s, *a):
		CSI=s.CSI
		if s.value == Move.ABS:
			X=a[0]
			Y=a[1]
			result=s.value.format(CSI=CSI,X=X,Y=Y)
		else:
			N = a[0]
			result=s.value.format(CSI=CSI,N=N)
		return result



class Cursor():
	def __init__(s, term):
		s.term    = term
		s.ansi    = Ansi
		s.move    = Move
		s._show   = Ansi.show
		s._hide   = Ansi.hide
		s._re      = re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R", re.VERBOSE)
		s._xy     = Coord(0,0)
		s._xyset  = Coord(0,0)
		s.store   = Store(s.term)
		s.visible = True
		s.hidden  = False
		s.mock    = False
		s.slaves  = []
		#TODO:		s.stamp=time_ns()
		#TODO:		s.moved=False
		#TODO:		s._history = [*(None,) * 64]ASDF
		s.init    = s.__sync__()
	def __sync__(s):
		s.update()
		s._xy=s.xy

	@property
	def xy(s):
		result=s.update()
		return result

	@xy.setter
	def xy(s,coord):
		if not isinstance(coord,Coord):
			coord=Coord(*coord)
		s.xyset=coord
		print('\x1b[{y};{x}H'.format(**coord), end='', flush=True)


	def stored(s):
		return s.store.store

	def update(s):
		def Parser():
			buf = ' '
			while buf[-1] != "R":
				buf += s.term.stdin.raw().decode('UTF-8')
				if len(buf) > 32:
					break
			return buf
		result = s.term.stdin.ansiresponse(s.ansi.LOC, Parser)
		try:
			groups = s._re.search(result).groupdict()
			matched = Coord(int(groups['X']), int(groups['Y']))
		except AttributeError:
			result = None
		if result is not None:
			result = matched
		else:
			result=s.xyset
		s._xy =result
		return result

	def hide(s, state=True):
		if s.visible and state:
			print(s.ansi.hide)
			s.visible=False
		elif not s.visible and not state:
			print(s.ansi.show)
			s.visible=True
		return s.visible
	def show(s,state=True):
		return s.hide(not state)


	@property
	def x(s):
		x=s.xy.x
		return x
	@property
	def y(s):
		y=s.xy.y

	def changed(s):
		ref=s._xy
		if s.xy !=ref:
			changed=True
		else:
			changed=False
		return changed

	def save(s):
		return s.store.save(s.xy)
	def load(s,n):
		coord=s.store.select(n)
		s.xy=coord
		return coord
	def undo(s):
		if not s.store.stop:
			current,coord=s.store.prev()
			stop=s.store.stop
			s.xy = coord
			return current,coord
		else:
			return s.store.stop


#TODO: class vCursor(Cursor):
class VirtCursor():
	def __init__(s, term,real,xy=Coord(0,0),symbol='░'):
		s.real    = real
		s.real.slaves+=[s]
		s.term    = term
		s.symbol  = symbol
		s._xy     = xy
		s._XY     = s.real.xy
		s.store   = Store()
		s.visible = True
		s.locked  = True
		s.enabled = False
		s.init    = s.__update__()
		s.draw()
	def enable(s):
		s.enabled = True
	@property
	def xy(s):
		s._xy

	@xy.setter
	def xy(s,coord):
		print('\x1b[{y};{x}H'.format(**coord), end='', flush=True)
		s.__update__()

	def stored(s):
		return s.store.stored

	def __update__(s):
		result=''
		return result

	def show(s, state=True):
		if s.hidden and state:
			s.hidden=False
			s.visible=True
		if s.visible and not state:
			s.hidden=True
			s.visible=False

	def hide(s, state=True):
		s.show(not state)

	@property
	def x(s):
		x=s.xy.x
		return x
	@property
	def y(s):
		y=s.xy.y
		return y

	def save(s):
		return s.store.save(s.xy)
	def load(s,n):
		coord=s.store.load(n)
		s.xy=coord
		return coord
	def undo(s):
		current=s.store.selected
		coord=s.store._store[current]
		if coord is not None:
			s.xy=coord
			s.store.prev()
		return coord
	def draw(s):
		print(s.xy,s.symbol,end='',flush=True)
	def edit(s):
		s.locked=False
		s._edit=True
		s.visible=True
		s.draw()
		s.term.mode = s.MODE.CONTROL
		xy=s.term.cursor.xy
		y=xy.y
		x=xy.x
		while s._edit:
			if s.term.stdin.event:
				key = s.term.stdin.read()
				if key == '\x1b[D':
					s.xy=Coord(x-1,y)
				elif key == '\x1b[C':
					s.xy=Coord(x-1,y)
				elif key == '\x1b[A':
					s.xy=Coord(x,y-1)
				elif key == '\x1b[B':
					s.xy=Coord(x,y+1)
				elif key == 'q':
					sys.exit(0)
				print(repr(key))