#!/usr/bin/env python

from libTerm import Color,Ansi,ColorSet,ColorPalette,Coord
from libTerm.components import Selector
class ChangeSet:
	def __init__(s,markup=None):
		s._old=None
		s._new=None
		s.markup=markup


		s.sel=''
		s.mod=''
		# s.mk_colors=markup.get('colors',{})
		s.tpl='\x1b[{SEL};38;2;{FGCOLOR}{BGCOLOR}{MOD}m'


	def __str__(s):

		return string
	@property
	def old(s):
		s.tpl.format(SEL='',MOD='',**s.mk_colors)
		return s._old
	@old.setter
	def old(s,value):
		s._old=value

	@property
	def new(s):
		return s._new
	@new.setter
	def new(s,value):
		s._new=value
from abc import ABCMeta, abstractmethod


class MenuItem:
	def __init__(s,*a,**k):
		s._name=k.get('name',a[0])
		s._label=s.safestring(k.get('label',s._name))
		s._selected=False
		s._focused=False
		s._chosen=False
		s._confirmed=False
		s._formatting=k.get('format',Formatting())
		s._mkup={'MKUP':''}
		s._padd={'LPAD':s.lpad,'RPAD':s.rpad}
		s._xy=None
		s._lpad=None
		s._rpad=None
		s._bullet={}
		s._bullet['enabled']=False
		s._bullet['string']=''
		s._bullet['pad']={'lpad':'','rpad':''}
		s._bullet['mkup']=''
		s._number={}
		s._number['enabled']=False
		s._number['string']=''
		s._number['pad']={'lpad':'','rpad':''}
		s._number['mkup']=''
		s._num=None
		s._template={}
		s._template['part']='{MKUP}{LPAD}{PART}{RPAD}'
		s._template['bullet']=s._template['part'].format(MKUP='{BULLET_MKUP}',LPAD='{BULLET_LPAD}',RPAD='BULLET_RPAD',PART='BULLET')
		s._template['number']=s._template['part'].format(MKUP='{NUMBER_MKUP}',LPAD='{NUMBER_LPAD}',RPAD='NUMBER_RPAD',PART='NUMBER',)
		s._template['label']=s._template['part'].format(MKUP='{LABEL_MKUP}',LPAD='{LABEL_LPAD}',RPAD='LABEL_RPAD',PART='LABEL',)
		s._templete['mods']='{SEL}{FOC}{PIC}{CNF}'
		s._template['string']='{XY}{MODS}{PREFIX}{LABEL}{SUFFIX}{RESET}'

	@property
	def bullet(s):
		return s._bullet['enabled']
	@property
	def bulletstr(s):
		return s._bullet['string']		
	@bullet.setter
	def bullet(s,state=None,string=None):
		if state is not None:
			s._bullet['enable']=state
		if string is not None:
			s._bullet['string']=string
	@property
	def number(s):
		return s._number['enabled']
	@property
	def numberstr(s):
		return s._number['string']
	@number.setter
	def number(s,state=None,string=None):
		if state is not None:
			s._number['enable']=state
		if string is not None:
			s._number['string']=string

	def safestring(s,string):
		return str(string).replace('{', '{{').replace('}', '}}')

	def __str__(s):
		def mkprefix():
			pfx=''
			if s.bullet:
				pfx+=s._template['bullet']
			if s.number:
				pfx+=s._template['number']
			return pfx
		string=s._template['string']
		XY=s.location
		MODS=s._template['mods']
		PFX=mkprefix()

		mods={
			'SEL': s._selected  *s._formatting.select,
			'FOC': s._focused   *s._formatting.focus,
			'PIC': s._chosen    *s._formatting.choose,
			'CNF': s._confirmed *s._formatting.confirm
		}
		return s._template.format(MODS=MODS.format(**mods),PFX=PFX,LABEL=s._label,SFX='')
	def __len__(s):
		return len(s._label)
	def focus(s,val=True):
		s._focused=val
	def select(s,val=True):
		s._selected=val
	def confirm(s,val=True):
		s._confirmed=val
	def draw(s):
		print(s.__str__(),end='',flush='')
# class MenuItem:
# 	def __init__(s,menu=None,ctx=None,name=None,id=None,nr=None,label=None,**k):
# 		s.ctx=ctx
# 		s.menu=menu
# 		s.name=name
# 		s.tpl='{PADPRE}{LABEL}{PADPOST}{RESET}'
# 		s._state=0
# 		s._label=None
# 		s._show=True
# 		s._focus=False
# 		s._selected=False
# 		s._onfocus=[]
# 		s._onselect=[]
# 		s._callback=[s.defaultcb]
# 		s._string=''
#
#
# 	def focus(s,state=True):
# 		s._focus=state
#
# 	def width(s, part):
# 		if s.menu:
# 			s.menu._maxw.get(part)
# 		return len(s.name)
#
# 	def fmt(s,part):
# 		return getattr(s.menu._fmt,part)
# 	def choose(s):
# 		s.highlight()
# 		s()
# 		s.menu.choice=s
# 		s.menu.draw()
#
# 	def highlight(s):
# 		s.selected=False
# 		s.normal=False
# 		s.highlt=True
# 		s.state=2
# 		s.menu.update()
# 	def deselect(s):
# 		s.state=0
# 		s.menu.update()
# 	def select(s):
# 		s.state=1
# 		s.menu.update()
#
# 	@property
# 	def label(s):
# 		return s.safestring()
#
# 	@label.setter
# 	def label(s,value):
# 		s._label=value
# 	def hide(s,state=True):
# 		s._show=not state
# 	def show(s,state=True):
# 		s._show=state
# 	def defaultcb(s):
# 		return s.nr,s.name
#
# 	def safestring(s):
# 		return str(s._label).replace('{', '{{').replace('}', '}}')
# 	def draw(s):
# 		print(str(s))
# 	def __len__(s):
# 		return len(str(s))
#
# 	def __str__(s):
# 		if s._show:
# 			nr=str(s.nr).rjust(s.width('num'))
# 			label=s.label.ljust(s.width('label')+len(s.fmt('pad_label')))
# 			mkup='\x1b[38;2;{FG}m'.format(FG=s._fmt.mku_colorItem.fg.ansi())
# 			sep=s.fmt('sep_nrlabel')
# 			padsep=s.fmt('pad_sep')
# 			padpre=s.fmt('pad_pre')
# 			padpost=s.fmt('pad_post')
# 		elif not s._show:
# 			nr=''
# 			label=''
# 			mkup=''
# 			sep=''
# 			padsep=''
# 			padpre=''
# 			padpost=''
# 		else:
# 			nr=' '*len(str(s.nr).rjust(s.width('num')))
# 			label=' '*len(s.label.ljust(s.width('label')+len(s.fmt('pad_label'))))
# 			mkup='\x1b[m'
#
#
#
# 		val={
# 		'MKUP'    : mkup,
# 		'LOC'     : str(s.location),
# 		'PADSEP'  : padsep,
# 		'PADPRE'  : padpre,
# 		'PADPOST' : padpost,
# 		'SEP'     : sep,
# 		'MOD'     : '\x1b[1;7m' if s.state==1 else '\x1b[m',
# 		'NOMKUP'  : '\x1b[0m'
# 		}
# 		s.string= s._tplitem.format(NR=nr,LABEL=label,**val)
# 		return s.string
#
# 	def __call__(s):
# 		for call in s.callback:
# 			call()


class MenuBase(metaclass=ABCMeta):
	def __init__(s,ctx=None,parent=None,*a,**k):
		s.ctx = ctx
		s.parent = parent
		s.term = s.parent._term
		s.name = name
		s.bulletsyms = '⟪«‹… …›»⟫'
		s._location = None
		s._size = None
		s._scroll = False
		s._shift = False
		s._hidden = False
		s.overflow = False
		s.v_viewrng = ViewRange(1, s.size.y)
		s.h_viewrng = ViewRange(1, s.size.x)
		s.linecount = lambda: s.data_idx
		s.tpl = {}
		s.tpl['LINE'] = '{XY}{MKUP}{{ITEM}}{RESET}'
		s.tpl['LNR'] = '{BG}{FG}{{SEL}}{MKUP}{{NR}}{UNSET}'
		s.tpl['BUFFER'] = {}
		s._direction=None
		s._idlist=[]
		s._lastid=None
		s._items={}
		s._item=None
		s._entries={}
		s._choice=None
		s._selitem=None
		s._focitem=None
		s._linecount=0
		s.linecount=lambda : s._linecount
		s.selector=Selector(1, len(s._idlist))
		s._num_enable=k.get('nums',True)
		s._num_start=k.get('numstart',1)
		s._maxw={'num':0,'label':0,'item':0}
		s._setw={'num':0,'label':0,'item':0}
		s._flag_stop=False
		s._menu=[]
		s._changed=[]
		s._update=None
		s._theme=None
		s._build_()
	@property
	def location(s):
		if s._location is None and s.parent is not None:
			s._location=s.parent.location+Coord(2,2)
		return s._location

	@location.setter
	def location(s,val):
		s._location=val+Coord(2, 2)
		s._state=1
		s.draw()

	@property
	def size(s):
		if s._size is None and s.parent is not None:
			s._size=s.parent.size+Coord(-2,-3)
		s.state=1
		return s._size

	@size.setter
	def size(s,val):
		s._size=val+Coord(-2,-3)
		s.state=1
		s.draw()

	@property
	def direction(s):
		return s._direction

	@direction.setter
	def direction(s,value):
		s._direction=value

	@property
	def item(s):
		return s._item

	@item.setter
	def item(s,item):
		s._item=item
		s.update()

	@abstractmethod
	def build(self): ...

	def read(s):
		return s.selector.read()

	def newid(s,id=None):
		if id is not None:
			s._lastid= id - 1 if id - 1 > s._lastid else s._lastid
		if s._lastid is None:
			s._lastid=len(s._items)
		thisid= s._lastid + 1
		s._lastid=thisid
		s._idlist+=[thisid]
		return thisid

	def addItem(s,item):
		id=s.newid()
		menuitem=MenuItem(s,name=item)
		lenlabel=len(menuitem)
		s._maxw['label']=max([s._maxw['label'],lenlabel])
		s._maxw['num']=len(str(len(s)))

		s._maxw['item']=sum([s._maxw['label'],s._maxw['num']])
		s._items[id]=menuitem
		s.selector.expand(1)

	def show(s,state=True):
		s._show=state
		s.draw()

	def select(s,nr):
		if  s.__len__() != 0:
			if nr > s.__len__():
				nr=s.__len__()
			old=s._entries[s.read()]
			old.deselect()
			s.selector.write(nr)
			s.item=s._entries[s.read()]
			s.item.select()
			s._changed+=[old,s.item]
		s.draw()

	def prev(s):
		old=s._entries[s.read()]
		old.focus(False)
		s.selector.prev()
		s.item=s._entries[s.read()]
		s.item.focus()
		s.update()

	def next(s):
		old=s._entries[s.read()]
		old.focus(False)
		s.selector.next()
		s.item = s._entries[s.read()]
		s.item.focus()
		s.update()


	def draw(s):
		for item in s._items:
			item.draw()

	def update(s):
		return

	def __len__(s):
		return len(s._idlist)

	def __str__(s):
		return s.menu

	@property
	def menu(s):
		return ''.join(s._menu)

class Menu(MenuBase):
	def __init__(s,term,items,templates=None,location=None,colors=None,nums=True,numstart=1,**k):
		super().__init__(parent=None,term=term,items=items,location=location,colors=colors,numstart=numstart,nums=nums,**k)
		s._build_(location)

	def __len__(s):
		return len(s.items)
	# def markup(s,sel='27',mod=''):
	# 	tpl='\x1b[{SEL};38;2;{FGCOLOR}{BGCOLOR}{MOD}m'
	# 	return {'MARKUP':tpl.format(SEL=sel,MOD=mod,**s._markup.ANSI())}

	def _build_(s, location=None):

		for i,arg in enumerate(s._items,start=1):
			XY = s._tpls['location'].format(Y=s.location.y + i, X=s.location.x)
			if s._num_enable:
				num=s._tpls['num'].format(XY=XY,NO=str(i+s._num_start-1).rjust(s._maxw['num']),**s.markup(mod=';2'))
			else:num=''
			s._entries[i]=s._tpls['item'].format(
				DESEL='\x1b[27m',
				CONR=s._tpls['item'],
				XY=XY if not  s._num_enable else '',
				MARKUP='{MARKUP}',
				NO=num if  s._num_enable else '',
				ITEM=arg.ljust(s._maxw['item']).rjust(s._maxw['item']))

		s._menu=[]
		s._menu+=['\n\n'*len(s._entries)+f'\x1b[{len(s._entries)}A']
		s._menu+=[f'\x1b[{len(s._entries)}D']
		for j,k in enumerate(s._items):
			s.menu += [s._entries[j+1].format(**s.markup())]

		s._menu+=s._entries[s.selector.read()].format(**s.markup('7'))
		return s.menu
	# def next(s):
	# 	change=ChangeSet()
	# 	s.changed.add(s.items[s.selector.read()])
	# 	s.selector.next()
	# 	s.changed.add(s.items[s.selector.read()])
	# 	return s.update()
	#
	# def prev(s):
	# 	s.changed.add(s.items[s.selector.read()])
	# 	s.selector.prev()
	# 	s.changed.add(s.items[s.selector.read()])
	# 	return s.update()

	def update(s):
		print(s.changed ,end='',flush=True)
		return s.update

	def delItem(s,item):
		items=[*s._items.remove(item)]
		s.setItems(items)
	def draw(s):
		s._build_()

		print(''.join(s.menu),end='',flush=True)
	def repr(s):
		print(''.join(s.menu),end='',flush=True)

		return ''.join(s.menu)+s.updated

class Row:
	def __init__(s,id):
		s.id=id
		s._show=True
		s._items=[]
		s._entries={}
		s._col={}

	def col(s,col):
		return
	def hide(s,state=True):
		s._show=not state
	def show(s,state=True):
		s._show=state

	def addItem(s,col,iid,item):
		s._items+=[item]
		s._entries[iid]=item
		s._col[col]=iid,item
	def getItem(s,col):
		return s._col.get(col)
	def getCol(s,col):
		return s._col.get(col)
	def __str__(s):
		return ''.join(str(item) for item in s._items)
class Grid(MenuBase):

	def __init__(s,ctx=None,parent=None,*a,**k):
		"""

		:param term: instance of libTerm.Term
		:param items:
		:param location:
		:param maxwidth:
		:param maxheight:
		:param fgcolor:
		:param bgcolor:
		"""
		super().__init__(ctx=ctx,parent=parent,*a,**k)
		s.cols={}
		s.rows={}
		s.stop = False
		s.init = False
		s.col={}
		s.row={}
		s.nrows={}
		s.ncols={}

	# def safestring(s,string):
	# 	return str(string).replace('{', '{{').replace('}', '}}')
	def _build(s):
		if s._lastid is not None:
			row=1
			hide=False
			c=s._maxw['item']
			col=1

			for i, iid in enumerate(s._items, start=1):
				if 'hor' in s.direction:
					if ((i % s.maxhoritems) ==1)*(i!=1):
						col=1
						row+=1
						if row>= s.size.y-1:
							hide=True
				elif 'vert' in s._direction:
					if ((i % s.s._fmt.mnu_maxvitems) == 1)*(i!=1):
						col+=1
						row=1
				s.row[row] = s.row.get(row, Row(id=row))
				s.row[row].hide(hide)

				entry = s._items.get(iid)
				x=s.location.x + (c * (col-1))
				y=s.location.y + row - 1
				entry.location=Coord(x,y)
				entry.hide(hide)
				s._linecount=row


				s.col[col]=s.col.get(col,{})
				# s.entries[i]=s._tpl[1].format(
				# 	DESEL='\x1b[27m',
				# 	CONR=s._tpl[2],
				# 	XY=s._tpl[0].format(Y=s.location.y + row - 1, X=s.location.x + (c * (col-1))),
				#` 	COIR=s._tpl[2],
				# 	NO=str(i).rjust(s.nr_width),
				# 	ITEM=arg.ljust(s.it_width).rjust(s.it_width))
				s._entries[i]=entry
				s.col[col][row]=i,s._entries[i]
				s.row[row].addItem(col,i,s._entries[i])
				s.rows[i]=row
				s.cols[i]=col
				s.nrows[col]=row
				s.ncols[row]=col
				if 'hor' in s._direction:
					col+=1
				elif 'vert' in s._direction:
					row+=1
			# for j in s._entries:
			# 	if s._entries[j]._show:
			# 		s._menu+=[str(s._entries[j])]
			# s._menu+=[str(s._entries[s.selector.read()])]
				for r in s.row:
					s._menu+=[str(s.row[r])]

	# @property
	# def location(s):
	# 	return s._location
	# @location.setter
	# def location(s,value):
	# 	if value is	None:
	# 		value=Coord(1,1)
	# 	s._location=value
	# 	s.setSelector()
	# 	s.build()
	def setfocus(s,item,focus=False):
		s._changed=[s._entries[s.read()]]
		s.selector.write(item)
		s._changed+=[s._entries[s.read()]]

	# def prev(s):
	#
	# 	s.changed.add(s.items[s.selector.read()])
	# 	s.selector.next()
	# 	s.changed.add(s.items[s.selector.read()])
	# 	return s.update()
	# def next(s):
	# 	s.changed.add(s.items[s.selector.read()])
	# 	s.selector.prev()
	# 	s.changed.add(s.items[s.selector.read()])
	# 	return s.update()

	def rowcol(s,r=0,c=0):
		return s.rows[s.read()]+r,s.cols[s.read()]+c


	def move_horizontal(s, val):
		def wrap(col):
			if (val < 0) * (col < 1):
				col = s.ncols[row]
			elif (val > 0) * (col > s.ncols[row]):
				col = 1
			assert col != 0
			return col

		old=s._entries[s.read()]
		old.deselect()
		row,col=s.rowcol(0,val)
		s.selector.write(s.col[wrap(col)][row][0])
		new=s._entries[s.read()]
		new.select()
		s._changed+=[old,new]
		s.draw()

	def move_vertical(s, val):
		def wrap(row):
			if (val < 0) * (row < 1):
				row = s.nrows[col]
			elif (val > 0) * (row > s.nrows[col]):
				row = 1
			assert row != 0
			return row
		old=s._entries[s.read()]
		old.deselect()
		row,col=s.rowcol(val,0)
		s.selector.write(s.col[col][wrap(row)][0])
		new=s._entries[s.read()]
		new.select()
		s._changed+=[old,new]
		s.draw()

	def right(s):
		s.move_horizontal(1)

	def left(s):
		s.move_horizontal(-1)

	def up(s):
		s.move_vertical(-1)

	def down(s):
		s.move_vertical(1)


# g=Grid()
# print(g)
#
# from libTerm import Term
# items=['xxxx','xxxx','yyyy','dasdf','dasdf','erwrsdd','sdf','pppfpf']
# t=Term()
# g=Grid(t,items,Coord(5,5),maxheight=3)
# g.draw()
# print()z
class Formatting:
	from libTerm import Ansi
	CSI = Ansi.CSI
	def __init__(s):
		s.lpad=''
		s.rpad=''
		s.select=Ansi.BOLD
		s.deselect=''
		s.focus=Ansi.COLSWP
		s.unfocus=Ansi.COLUNSWP
		s.choose=''
		s.confirm=''
		s.reset=Ansi.RESET
		s.maxwidth=None
		s.color=ColorSet(fg=Color(64,192,192),bg=None)

	@property
	def fg(s):
		return s.color.fg
	@fg.setter
	def fg(s,color):
		s.color.fg=color
