#!/usr/bin/env python
from libTerm import Term
from libTerm import Coord,Color,Buffer,Ansi
from libTerm.modules.class_display import LineDisplay


class Frame:
	"""
	a line display that is framed of in size , and can be used to
	print lines to. it fills the linebuffer untill full and then
	starts autoscrolling new prints. it allows for scrolling back up
	and down, by default lines are not wrapped but cropped , the cropped
	charakters can be accessed in scroll mode by moving the viewport right

	"""
	def __init__(s,term=None,name=None,location=Coord(1,1),size=Coord(80,5),display=None,linenrs=True,border=True):
		s.term=term
		s.name=name
		s.title=name.lstrip('frm_')
		s.subtitle=''
		s._loc=location
		s._size=size
		s.border=border
		s.linenrs=linenrs
		s._focus=False
		s._hidden=False
		s.boxsyms=' ─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕ ▖▗▘▙▚▛▜▝▞▟■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱'
		s.lines={}
		s._clear=''
		s.display=None
		s.displays={}
		s.tpl={}
		s.tpl['LINE']='{XY}{BG}{FG}{L}{UNSET}{BG}{FG}{C}{UNSET}{BG}{FG}{R}{RESET}'
		s.tpl['BUFFER']={}
		# s.initspace()
		s.TLCR={'L':s.boxsyms[110],'C':s.boxsyms[17]+s.title+s.boxsyms[13]+s.boxsyms[1]*(s.size.x-2-len(s.title)),'R':s.boxsyms[111]}
		s.CLCR = {'L': s.boxsyms[3], 'C': s.boxsyms[0] * (s.size.x), 'R': s.boxsyms[3]}
		s.BLCR = {'L': s.boxsyms[113], 'C': s.boxsyms[1] * (s.size.x ), 'R': s.boxsyms[112]}
		s.LCR=[s.TLCR,s.CLCR,s.BLCR]


	def focus(s,val=None):
		if val is None:
			val=not s._focus
		s._focus=val
		s.redraw()

	def show(s,val=None):
		if val is None:
			val=not s._hidden
		else:
			val=not val
		s._hidden=val
		s.draw()

	def makeFrame(s,LCR=None):
		def makeClear():
			TLCR={'T':' ','L':' ','C':' '*(s.size.x),'R':' ',}
			CLCR={'T':' ','L':' ','C':' '*(s.size.x),'R':' ',}
			BLCR={'T':' ','L':' ','C':' '*(s.size.x),'R':' ',}
			opts = {'BG': '', 'FG': '', 'RESET': '\x1b[m', 'UNSET': Ansi.UNSET}
			s._clear =s.tpl['LINE'].format(XY=Coord(s.location.x,s.location.y),**TLCR,**opts)
			for i in range(1,s.size.y-1):
				s._clear+=s.tpl['LINE'].format(XY=Coord(s.location.x,s.location.y+i),**CLCR,**opts)
			s._clear+=s.tpl['LINE'].format(XY=Coord(s.location.x,s.location.y+s.size.y-1),**BLCR,**opts)


		makeClear()

		TLCR=s.LCR[0]
		CLCR=s.LCR[1]
		BLCR=s.LCR[2]
		opts = {'BG': '', 'FG': '', 'RESET': '\x1b[m', 'UNSET': Ansi.UNSET}
		if s.border:
			# tpl='{XY}{BG}{FG}{BOX}{RESET}'

			if s._focus:
				opts['FG']='\x1b[1m'
			else:
				opts['BG']=''


			s.lines[1] =s.tpl['LINE'].format(XY=Coord(s.location.x,s.location.y),**TLCR,**opts)
			for i in range(1,s.size.y-1):
				s.lines[1+i]=s.tpl['LINE'].format(XY=Coord(s.location.x,s.location.y+i),**CLCR,**opts)
			s.lines[s.size.y+1] = s.tpl['LINE'].format(XY=Coord(s.location.x, s.location.y + s.size.y - 1), **BLCR, **opts)

	@property
	def location(s):
		return s._loc
	@location.setter
	def location(s,value):
		s._loc=value
		for disp in s.displays:
			s.displays[disp].location=s._loc+Coord(2,2)
	@property
	def size(s):
		return s._size

	@size.setter
	def size(s,value):
		s._size=value
		for disp in s.displays:
			s.displays[disp].size=s._size+Coord(2,2)

	def draw(s):
		s.makeFrame(LCR=s.LCR)
		if not s._hidden:
			print(''.join(s.lines.values()), end='', flush=True)
			for disp in s.displays:
				s.displays[disp].draw()

	def redraw(s):
		if not s._hidden:
			s.clear()
			s.makeFrame()
			s.draw()


	def addDisplay(s,name,disp):
		did=len(s.displays)+1
		s.displays[did]=disp(s.term,name,location=s.location+Coord(2,2),size=s.size+Coord(-2,-2))
		return did

	def selectDisplay(s,n=1):
		s.display=s.displays.get(n)
		s.display.show(True)
		s.display.draw()

	def addMenu(s,menu,**opts):
		# fg = Color(0, 196, 196)
		# mycolors = ColorSet(fg=fg)
		s.display=menu(s.term, location=s.location+Coord(2,2), **opts)
		s.display.draw()
		s.displays[1]=s.display

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

