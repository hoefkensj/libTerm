import re

from libTerm.components.base import Coord,Store
from libTerm.components.enums import StoreStop as Stop
from libTerm.components.enums import Ansi,Move


class Cursor():
	ANSI=Ansi
	def __init__(s, term):
		s.term         = term
		s.move         = Move
		s._re      = re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R", re.VERBOSE)
		s._xy     = Coord(0,0)
		s._xyset  = Coord(0,0)
		s._coordstore   = Store(s.term)
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
			if isinstance(coord,tuple|set|list) and len(coord)==2:
				coord=Coord(*coord)
			elif isinstance(coord,dict):
				if  'x' in coord and 'y' in coord:
					coord=Coord(coord['x'],coord['y'])
				elif 'col' in coord and 'row' in coord:
					coord=Coord(coord['col'],coord['row'])

			else:
				raise TypeError('Expected a Coord, tuple or set of length 2, got {EXTRA}'.format(EXTRA=coord))
		s._xyset=coord
		print(s.move.ABS.format(**coord), end='', flush=True)

	def stored(s):
		return s._coordstore.store

	def update(s):

		result = s.term.stdin.query(s.ANSI.LOC)
		try:
			groups = s._re.search(result).groupdict()
			matched = Coord(int(groups['X']), int(groups['Y']))
		except AttributeError:
			matched = None
		if matched is not None:
			result = matched
		else:
			result=s._xyset
		s._xy =result
		return result

	def hide(s, state=True):
		if s.visible and state:
			print(s.ANSI.hide)
			s.visible=False
		elif not s.visible and not state:
			print(s.ANSI.show)
			s.visible=True
		return s.visible

	def show(s,state=True):
		return s.hide(not state)

	def quicksave(s):
		return s.ansi.save()

	def quickload(s):
		return s.ansi.load()

	@property
	def x(s):
		x=s.xy.x
		return x
	@property
	def y(s):
		y=s.xy.y

	def loc_changed(s):
		ref=s._xy
		if s.xy !=ref:
			changed=True
		else:
			changed=False
		return changed

	def save(s):
		return s._coordstore.save(s.xy)
	def load(s,n):
		coord=s._coordstore.select(n)
		s.xy=coord
		return coord
	def undo(s):
		prev=s._coordstore.prev()
		if not s._coordstore.stop:
			current=prev[0]
			coord=prev[1]
			stop=s._coordstore.stop
			if not (coord is Stop.FIRST_OF_STORE):
				s.xy=coord
				result=current,coord
			else:
				stop=Stop.FIRST_OF_STORE
				result=stop

		return result

# #TODO: class vCursor(Cursor):
# class VirtCursor():
# 	def __init__(s, term,real,xy=Coord(0,0),symbol='░'):
# 		s.real    = real
# 		s.real.slaves+=[s]
# 		s.term    = term
# 		s.symbol  = symbol
# 		s._xy     = xy
# 		s._XY     = s.real.xy
# 		s.store   = Store()
# 		s.visible = True
# 		s.locked  = True
# 		s.enabled = False
# 		s.init    = s.__update__()
# 		s.draw()
# 	def enable(s):
# 		s.enabled = True
# 	@property
# 	def xy(s):
# 		s._xy
#
# 	@xy.setter
# 	def xy(s,coord):
# 		print('\x1b[{y};{x}H'.format(**coord), end='', flush=True)
# 		s.__update__()
#
# 	def stored(s):
# 		return s.store.stored
#
# 	def __update__(s):
# 		result=''
# 		return result
#
# 	def show(s, state=True):
# 		if s.hidden and state:
# 			s.hidden=False
# 			s.visible=True
# 		if s.visible and not state:
# 			s.hidden=True
# 			s.visible=False
#
# 	def hide(s, state=True):
# 		s.show(not state)
#
# 	@property
# 	def x(s):
# 		x=s.xy.x
# 		return x
# 	@property
# 	def y(s):
# 		y=s.xy.y
# 		return y
#
# 	def save(s):
# 		return s.store.save(s.xy)
# 	def load(s,n):
# 		coord=s.store.load(n)
# 		s.xy=coord
# 		return coord
# 	def undo(s):
# 		current=s.store.selected
# 		coord=s.store._store[current]
# 		if coord is not None:
# 			s.xy=coord
# 			s.store.prev()
# 		return coord
# 	def draw(s):
# 		print(s.xy,s.symbol,end='',flush=True)
# 	def edit(s):
# 		s.locked=False
# 		s._edit=True
# 		s.visible=True
# 		s.draw()
# 		s.term.mode = s.MODE.CONTROL
# 		xy=s.term.cursor.xy
# 		y=xy.y
# 		x=xy.x
		# while s._edit:
		# 	if s.term.stdin.event:
		# 		key = s.term.stdin.read()
		# 		if key == '\x1b[D':
		# 			s.xy=Coord(x-1,y)
		# 		elif key == '\x1b[C':
		# 			s.xy=Coord(x-1,y)
		# 		elif key == '\x1b[A':
		# 			s.xy=Coord(x,y-1)
		# 		elif key == '\x1b[B':
		# 			s.xy=Coord(x,y+1)
		# 		elif key == 'q':
		# 			sys.exit(0)
		# 		print(repr(key))