#!/usr/bin/env python
from libTerm import Term
from libTerm import Coord,Color,Buffer,Ansi
from libTerm.modules.class_display import LineDisplay
import dataclasses
from dataclasses import dataclass,field
from collections import namedtuple

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


class Frame:
	"""
	a line display that is framed of in size , and can be used to
	print lines to. it fills the linebuffer untill full and then
	starts autoscrolling new prints. it allows for scrolling back up
	and down, by default lines are not wrapped but cropped , the cropped
	charakters can be accessed in scroll mode by moving the viewport right

	"""
	def __init__(s,ctx=None,**k):
		s.boxsyms=' ─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕ ▖▗▘▙▚▛▜▝▞▟■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱'
		s.symbolset=SymbolSet(*'╭╮│─╰╯┬┴├┤┌┐└┘')
		s.clearset=SymbolSet()
		s.ctx=ctx
		s.term=k.get('term',k.get('t',getattr(s.ctx, 'term',None)))
		s.name=k.get('name')
		s.title=k.get('title',s.maketitle())
		s.border=k.get('border',True)
		s.linenrs=k.get('linenrs',True)

		s.subtitle='{SUBTITLE}'


		s._draw=0
		s._location=None
		s._size=None
		s._focus=False
		s._hidden=False


		s.lines={}

		s.displays={}
		s.display=None

		s.location=k.get('location')

		s._setsize=k.get('size')
		s.size=k.get('size')


		s.framestr=''
		s.framestr_clear=''
		s.framewipelst=[]




		s.tpl={}
		s.tpl['BORDER']={}
		s.tpl['BORDER']['TOP']='{{XY}}{MKUP}{LTC}'+'{HL}'*(s.size.x-2)+'{RTC}{{RESET}}'
		s.tpl['BORDER']['MID']= ['{{XYL}}{MKUP}{VL}{{RESET}}','{{XYR}}{MKUP}{VL}{{RESET}}',]
		s.tpl['BORDER']['BOT']='{{XY}}{MKUP}{LBC}'+'{HL}'*(s.size.x-2)+'{RBC}{{RESET}}'
		s.tpl['BORDERS']={}
		s.tpl['CLEAR']={}
		s.tpl['LINE']='{{XY}}{BG}{FG}{{LINE}}'
		s.tpl['BUFFER']={}
		s.tpl['BORDERS'][1] = s.tpl['BORDER']['TOP'].format(**s.symbolset._asdict(),MKUP='{BG}{FG}')
		s.tpl['BORDERS'][2] = s.tpl['BORDER']['MID'][0].format(**s.symbolset._asdict(), MKUP='{BG}{FG}')
		s.tpl['BORDERS'][3] = s.tpl['BORDER']['MID'][1].format(**s.symbolset._asdict(), MKUP='{BG}{FG}')
		s.tpl['BORDERS'][4] = s.tpl['BORDER']['BOT'].format(**s.symbolset._asdict(),MKUP='{BG}{FG}')
		s.tpl['CLEAR'][1] = s.tpl['BORDER']['TOP'].format(**s.clearset._asdict(),MKUP='{BG}{FG}')
		s.tpl['CLEAR'][2] = s.tpl['BORDER']['MID'][0].format(**s.clearset._asdict(),MKUP='{BG}{FG}')
		s.tpl['CLEAR'][3] = s.tpl['BORDER']['MID'][1].format(**s.clearset._asdict(),MKUP='{BG}{FG}')
		s.tpl['CLEAR'][4] = s.tpl['BORDER']['BOT'].format(**s.symbolset._asdict(),MKUP='{BG}{FG}')
		# s.initspace()

	def maketitle(s):
		nosep=''
		if isinstance(s.name,str):
			noprefix=s.name.lstrip('frm')
			nosep=noprefix.lstrip('_')
		return nosep

	def focus(s,val=None):
		if val is None:
			val=not s._focus
		s._focus=val
		s.makeFrame()
		s.redraw()

	def show(s,val=None):
		if val is None:
			val=not s._hidden
		else:
			val=not val
		s._hidden=val
		s.draw()

	def makeFrame(s,LCR=None):
		# print(s.symbolset._asdict())

			# print(f'{i=}')
		opts = {'BG': '', 'FG': '', 'RESET': '\x1b[m', 'UNSET': Ansi.UNSET}
		if s.border:
			if s._focus:
				opts['FG']='\x1b[1m'
			else:
				opts['FG']=''

			s.lines[1] =s.tpl['BORDERS'][1].format(XY=Coord(s.location.x,s.location.y),**opts)
			for i in range(s.size.y):
				s.lines[2+i]=(s.tpl['BORDERS'][2].format(XYL=Coord(s.location.x,s.location.y+1+i),**opts)+
							  s.tpl['BORDERS'][3].format(XYR=Coord(s.location.x+s.size.x-1,s.location.y+1+i),**opts))
				s.framewipelst+=[ s.tpl['CLEAR'][2].format(XYL=Coord(s.location.x, s.location.y+i), **opts)]
				s.framewipelst+=[ s.tpl['CLEAR'][3].format(XYR=Coord(s.location.x+s.size.x-1, s.location.y+i), **opts)]
			s.lines[len(s.lines)] = s.tpl['BORDERS'][4].format(XY=Coord(s.location.x, s.location.y + s.size.y-1), **opts)
			for line in s.lines:
				print(s.lines[line])
			s.frame=''.join(s.lines.values())
			s.framewipelst=[*s.framewipelst]
			s.framestr_clear=''.join(s.framewipelst)

	@property
	def location(s):
		return s._location
	@location.setter
	def location(s,value):
		if not isinstance(value,Coord):
			value=Coord(value)
		s._location=value
		for disp in s.displays:
			s.displays[disp].location= s._location + Coord(2, 2)
		if s._draw !=0 :
			s.redraw()
	def _displaylocation(s):
		return s._location + Coord(2, 2)
	@property
	def size(s):
		if s._size is None:
			s._size-s.term.size.xy
		return s._size
	@size.setter
	def size(s,value):
		s._size=value
		for disp in s.displays:
			s.displays[disp].size=s._size+Coord(-2,-2)

	def _displaysize(s):
		return s._size+Coord(-2,-2)

	def draw(s):
		if not s._hidden:
			if s._draw==0:
				s._draw=1
				s.firstdraw()
			else:
				for disp in s.displays:
					s.displays[disp].flag['redraw']=True
					s.displays[disp].draw()

	def drawframe(s):
		print(s.framestr,end='',flush=True)

	def firstdraw(s):
		if s.location and s.size :
			s.makeFrame()
			s.drawframe()
			s.draw()

	def redraw(s):
		if s.location:
			print(s.framestr_clear)
			s.makeFrame()
			s.draw()
			s.drawframe()

			# s.drawframe()
			# s.draw()

	def addDisplay(s,name,disp):
		did=len(s.displays)+1
		s.displays[did]=disp(s,name)
		return did

	def selectDisplay(s,n=1):
		s.display=s.displays.get(n)
		s.display.show(True)
		s.display.draw()

	def addMenu(s,menu,**opts):
		# fg = Color(0, 196, 196)
		# mycolors = ColorSet(fg=fg)
		did=len(s.displays) + 1
		s.displays[did]=menu(s, **opts)
		s.selectDisplay(did)



	def print(s,line):
		s.display.print(line)
	def clear(s):
		print(s._clear, end='', flush=True)

	def move(s,location):
		s.clear()
		s.location=s.location+location
		s.makeFrame()
		s.draw()
	def h_resize(s,val):
		s.clear()
		s.size=Coord(s.size.x+val,s.size.y)
		s.makeFrame()
		s.draw()

	def v_resize(s,val):
		s.clear()
		s.size = Coord(s.size.x, s.size.y + val)
		s.makeFrame()
		s.draw()


class FrameSet:

	def newFrame(s,term=None,name=None,location=Coord(1,1),size=Coord(80,5),display=None,linenrs=True,border=True):
		framename='frm_'+name.lstrip('frm_')
		s.__setattr__(framename,Frame())

