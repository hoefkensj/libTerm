#!/usr/bin/env python
import asyncio

from libTerm import Coord,Colors,Ansi,Move
from libTerm import Term
from libTerm.components.enums import DrawState
from abc import ABCMeta, abstractmethod


# class LineDisplay:
# 	def __init__(s, ctx, pkg, location, size):
# 		s.ctx = ctx
# 		# s.pkg=pkg
# 		s.loc = location
# 		s.size = size
# 		s.build()
# 		s.tpl_line = '\x1b[{Y};{X}H{MKUP}{LINE}\x1b[m'
# 		s.linetpl = ''
# 		s.mkup = '\x1b[38;2;160;160;160m'
# 		s.tpl_lines = []
# 		s._scroll = False
# 		s._wrap = False  # were there any wraps
# 		s._wordwrap = False  # True to enable wrapping
# 		s.viewrange = (-s.size.y, -s.size.y + s.size.y)
# 		s.viewshift = 0
# 		s.linecount = 0
# 		s.lines = []
# 		s.data = []
# 		s.buffer = None
# 		s.update()
# 		s.m = 0
#
#
# 	def scroll(s, val):
# 		if not s._scroll:
# 			last = len(s.data)
# 			first = last - s.size.y
# 			s.viewrange = (first, last)
# 			s._scroll = True
# 		first, last = s.viewrange
# 		first += val
# 		last += val
# 		s.viewrange = (first, last)
# 		for l, line in enumerate(s.data[first:last]):
# 			print(s.linetpl.format(Y=s.loc.y + l, LINE=s.crop(line)), end='', flush=True)
# 		if s._scroll:
# 			if s.viewrange[1] == s.linecount:
# 				s._scroll = False
# 				s.update()
#
#
# 	def shift(s, val):
# 		if not s._shift:
# 			s.viewshift = 0
# 			s._shift = True
# 		s.viewshift += val
# 		for line, tpl in zip(s.data[-s.size.y:], s.tpl_lines):
# 			print(tpl.format(LINE=s.crop(line)), end='', flush=True)
#
#
# 	def control(s, key):
# 		if key == '\x1b[B':
# 			s.scroll(1)
# 		elif key == '\x1b[A':
# 			s.scroll(-1)
#
#
# 	def crop(s, line):
# 		if len(line) >= s.size.x:
# 			while len(line) > (s.size.x - 4):
# 				line = line[s.viewshift:-4 + s.viewshift]
# 			line += '\x1b[{G}G\x1b[38;2;64;192;64m⟫\x1b[m'.format(G=s.loc.x + s.size.x - 2)
# 		else:
# 			line = line.ljust(s.size.x).rjust(s.size.x)
# 		return line
#
#
# 	def build(s):
# 		s.linetpl = s.tpl_line.format(Y='{Y}', X=s.loc.x, LINE='{LINE}', MKUP=s.mkup)
#
#
# 	def append(s, line):
# 		if s.linecount < s.size.y:
# 			s.data[s.linecount] = line.rstrip('\n')
# 		else:
# 			s.data.append(line.rstrip('\n'))
# 		s.linecount += 1
# 		s.update()
#
#
# 	def update(s):
# 		if not s._scroll:
# 			for l, line in enumerate(s.data[s.viewrange[1]:s.viewrange[0]]):
# 				print(s.linetpl.format(Y=s.loc.y + s.size.y - l, LINE=s.crop(line)), end='', flush=True)
#
class ViewRange():
	def __init__(s,start,size):
		s._start=start
		s.size=size
		s._stop=start+size-1

	def shift(s,value=1):
		if (s._start+value) >= 0:
			s._start+=value
			s._stop+=value

	@property
	def start(s):
		return s._start
	@start.setter
	def start(s,val):
		if val >= 0:
			s._start=val
			s._stop=val+s.size-1

	@property
	def stop(s):
		return s._stop
	@stop.setter
	def stop(s,val):
		start=val-s.size
		if start >= 1:
			s._stop=val
			s._start=val-s.size
		else:
			s._stop=val
			s._start=1


	def __call__(s):
		return list(range(s.start,s.stop))

	def __str__(s):
		return f'ViewRange({s.start},{s.stop})'

class Markup():
	def __init__(s,name):
		s.name=name
	def set(s,property,value):
		s.__setattr__(property,value)

	def get(s,*props):
		return '\x1b['+';'.join([s.__getattribute__(prop) for prop in props])+'m'

class TemplateSet:
	def __init__(s,):
		s._location='{XY}'
		s._markups={'HL':'{HL}{DATA}{NOHL}','FG':'{FG}{DATA}{NOFG}','BG':'{BG}{DATA}{NOBG}','UL':'{UL}{DATA}{NOUL}'}
		s._controls={'SEL':'{SEL}{DATA}{SEL}','FOC':'{FOC}{DATA}{FOC}','PIC':'{PIC}{DATA}{PIC}','CNF':'{CNF}{DATA}{CNF}'}
		s._markup='{MKUP}'
		s._demarkup='DMKUP'
		s._control='{CTRL}'
		s._decontrol='{DCTRL}'
		s._prefix='{PREFIX}'
		s._leftpad='{LPAD}'
		s._rightpad='{RPAD}'
		s._data='{DATA}'
		s._suffix='{SUFFIX}'
		s._end='{RESET}'
	def apply_mkup(s,item,markup=None):
		if markup=='all'|markup is None:
			for mkup in s.markups:
				item=s.apply_mkup(item,mkup)
			else:
				item=s.markups[markup].format(data=item)
		return item
	def apply_ctrl(s,item,control=None):
		if control=='all'| control is None:
			for ctrl in s.markups:
				item=s.apply_control(item,ctrl)
			else:
				item=s.controls[control].format(data=item)
		return item



	# def enable(s,):
	def __str__(s):
		return '{LOC}{CTRL}{PREFIX}{DATA}{SUFFIX}{END}'.format(**s)
	def __dict__(s):
		return {'LOC':s.location,
		'CTRL':s.control,
		'PREFIX':s.markup+s.prefix+s.demarkup,
		'DATA':s.markup+s.data+s.demarkup,
		'SUFFIX':s.markup+s.suffix+s.demarkup,
		'END':s.end	}

ColorSet=Colors.Set
Color=Colors.Color

default_markup=Markup('display')
default_markup.line=Markup('line')
default_markup.line.default=Markup('default')
default_markup.line.default.colors=ColorSet(fg=Color(160,160,160),bg=Color(16,16,16))
default_markup.line.default.mkup=''
default_markup.line.selected=Markup('selected')
default_markup.line.selected.colors=ColorSet(fg=Color(160,160,160),bg=Color(64,192,64))
default_markup.line.selected.mkup='\x1b[7m'
default_markup.lnr=Markup('lnr')
default_markup.lnr.default=Markup('default')
default_markup.lnr.default.colors=ColorSet(fg=Color(128,128,128),bg=Color(64,64,64))
default_markup.lnr.default.mkup=''
default_markup.lnr.selected=Markup('selected')
default_markup.lnr.selected.colors=ColorSet(fg=Color(160,160,160),bg=Color(64,192,64))
default_markup.lnr.selected.mkup=''

from libTerm.components.tools import Cascade
class DisplayBase(metaclass=ABCMeta):
	STATE=DrawState
	def __init__(s, ctx=None, parent=None,*a, **k):
		s.ctx=ctx
		s.parent=parent
		s.hasparent=True if parent is not None else False
		s.term=Cascade(
		            None,
		            lambda:k.get('term'),
					   lambda:s.parent._term,
					   lambda:Term()
		)
		s.name=k.get('name',k.get('id'))
		s.opts={}
		s.opts['numbers']=True
		s.opts['gutter']=True
		s.opts['bullets']=False
		s.opts['gutters']=False
		s.opts['hidden']=False
		s.opts['wrap']=False
		s.opts['scroll']=False
		s.tool={}
		s.tool['symbols']={}
		s.tool['symbols']['bullet']='⟪«‹… …›»⟫'
		s.limits={}
		s._location=None
		s._size=None
		s._ctlflags={}
		s._ctlflags['overflow']=False
		s._ctlflags['scroll']=False
		s._ctlflags['shift']=False
		s._ctlflags['wrap']=False
		s._viewrange={}
		s._viewrange['v']=ViewRange(1,40)
		s._viewrange['h']=ViewRange(1,80)
		s._count={}
		s._flags={}
		s._flags['drawstate']=DrawState(0)
		s._flags['asyncdraw']=asyncio.Event()
		s._flags['asyncdone']=asyncio.Event()
		s._flags['overflow']=False
		s._data={}
		s._cache={}
		s._templates={}
		s._templates['default']={}
		s._buffers={}
	@property
	def drawflag(s):
		return s._flags['drawstate']
	@drawflag.setter
	def drawflag(s, flags):
		s._flags['drawstate']=flags
	def toggleflag(s,flags):
		s._flags['drawstate']^=flags
	def setflag(s,flags):
		s._flags['drawstate']|=flags
	def clearflag(s,flags):
		s._flags['drawstate']&=~flags

	@property
	def location(s):
		if s._location is None:
			if s.hasparent:
				s._location=s.parent.location+Coord(2,2)
			else:
				s._location=Coord(1,1)
		return s._location
	@location.setter
	def location(s,val):
		draw = s.STATE
		s._location=val+Coord(2, 2)
		s.drawflag = draw.WIPE | draw.UPDATE | draw.DRAW
		print('\x1b[1;120H'+repr(s.drawflag),end='',flush=True)

		s.draw()
	@property
	def size(s):
		if s._size is None and s.parent is not None:
			s._size=s.parent.size+Coord(-2,-3)
		s.state=1
		return s._size

	@size.setter
	def size(s,val):
		draw = s.STATE
		s._size=val+Coord(-2,-3)
		s.drawflag= draw.WIPE | draw.REBUILD | draw.DRAW
		print('\x1b[1;120H'+repr(s.drawflag),end='',flush=True)
		s.draw()


class LineDisplay(DisplayBase):
	"""
	a line display that is framed of in size , and can be used to
	print lines to. it fills the linebuffer untill full and then
	starts autoscrolling new prints. it allows for scrolling back up
	and down, by default lines are not wrapped but cropped , the cropped
	charakters can be accessed in scroll mode by moving the viewport right

	"""

	def __init__(s,ctx=None,parent=None,**k):
		super().__init__(ctx=ctx,parent=parent,**k)
		s._viewrange['v'] = ViewRange(1, 40)
		s._viewrange['h'] = ViewRange(1, 80)
		s._data['lines']={}
		s._data['idx']=0
		s._count['lines']=0
		s._cache['longest_line']=0
		s._buffers['print']={}
		s._buffers['line']={}
		s._buffers['clear']={}
		s.mkup=default_markup
		s._templates['default']['LINE']={}
		s._templates['default']['LINE']['LOC']='{XY}'
		s._templates['default']['LINE']['CTRL']='{MODS}'
		s._templates['default']['LINE']['PREFIX']='{MKUP}{LPAD}{{PREFIX}}{RPAD}{END}'
		s._templates['default']['LINE']['LINE']='{MKUP}{LPAD}{{LINE}}{RPAD}{END}'
		s._templates['default']['LINE']['SUFFIX']='{MKUP}{LPAD}{{SUFFIX}}{RPAD}{END}'
		s._templates['default']['LINE']['END']='{RESET}'
		s._templates['default']['GUTTER']= {}
		s._templates['default']['GUTTER']['NUMBER']='{NUM}'
		s._templates['default']['MODS']='{SEL}{FOC}{PIC}{CNF}'
		s._templates['default']['MKUP']='{FG}{BG}{HL}{UL}'
		s.drawflag=DrawState.NONE
		s.draw()

	def __len__(s):
		return s._data['idx']
	def _measure(s,line):
		cur=s._cache['longest_line']
		l=len(line)
		if l > cur:
			s._cache['longest_line'] = l
			s.extendlines()

	@property
	def lines(s):
		return s._data['lines'].values()
	def _printrange(s, xy):
		x={}
		y={}
		x['start']=s.location.x
		y['start']=s.location.y
		x['stop']=s.location.x+s.size.x
		y['stop']=s.location.y+s.size.y
		XY={'x':x,'y':y}

		return XY.get(xy)

	def print(s,line):
		"""
		Prints/Appends a line to the display
		:param line: the string/line to append
		:return:
		"""
		s.addline(line.rstrip("\n"))
		s._flags['drawstate']=s.STATE.UPDATE
		s.draw()

	# def initspace(s):
	# 	# s.printrng('y')
	#
	# 	line = s._buffers['print'][l]
	# 	wipe = ' ' * (s.size.x - 4)
	# 	xy = f'\x1b[{{Y}};{s.location.x}H'
	# 	ltpl = s._templates['default']['LINE']
	# 	mtpl = s._templates['default']['MKUP']
	#
	# 	if s.opts['hidden'] is False:
	# 		for l in range(1,s.size.y):
	# 			mkup = mtpl.format(FG='',  BG='',  UL='', HL='')
	# 			loc = ltpl['LOC'].format(XY=xy.format(Y=line))
	# 			prefix = ltpl['PREFIX'].format(LPAD='', RPAD='', MKUP=mkup)
	# 			suffix = ltpl['SUFFIX'].format(LPAD='', RPAD='', MKUP=mkup)
	#
	# 			print(line['LINE'].format(SEL='',LINE=wipe,LNR=gutter))

	def show(s,val=True):
		s._hidden=not val
		s.draw()

	def _build(s):
		xy = f'\x1b[{{Y}};{s.location.x}H'
		ltpl=s._templates['default']['LINE']
		mtpl=s._templates['default']['MKUP']

		rng=s._printrange('y')
		vp=range(rng['start'],rng['stop'])
		for l,line in enumerate(vp,start=1):

			if s.opts['gutter']:
				pfxbg=s.mkup.lnr.default.colors.bg.ansibg
			else:
				pfxbg=''


			mkup=mtpl.format(FG=s.mkup.lnr.default.colors.fg.ansifg,
							 BG=pfxbg,
							 UL='', HL='')
			loc=ltpl['LOC'].format(XY=xy.format(Y=line))
			prefix=ltpl['PREFIX'].format(LPAD='',RPAD='',MKUP=mkup,END='\x1b[m')
			suffix=ltpl['SUFFIX'].format(LPAD='',RPAD='',MKUP=mkup,END='\x1b[m')
			line=ltpl['LINE'].format(LPAD='',RPAD='',MKUP='',END='\x1b[m')
			s._buffers['line'][l]={}
			s._buffers['line'][l]['LOC']=loc
			s._buffers['line'][l]['LINE']=prefix+line+suffix
			s._buffers['line'][l]['WIPE']=' '*s.size.x
			s._buffers['clear'][l]=loc+s._buffers['line'][l]['WIPE']

	def frame_fill(s, adjust):
		for l, idx in enumerate(s._data['lines'], start=1):
			tpls = s._buffers['line'][l]
			line = s._data['lines'][idx]
			if s.opts['numbers']:
				nr = f'{idx}. '.rjust(len(str(idx)) + 3)
				lnr = s._templates['default']['GUTTER']['NUMBER'].format(NUM=nr)
				adjust = -len(nr)
			if not s.opts['wrap']:
				line = line['crop'](adjust=adjust)
			
			s._buffers['print'][l] = [str(s._buffers['line'][l]['LOC'])]
			s._buffers['print'][l] += [tpls['LINE'].format(PREFIX=lnr, LINE=line, SUFFIX='')]

	def frame_autoscroll(s,adjust):
		for l in range(1, s.size.y + 1):
			tpls = s._buffers['line'][l]
			offset = s._viewrange['v'].start + l
			line = s._data['lines'][offset]
			if s.opts['numbers']:
				nr = f'{offset}. '.rjust(4)
				lnr = s._templates['default']['GUTTER']['NUMBER'].format(NUM=nr)
				adjust = -len(nr)
			if not s.opts['wrap']:
				line = line['crop'](adjust=adjust)
			s._buffers['print'][l] = [stdfr(s._buffers['line'][l]['LOC'])]
			s._buffers['print'][l] += [tpls['LINE'].format(PREFIX=lnr, LINE=line, SUFFIX='')]

	def update_buffers(s):

		adjust=0
		if not s._ctlflags['overflow']:
			s.frame_fill(adjust)

		else:
			s.frame_autoscroll(adjust)

	def extendlines(s):
		for line in s._data['lines'].values():
			if len(line['data']) < s._cache['longest_line']:
				line['data'].ljust(s._cache['longest_line'])
				line['crop']=s.crop(line['data'])

	def wrap(s,line):
		# TODO: figure this out as it seems impossible with this setup
		def wrapped(adjust=0):

			save=ctx._term.cursor.quicksave
			load=ctx._term.cursor.quickload
			down=Move.DOWN
			maxw   = s._viewrange['h'].size
			start  = s._viewrange['h'].start
			stop   = s._viewrange['h'].stop+adjust+2
			ol = line.ljust(maxw).rjust(maxw)
			ll=[]
			while ol :
				ll+=[save()+ol[:maxw]+load()+down()]
				ol=ol[maxw:]


	def crop(s,line):
		def cropped(adjust=0):
			cropping = False
			clipping = False
			nfix   = color(64,192,64).ansi.fg + '…' + '\x1b[39m'
			maxw   = s._viewrange['h'].size
			start  = s._viewrange['h'].start
			stop   = s._viewrange['h'].stop+adjust+2
			suffix = f' [{nfix}]' if len(line)>(maxw+adjust) else False
			l      = line.ljust(maxw).rjust(maxw)[start:stop]
			crop   = line.ljust(maxw).rjust(maxw)[stop:]
			if crop.strip(' ')!='':
				cropping=True
			if start > 0:
				clipping=True
			if clipping:
				l=nfix+l[:-1]
			if cropping:
				l=l[:-5]+suffix

			#
			# if len(l)<s._viewrange['h'].size+adjust:
			# 	l+=' '*(s._viewrange['h'].size+(adjust-len(l)))

			return l
		return cropped

	def addline(s,line):
		s._data['idx']+=1
		s._measure(line)
		s._data['lines'][s._data['idx']]={'data':line,'crop':s.crop(line)}
		if not s._ctlflags['overflow']:
			s._viewrange['v'].stop=s._data['idx']
			# print('\x1b[2;1H',s.data_idx,s._viewrange['v'])

		if s._data['idx'] == s.size.y:
			s._ctlflags['overflow']=True

	def scroll(s, val):
		v=val
		draw = s.STATE
		if not s._scroll:
			s._scroll = True
		if s._scroll:
			if s._viewrange['v'].stop+1 == s._data['idx']:
				s._scroll = False
			elif s._viewrange['v'].start == 1:
				v=0
			elif val ==0:
				s._scroll= False
		s._viewrange['v'].shift(v)
		s.drawflag=draw.WIPE | draw.REBUILD | draw.DRAW
		s.draw()

	def shift(s,val):
		if not s._shift:
			s._shift = True
		s._viewrange['h'].shift(val)
		s.update_buffers()

	def wipelines(s):
		for idx in s._buffers['clear']:
			print(s._buffers['clear'][idx], end='', flush=True)

	def draw(s):
		draw=s.STATE
		def pstate():
			print('\x1b[1;120H' + repr(s.drawflag), end='', flush=True)

		def forcedraw():
			if draw.DRAW not in s.drawflag:
				s.drawflag=draw.DRAW

		if draw.START in s.drawflag:
			s.drawflag = draw.INIT

		if draw.INIT in s.drawflag:
			s._build()
			s.clearflag(draw.INIT)
			s.setflag(draw.DEFAULT)
			pstate()
			forcedraw()

		if draw.DEFAULT in s.drawflag:
			if draw.WIPE in s.drawflag:
				s.drawflag = draw.WIPE
				pstate()
				s.wipelines()

			if draw.CLEAR in s.drawflag:
				pstate()
				s.drawflag = draw.CLEAR

			if draw.UPDATE in s.drawflag:
				s.drawflag = draw.UPDATE
				pstate()
				s.update_buffers()
				forcedraw()

			if draw.BUILD in s.drawflag:
				s.drawflag = draw.BUILD
				pstate()
			if draw.REBUILD in s.drawflag:
				s.drawflag = draw.REBUILD
				pstate()

			if draw.DRAW in s.drawflag:
				pstate()
				s.drawflag = draw.DRAW
				if not s.opts['hidden']:
					for idx in s._buffers['print']:
						print(''.join(s._buffers['print'][idx]),end='',flush=True)


