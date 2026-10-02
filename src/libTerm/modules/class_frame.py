#!/usr/bin/env python
from copy import deepcopy

from libTerm import Term
from libTerm import Coord,Color,Buffer,Ansi
from libTerm.components.enums import DrawState
from libTerm.modules.class_display import LineDisplay
from abc import ABCMeta, abstractmethod
import dataclasses
from dataclasses import dataclass,field
from collections import namedtuple
import asyncio

@dataclass()
class SymbolSet(namedtuple('Symbolset', ['LTC','RTC','VL','HL','LBC','RBC','TT','BT','LT','RT','LBT','RBT','LBB','RBB'])):
	__module__ = None
	__qualname__='SymbolSet'
	LTC: str = field(default=' ')
	RTC: str = field(default=' ')
	VL: str = field(default=' ')
	HL: str = field(default=' ')
	LBC: str = field(default=' ')
	RBC: str = field(default=' ')
	TT: str = field(default=' ')
	BT: str = field(default=' ')
	LT: str = field(default=' ')
	RT: str = field(default=' ')
	LBT: str = field(default=' ')
	RBT: str = field(default=' ')
	LBB: str = field(default=' ')
	RBB: str = field(default=' ')

	def __new__(cls, LTC=None, RTC=None, VL=None, HL=None, LBC=None, RBC=None, TT=None ,BT=None,LT=None,RT=None,LBT=None,RBT=None,LBB=None,RBB=None):
		# Pull default values from dataclass field definitions when arguments are omitted (None)
		df = getattr(cls, '__dataclass_fields__', None)
		def _d(name):
				f = df.get(name) if df else None
				return f.default if (f is not None and getattr(f, 'default', None) is not dataclasses.MISSING) else None

		LTC = LTC if LTC is not None else _d('LTC')
		RTC = RTC if RTC is not None else _d('RTC')
		VL = VL if VL is not None else _d('VL')
		HL = HL if HL is not None else _d('HL')
		LBC = LBC if LBC is not None else _d('LBC')
		RBC = RBC if RBC is not None else _d('RBC')
		TT = TT if TT is not None else _d('TT')
		BT = BT if BT is not None else _d('BT')
		LT = LT if LT is not None else _d('LT')
		RT = RT if RT is not None else _d('RT')
		LBT = LBT if LBT is not None else _d('LBT')
		RBT = RBT if RBT is not None else _d('RBT')
		LBB = LBB if LBB is not None else _d('LBB')
		RBB = RBB if RBB is not None else _d('RBB')
		return super(SymbolSet, cls).__new__(cls, LTC, RTC, VL, HL, LBC, RBC, TT, BT, LT, RT,LBT,RBT,LBB,RBB)
	def __getattr__(s, item):
		return {**s._asdict()}.get(item)
	def keys(s):
		return {**s._asdict()}.keys()
	def __dict__(s):
		return {**s._asdict()}


class FrameBase(metaclass=ABCMeta):
	STATE=DrawState

	def __init__(s,ctx=None,*a, **k):
		pass

class FixedSet(dict):
	def __init__(s,*a,**k):
		s._list=[]
		s._defaults = k.pop('defaults',{})
		s._missing=k.get('fallback')
		for i,key in enumerate(a):
			s.add(key)
			if i+1 <= len(s._defaults):
				s.__setitem__(key,s._defaults[i])
			elif len(s._defaults)==1:
				s.__setitem__(key,deepcopy(s._defaults[0]))
		if k:
			for key in k:
				s.add(key)
				s.__setitem__(key,k.get(key))





	def add(s,key):
		s._list+=[key]
		super().__setitem__(key,None)
	def __setitem__(s, key, value):
		if not key in s._list:
			raise AttributeError
		else:
			super().__setitem__(key,value)
	def __getitem__(s, key):
		if not key in s._list:
			raise KeyError
		else:
			return super().__getitem__(key)
	def __getattr__(s, key):
		if key.startswith('_'):
			val=super().__getattr__(key)
		else:
			val=s.__getitem__(key)
		return val

	def __setattr__(s, key, value):
		if key.startswith('_'):
			super().__setattr__(key,value)
		elif key in s._list:
			super().__setitem__(key,value)
		else:
			raise AttributeError

s=FixedSet('test', 'ikkel', 'zzz')
s.test='sss'
s['zzz']='best'
# s.bbb='llk'
print(repr(s))
print(s._list)

class Frame:
	"""
	a line display that is framed of in size , and can be used to
	print lines to. it fills the linebuffer untill full and then
	starts autoscrolling new prints. it allows for scrolling back up
	and down, by default lines are not wrapped but cropped , the cropped
	charakters can be accessed in scroll mode by moving the viewport right

	"""
	_symset=FixedSet('box','test','default','clearframe','user')
	STATE=DrawState

	def __init__(s,ctx=None,**k):
		s._symset.box = ' ─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕ ▖▗▘▙▚▛▜▝▞▟■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱'
		s._symset.default = SymbolSet(*'╭╮│─╰╯┬┴├┤┌┐└┘')
		s._symset.clearframe = SymbolSet()
		s._symset.test = SymbolSet(*'++|-++++++++++')
		s._ctx=ctx
		s._term=k.get('term', k.get('term', getattr(s._ctx, 'term', None)))
		s.name=k.get('name')
		s.props=FixedSet('name','title','border','linenumbers','focus','hidden','subtitle')
		s.props['title'] = k.get('title',s._makeTitle())
		s.props['border'] = k.get('border',True)
		s.linenrs=k.get('linenrs',True)
		s.subtitle='{SUBTITLE}'
		s._settings=FixedSet('focus','hidden','border','title')
		s._location=None
		s._size=None

		s._settings.focus=False
		s._settings.hidden=False
		s._settings.border=True
		s._settings.title=False

		s._flags=FixedSet('drawstate', 'asyncdraw', 'asyncdone','hidden', 'wrap', 'scroll','focus')
		s._str=FixedSet('frame', 'clearframe', 'wipe')
		s._lst=FixedSet('wipe', 'border', 'clearframe', 'test')
		s._tpl=FixedSet('LINE', 'BORDER', 'BUFFER', 'BORDERS', 'CLEAR', 'TEST', )
		s._tpl.BORDER=FixedSet('TOP', 'MID', 'BOT')
		s._mkup=FixedSet('ACTIVE', 'DEFAULT', 'FOCUS', defaults=[FixedSet('BG', 'FG', 'RESET', 'UNSET')])
		# s._mkup.DEFAULT=FixedSet('BH', 'FG', 'RESET', 'UNSET')
		# s._mkup.FOCUS=FixedSet('BH', 'FG', 'RESET', 'UNSET')
		s._flags.drawstate=DrawState(0)
		s._flags.asyncdraw=asyncio.Event()
		s._flags.asyncdone=asyncio.Event()
		s._flags.hidden=False
		s._flags.wrap=False
		s._flags.scroll=False
		s._flags.focus=False
		s.lines={}
		s.displays={}
		s.display=None
		s.location=k.get('location',Coord(1,1))
		s._setsize=k.get('size')
		s.size=k.get('size')

		s._str.frame= ''
		s._str.clearframe= ''
		s._str.wipe= ''

		s._lst.wipe={}
		s._lst.border={}
		s._lst.clearframe={}
		s._lst.test={}

		s._tpl.LINE= '{{XY}}{BG}{FG}{{LINE}}'
		s._tpl.BORDER.TOP= '{{XY}}{MKUP}{LTC}' + '{HL}' * (s.size.x - 2) + '{RTC}{{RESET}}'
		s._tpl.BORDER.MID= ['{{XYL}}{MKUP}{VL}{{RESET}}', '{{XYR}}{MKUP}{VL}{{RESET}}', ]
		s._tpl.BORDER.BOT= '{{XY}}{MKUP}{LBC}' + '{HL}' * (s.size.x - 2) + '{RBC}{{RESET}}'
		s._tpl.BUFFER={}
		s._tpl.BORDERS={}
		s._tpl.BORDERS[1] = s._tpl.BORDER.TOP.format(**s._symset.default._asdict(), MKUP='{BG}{FG}')
		s._tpl.BORDERS[2] = s._tpl.BORDER.MID[0].format(**s._symset.default._asdict(), MKUP='{BG}{FG}')
		s._tpl.BORDERS[3] = s._tpl.BORDER.MID[1].format(**s._symset.default._asdict(), MKUP='{BG}{FG}')
		s._tpl.BORDERS[4] = s._tpl.BORDER.BOT.format(**s._symset.default._asdict(), MKUP='{BG}{FG}')
		s._tpl.CLEAR={}
		s._tpl.CLEAR[1] = s._tpl.BORDER.TOP.format(**s._symset.clearframe._asdict(), MKUP='{BG}{FG}')
		s._tpl.CLEAR[2] = s._tpl.BORDER.MID[0].format(**s._symset.clearframe._asdict(), MKUP='{BG}{FG}')
		s._tpl.CLEAR[3] = s._tpl.BORDER.MID[1].format(**s._symset.clearframe._asdict(), MKUP='{BG}{FG}')
		s._tpl.CLEAR[4] = s._tpl.BORDER.BOT.format(**s._symset.clearframe._asdict(), MKUP='{BG}{FG}')
		s._tpl.TEST={}
		s._tpl.TEST[1] = s._tpl.BORDER.TOP.format(**s._symset.test._asdict(), MKUP='{BG}{FG}')
		s._tpl.TEST[2] = s._tpl.BORDER.MID[0].format(**s._symset.test._asdict(), MKUP='{BG}{FG}')
		s._tpl.TEST[3] = s._tpl.BORDER.MID[1].format(**s._symset.test._asdict(), MKUP='{BG}{FG}')
		s._tpl.TEST[4] = s._tpl.BORDER.BOT.format(**s._symset.test._asdict(), MKUP='{BG}{FG}')
		s._mkup.ACTIVE.BG= ''
		s._mkup.ACTIVE.FG= ''
		s._mkup.ACTIVE.RESET= '\x1b[m'
		s._mkup.ACTIVE.UNSET= Ansi.UNSET
		s._mkup.DEFAULT.BG= ''
		s._mkup.DEFAULT.FG= ''
		s._mkup.DEFAULT.RESET= '\x1b[m'
		s._mkup.DEFAULT.UNSET= Ansi.UNSET
		s._mkup.FOCUS.BG= ''
		s._mkup.FOCUS.FG= '\x1b[32m'
		s._mkup.FOCUS.RESET= '\x1b[m'
		s._mkup.FOCUS.UNSET= Ansi.UNSET
		s.setflag(s.STATE.START)
		# s.initspace()
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
		return s._location
	@location.setter
	def location(s,value):
		if not isinstance(value,Coord):
			value=Coord(value)
		s._location=value
		for disp in s.displays:
			s.displays[disp].location=s._location
	@property
	def size(s):
		if s._size is None:
			s._size=s._term.size.xy
		if s._size.y < 3:
			s._size =  Coord(s._size.x,3)
		return s._size
	@size.setter
	def size(s,value):
		s._size=value
		for disp in s.displays:
			s.displays[disp].size=s._size+Coord(-2,-2)

			s.makeFrame()
	def _build(s):
		opts=s._flags['MKUP']['ACTIVE']
		locx=s.location.x
		locy=s.location.y
		s._lst['border'][1] =s._tpl['BORDERS'][1].format(XY=s.location, **opts)
		j=0
		for i in range(2,s.size.y-1):
			XYL=s.location + Coord(0, i - 1)
			XYR=s.location + Coord(s.size.x-1,i-1)
			p1=s._tpl['BORDERS'][2].format(XYL=XYL, **opts)
			p2=s._tpl['BORDERS'][3].format(XYR=XYR, **opts)
			s._lst['border'][i]=(p1 + p2)
			j=i
		s._lst['border'][j + 1] = s._tpl['BORDERS'][4].format(XY=s.location + Coord(0, j), **opts)
		s.frame=''.join(s._lst['border'].values())
		s._str['frame']= ''.join(s._lst['border'].values())
	def _clear(s):
		opts=s._flags['MKUP']['ACTIVE']
		locx=s.location.x
		locy=s.location.y
		s._lst['clear'][1] =s._tpl['CLEAR'][1].format(XY=s.location, **opts)
		j=0
		for i in range(2,s.size.y-1):
			XYL=s.location + Coord(0, i - 1)
			XYR=s.location + Coord(s.size.x-1,i-1)
			p1=s._tpl['CLEAR'][2].format(XYL=XYL, **opts)
			p2=s._tpl['CLEAR'][3].format(XYR=XYR, **opts)
			s._lst['clear'][i]=(p1 + p2)
			j=i
		s._lst['clear'][j + 1] = s._tpl['CLEAR'][4].format(XY=s.location + Coord(0, j), **opts)
		s.frame=''.join(s._lst['clear'].values())
		s._str['clear']= ''.join(s._lst['clear'].values())

	def _test(s):
		opts=s._flags['MKUP']['ACTIVE']
		locx=s.location.x
		locy=s.location.y
		s._lst['test'][1] =s._tpl['TEST'][1].format(XY=s.location, **opts)
		j=0
		for i in range(2,s.size.y-1):
			XYL=s.location + Coord(0, i - 1)
			XYR=s.location + Coord(s.size.x-1,i-1)
			p1=s._tpl['TEST'][2].format(XYL=XYL, **opts)
			p2=s._tpl['TEST'][3].format(XYR=XYR, **opts)
			s._lst['test'][i]=(p1 + p2)
			j=i
		s._lst['test'][j + 1] = s._tpl['TEST'][4].format(XY=s.location + Coord(0, j), **opts)
		s.frame=''.join(s._lst['test'].values())
		s._str['test']= ''.join(s._lst['test'].values())



	def _drawFrame(s):
		print(s._str['frame'], end='', flush=True)
	def _clearFrame(s):
		print(s._str['test'], end='', flush=True)
	def _testFrame(s):
		print(s._str['test'], end='', flush=True)

	def _makeTitle(s):
		nosep=''
		if isinstance(s.name,str):
			noprefix=s.name.lstrip('frm')
			nosep=noprefix.lstrip('_')
		return nosep

	def focus(s,val=True):
		s._flags.focus=val
		if s._flags.focus:
			s.MKUP.ACTIVE=s.MKUP.FOCUS
		else:
			s.MKUP.ACTIVE=s.MKUP.DEFAULT
		s.draw()
		
	def show(s,val=True):
		s._hidden=not val
		for disp in s.displays:
			s.displays[disp].show(val)
		s._state=2
		s.draw()


	async def adraw(self):
		if 	s._flags['asyncdraw'].is_set():
			await s._flags['asyncdone'].wait()
			s._flags['asyncdone'].clearframe()
			return
	def drawqueue(s):
		loop=asyncio.get_running_loop()

	def checkflag(s,flag,):
		if flag == s.STATE.INIT:
			s._flags.drawstate-=s.STATE.INIT

	def draw(s):
		from signal import Signals,pause,SIGUSR1
		draw=s.STATE
		INIT=draw.INIT
		WIPE=draw.WIPE
		CLEAR=draw.CLEAR
		DEFAULT=draw.DEFAULT


		if s.checkflag(INIT):
			print('init')
			s._build()
			s._clear()
			s._test()
			s.setflag(draw.DRAW)
			s.setflag(draw.DEFAULT)

		if s.checkflag(draw.DEFAULT,clear=False):
			if s.checkflag(draw.START,new=draw.INIT):
				s.raw()

		print('4')

		s._flags['asyncdraw'].set()

		if draw.DEFAULT in s.drawflag:
			print('DEFAULT')

			if checkflag(draw.WIPE,draw.DRAW):
				pstate()
				s._testFrame()
				# s._makeFrame()
			if checkflag(draw.CLEAR,draw.DRAW):
				pstate()
				s._clearFrame()
				# s._makeFrame()
			if checkflag(draw.UPDATE,draw.DRAW):
				pstate()
				# s.update_buffers()
				# forcedraw()
			if checkflag(draw.BUILD,draw.DRAW):
				s._build()
				pstate()

			if checkflag(draw.REBUILD,draw.DRAW) :
				s._clear()
				s._build()
				pstate()
			if checkflag(draw.REDRAW):
				pass

		if checkflag(draw.DRAW) :
			pstate()
			if not s._flags['hidden']:
				s._drawFrame()
				for disp in s.displays:
					s.displays[disp].draw()
			s.clearframeflag(draw.DRAW)
		s._flags['asyncdraw'].clearframe()







		# if s._state==0:
		#
		# elif s._state==1:
		# 	s._clearFrame()
		# 	s._makeFrame()
		# elif s._state==2:
		# 	s._wipeFrame()
		# 	s._makeFrame()
		# if not s._hidden:
		# 	for disp in s.displays:
		# 		s.displays[disp].state=s._state
		# 		s.displays[disp].draw()
		# 	s._drawFrame()
		# 	s._state=3

	def addDisplay(s,name,disp,select=True):
		did=len(s.displays)+1
		s.displays[did]=disp(ctx=s._ctx, parent=s, name=name)
		s.selectDisplay(did)
		return s.displays[did]
	def addMenu(s,menu,**opts):
		# fg = Color(0, 196, 196)
		# mycolors = ColorSet(fg=fg)
		did=len(s.displays) + 1
		s.displays[did]=menu(s, **opts)
		s.selectDisplay(did)
	def selectDisplay(s,n=1):
		s.display=s.displays.get(n)

	def print(s,line):
		s.display.print(line)
	def printto(s,display,line):
		s.displays[display].print(line)

	def move(s,location):
		s._flags['drawstate']^=s.STATE.WIPE
		s.location=s.location+location
		s.draw()

	def h_resize(s,val):
		s._flags['drawstate']^=s.STATE.WIPE
		s.size=Coord(s.size.x+val,s.size.y)
		s.draw()

	def v_resize(s,val):
		s._flags['drawstate']^=s.STATE.WIPE
		s.size = Coord(s.size.x, s.size.y + val)
		s.draw()



class FrameSet:

	def newFrame(s,term=None,name=None,location=Coord(1,1),size=Coord(80,5),display=None,linenrs=True,border=True):
		framename='frm_'+name.lstrip('frm_')
		s.__setattr__(framename,Frame())

