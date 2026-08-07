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
		s.term=k.get('term',k.get('term',getattr(s.ctx, 'term',None)))
		s.name=k.get('name')
		s.title=k.get('title',s._makeTitle())
		s.border=k.get('border',True)
		s.linenrs=k.get('linenrs',True)
		s.subtitle='{SUBTITLE}'
		s._state=0
		s._location=None
		s._size=None
		s._focus=False
		s._hidden=False
		s.lines={}
		s.displays={}
		s.display=None
		s.location=k.get('location',Coord(1,1))
		s._setsize=k.get('size')
		s.size=k.get('size')
		s.str={}
		s.str['frame']=''
		s.str['clear']=''
		s.str['wipe']=''
		s.lst={}
		s.lst['wipe']={}
		s.lst['border']={}

		s.tpl={}
		s.tpl['LINE']='{{XY}}{BG}{FG}{{LINE}}'
		s.tpl['BORDER']={}
		s.tpl['BORDER']['TOP']='{{XY}}{MKUP}{LTC}'+'{HL}'*(s.size.x-2)+'{RTC}{{RESET}}'
		s.tpl['BORDER']['MID']= ['{{XYL}}{MKUP}{VL}{{RESET}}','{{XYR}}{MKUP}{VL}{{RESET}}',]
		s.tpl['BORDER']['BOT']='{{XY}}{MKUP}{LBC}'+'{HL}'*(s.size.x-2)+'{RBC}{{RESET}}'
		s.tpl['BUFFER']={}
		s.tpl['BORDERS']={}
		s.tpl['BORDERS'][1] = s.tpl['BORDER']['TOP'].format(**s.symbolset._asdict(),MKUP='{BG}{FG}')
		s.tpl['BORDERS'][2] = s.tpl['BORDER']['MID'][0].format(**s.symbolset._asdict(), MKUP='{BG}{FG}')
		s.tpl['BORDERS'][3] = s.tpl['BORDER']['MID'][1].format(**s.symbolset._asdict(), MKUP='{BG}{FG}')
		s.tpl['BORDERS'][4] = s.tpl['BORDER']['BOT'].format(**s.symbolset._asdict(),MKUP='{BG}{FG}')
		s.tpl['CLEAR']={}
		s.tpl['CLEAR'][1] = s.tpl['BORDER']['TOP'].format(**s.clearset._asdict(),MKUP='{BG}{FG}')
		s.tpl['CLEAR'][2] = s.tpl['BORDER']['MID'][0].format(**s.clearset._asdict(),MKUP='{BG}{FG}')
		s.tpl['CLEAR'][3] = s.tpl['BORDER']['MID'][1].format(**s.clearset._asdict(),MKUP='{BG}{FG}')
		s.tpl['CLEAR'][4] = s.tpl['BORDER']['BOT'].format(**s.clearset._asdict(),MKUP='{BG}{FG}')
		s.opts = {}
		s.opts['MKUP']={}
		s.opts['MKUP']['ACTIVE']={}
		s.opts['MKUP']['ACTIVE']['BG']= ''
		s.opts['MKUP']['ACTIVE']['FG']= ''
		s.opts['MKUP']['ACTIVE']['RESET']='\x1b[m'
		s.opts['MKUP']['ACTIVE']['UNSET']= Ansi.UNSET
		s.opts['MKUP']['DEFAULT']={}
		s.opts['MKUP']['DEFAULT']['BG']= ''
		s.opts['MKUP']['DEFAULT']['FG']= ''
		s.opts['MKUP']['DEFAULT']['RESET']='\x1b[m'
		s.opts['MKUP']['DEFAULT']['UNSET']= Ansi.UNSET
		s.opts['MKUP']['FOCUS']={}
		s.opts['MKUP']['FOCUS']['BG']= ''
		s.opts['MKUP']['FOCUS']['FG']= '\x1b[32m'
		s.opts['MKUP']['FOCUS']['RESET']='\x1b[m'
		s.opts['MKUP']['FOCUS']['UNSET']= Ansi.UNSET
		# s.initspace()
	@property
	def location(s):
		return s._location
	@location.setter
	def location(s,value):
		if not isinstance(value,Coord):
			value=Coord(value)
		s._location=value
	@property
	def size(s):
		if s._size is None:
			s._size=s.term.size.xy
		if s._size.y < 3:
			s._size =  Coord(s._size.x,3)
		return s._size
	@size.setter
	def size(s,value):
		s._size=value
		for disp in s.displays:
			s.displays[disp].size=s._size+Coord(-2,-2)
		if s._state!=0:
			s.makeFrame()
	def _makeFrame(s):
		opts=s.opts['MKUP']['ACTIVE']
		locx=s.location.x
		locy=s.location.y
		s.lst['border'][1] =s.tpl['BORDERS'][1].format(XY=s.location,**opts)
		s.lst['wipe'][1] = s.tpl['CLEAR'][1].format(XY=s.location, **opts)
		j=0
		for i in range(2,s.size.y-1):
			s.lst['border'][i]=(s.tpl['BORDERS'][2].format(XYL=s.location+Coord(0,i-1),**opts)+
							  s.tpl['BORDERS'][3].format(XYR=s.location+Coord(s.size.x-1,i-1),**opts))
			s.lst['wipe'][i]=( s.tpl['CLEAR'][2].format(XYL=s.location+Coord(0,i-1), **opts)+
							' '*(s.size.x-2)+
							 s.tpl['CLEAR'][3].format(XYR=s.location+Coord(s.size.x-1, i-1), **opts))
			j=i
		s.lst['border'][j+1] = s.tpl['BORDERS'][4].format(XY=s.location+Coord(0, j), **opts)
		s.lst['wipe'][j+1] = s.tpl['CLEAR'][4].format(XY=s.location+Coord(0, j), **opts)
		s.frame=''.join(s.lst['border'].values())
		s.str['clear']=''.join(s.lst['wipe'].values())
		s.str['frame']=''.join(s.lst['border'].values())
	def _drawFrame(s):
		print(s.str['frame'],end='',flush=True)
	def _clearFrame(s):
		print(s.str['clear'],end='',flush=True)
	def _wipeFrame(s):
		print(s.str['clear'],end='',flush=True)

	def _makeTitle(s):
		nosep=''
		if isinstance(s.name,str):
			noprefix=s.name.lstrip('frm')
			nosep=noprefix.lstrip('_')
		return nosep

	def focus(s,val=True):
		s._focus=val
		if s._focus:
			s.opts['MKUP']['ACTIVE']=s.opts['MKUP']['FOCUS']
		else:
			s.opts['MKUP']['ACTIVE']=s.opts['MKUP']['DEFAULT']
		s._state=1
		s.draw()
	def show(s,val=True):
		s._hidden=not val
		for disp in s.displays:
			s.displays[disp].show(val)
		s._state=2
		s.draw()
	def draw(s):
		if s._state==0:
			s._makeFrame()
		elif s._state==1:
			s._clearFrame()
			s._makeFrame()
		elif s._state==2:
			s._wipeFrame()
			s._makeFrame()
		if not s._hidden:
			for disp in s.displays:
				s.displays[disp].flag['redraw']=True
				s.displays[disp].draw()
			s._drawFrame()
			s._state=3


	def addDisplay(s,name,disp,select=True):
		did=len(s.displays)+1
		s.displays[did]=disp(ctx=s.ctx,parent=s,name=name)
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

	def move(s,location):
		s._state=2
		s.location=s.location+location
		s.draw()

	def h_resize(s,val):
		s._state=2
		s.size=Coord(s.size.x+val,s.size.y)
		s.draw()

	def v_resize(s,val):
		s._state=2
		s.size = Coord(s.size.x, s.size.y + val)
		s.draw()

class FrameSet:

	def newFrame(s,term=None,name=None,location=Coord(1,1),size=Coord(80,5),display=None,linenrs=True,border=True):
		framename='frm_'+name.lstrip('frm_')
		s.__setattr__(framename,Frame())

