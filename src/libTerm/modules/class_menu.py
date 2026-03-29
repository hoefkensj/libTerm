#!/usr/bin/env python

from libTerm import Color
from libTerm.components import Selector

class Menu:
	def __init__(s,term,items,templates=None,location=None,colors=None,nums=True,numstart=1):
		s.CSI='\x1b['
		s.term=term
		s.loc=location
		s.fgcol=colors.fg or Color(64,192,192)
		s.bgcol=f';48;2;{colors.bg.ansi()}' if colors.bg is not None else ''
		s.nums=nums
		s.numstart=numstart
		s._tpl=['\x1b[{Y};{X}H','{XY}{MARKUP}{NO}.','{NO}{XY}\x1b[m{MARKUP}{ITEM}{DESEL}']
		s._items=[*items]
		s.selector=Selector((1,len(s._items)))
		s.stop=False
		s.items={}
		s.menu=[]
		s.changed=[]
		s.updated=''
		s.init=False
		s.it_width = max([len(n) for n in s._items]) + 2
		s.nr_width = len(str(len(s._items)))
		s.colors={'FGCOLOR':s.fgcol.ansi(),'BGCOLOR':s.bgcol}
		s.build(location)
	@property
	def selected(s):
		v=s.selector.read()
		return v
	def __len__(s):
		return len(s.items)

	def markup(s,sel='27',mod=''):
		tpl='\x1b[{SEL};38;2;{FGCOLOR}{BGCOLOR}{MOD}m'
		return {'MARKUP':tpl.format(SEL=sel,MOD=mod,**s.colors)}

	def build(s,xy):
		for i,arg in enumerate(s._items,start=1):
			XY = s._tpl[0].format(Y=xy.y + i, X=xy.x)
			if s.nums:
				num=s._tpl[1].format(XY=XY,NO=str(i+s.numstart-1).rjust(s.nr_width),**s.markup(mod=';2'))
			else:num=''
			s.items[i]=s._tpl[2].format(
				DESEL='\x1b[27m',
				CONR=s._tpl[2],
				XY=XY if not s.nums else '',
				MARKUP='{MARKUP}',
				NO=num if s.nums else '',
				ITEM=arg.ljust(s.it_width))

		s.menu=[]
		for i in s.items:
			s.menu += [s.items[i].format(**s.markup())]
		s.menu+=s.items[s.selector.read()].format(**s.markup('7'))
		return s.menu

	def next(s):
		s.changed=[s.items[s.selector.read()].format(**s.markup())]
		s.selector.next()
		s.changed+=[s.items[s.selector.read()].format(**s.markup('7'))]
		return s.update()

	def prev(s):
		s.changed=[s.items[s.selector.read()].format(**s.markup())]
		s.selector.prev()
		s.changed+=[s.items[s.selector.read()].format(**s.markup('7'))]
		return s.update()

	def select(s,nr):
		if nr > s.__len__():
			nr=s.__len__()
		s.changed=[s.items[s.selector.read()].format(**s.markup('2'))]
		s.selector.write(nr)
		sel=s.selector.read()
		s.changed+= [s.items[sel].format(**s.markup('7'))]
		return s.update()

	def update(s):
		s.updated=''.join(s.changed[::-1])
		print(s.updated,end='',flush=True)
		return s.updated

	def choose(s,markup=';27;1;38;2;0;255;255'):
		itemtpl=s.items[s.selector.read() ]
		item=s._items[s.selector.read()-1]
		s.changed = [itemtpl.format(**s.markup(sel='',mod=markup))]
		s.update()
		return [s.selector.read(),item]

	def draw(s):
		print(''.join(s.menu),end='',flush=True)
	def repr(s):
		print(''.join(s.menu),end='',flush=True)
	def __str__(s):
		return ''.join(s.menu)+s.updated


class Grid(Menu):
	def __init__(s, term, items, location, direction='vertical', maxwidth=None, maxheight=None, colors=None,itempad=6,nums=True,numstart=1):
		"""

		:param term: instance of libTerm.Term
		:param items:
		:param location:
		:param maxwidth:
		:param maxheight:
		:param fgcolor:
		:param bgcolor:
		"""
		s.term = term
		s._tpl=['\x1b[{Y};{X}H','{XY}{CONR}{NO}. {COIR}{ITEM}{DESEL}','{MARKUP}']
		s._items = [str(item).replace('{','{{').replace('}','}}') for item in items]
		s._maxw=maxwidth or term.size.xy.x//len(s._items)
		s._maxh=maxheight or term.size.xy.y
		s._pad=itempad
		s._dir=direction
		s.cols={}
		s.rows={}
		s.fgcol=colors.fg or Color(64,192,192)
		s.bgcol=f';48;2;{colors.bg.ansi()}' if colors.bg is not None else ''
		s.selector = Selector((0,len(s._items)))
		s.selector.write(1)
		s.stop = False
		s.items = {}
		s.menu = []
		s.changed = []
		s.updated = ''
		s.init = False
		s.col={}
		s.row={}
		s.nrows={}
		s.ncols={}
		s.it_width = max([len(str(n)) for n in s._items]or [itempad])
		s.nr_width = len(str(len(s._items)))
		s.colors={'FGCOLOR':s.fgcol.ansi(),'BGCOLOR':s.bgcol}
		s.build(location)


	def build(s, xy):
		row=1
		c=s.it_width+s._pad
		col=1
		for i, arg in enumerate(s._items, start=1):
			if 'vert' in s._dir:
				if (i % (s._maxh) ==1)*(i!=1):
					col+=1
					row=1
			elif 'hor' in s._dir:
				if (i % s._maxw == 1)*(i!=1):
					col=1
					row+=1
			s.col[col]=s.col.get(col,{})
			s.row[row]=s.row.get(row,{})
			s.items[i]=s._tpl[1].format(
				DESEL='\x1b[27m',
				CONR=s._tpl[2],
				XY=s._tpl[0].format(Y=xy.y + row - 1, X=xy.x + (c * (col-1))),
				COIR=s._tpl[2],
				NO=str(i).rjust(s.nr_width),
				ITEM=arg.ljust(s.it_width).rjust(s.it_width))
			s.col[col][row]=i,s.items[i]
			s.row[row][col]=i,s.items[i]
			s.rows[i]=row
			s.cols[i]=col
			s.nrows[col]=row
			s.ncols[row]=col
			if 'vert' in s._dir:
				row+=1
			elif 'hor' in s._dir:
				col+=1
		for i in s.items:
			s.menu+=[s.items[i].format(**s.markup())]
		s.menu+=s.items[s.selector.read()].format(**s.markup('7'))
		return s.menu



	def prev(s):
		s.changed=[s.items[s.selector.read()].format(**s.markup())]
		s.selector.next()
		s.changed+=[s.items[s.selector.read()].format(**s.markup('7'))]
		return s.update()
	def next(s):
		s.changed=[s.items[s.selector.read()].format(**s.markup())]
		s.selector.prev()
		s.changed+=[s.items[s.selector.read()].format(**s.markup('7'))]
		return s.update()
	def rowcol(s,r=0,c=0):
		return s.rows[s.selector.read()]+r,s.cols[s.selector.read()]+c

	def hor(s,val):
		def wrap(col):
			if (val < 0) * (col < 1):
				col = s.ncols[row]
			elif (val > 0) * (col > s.ncols[row]):
				col = 1
			assert col != 0
			return col
		sel=s.selector.read()
		s.changed=[s.items[sel].format(**s.markup(''))]
		row,col=s.rowcol(0,val)
		s.selector.write(s.col[wrap(col)][row][0])
		s.changed+=[s.items[s.selector.read()].format(**s.markup('7'))]
	def ver(s,val):
		def wrap(row):
			if (val < 0) * (row < 1):
				row = s.nrows[col]
			elif (val > 0) * (row > s.nrows[col]):
				row = 1
			assert row != 0
			return row
		sel=s.selector.read()
		s.changed=[s.items[sel].format(**s.markup())]
		row,col=s.rowcol(val,0)
		s.selector.write(s.col[col][wrap(row)][0])
		s.changed+=[s.items[s.selector.read()].format(**s.markup('7'))]

	def right(s):
		s.hor(1)
		return s.update()
	def left(s):
		s.hor(-1)
		return s.update()
	def up(s):
		s.ver(-1)
		return s.update()

	def down(s):
		s.ver(1)
		return s.update()


# from libTerm import Term
# items=['xxxx','xxxx','yyyy','dasdf','dasdf','erwrsdd','sdf','pppfpf']
# t=Term()
# g=Grid(t,items,Coord(5,5),maxheight=3)
# g.draw()
# print()