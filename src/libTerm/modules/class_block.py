#!/usr/bin/env python
from libTerm import Term
from libTerm import Coord,Color,Buffer
from libTerm.modules.class_display import LineDisplay

class Bar:
	def __init__(s,ctx=None,parent=None,text='',location=None,width=None,fgcolor=Color(0,0,0),bgcolor=Color(32,128,128),allign='center'):
		s.ctx=ctx
		s.parent=parent
		s.tpl='\x1b[{X1OFF}G\x1b[{FOC};48;2;{BGC}m\x1b[K{TEXT}\x1b[{X2OFF}G\x1b[m\x1b[K'
		s.loc=location+Coord(1,1) if location is not None else parent.loc+Coord(1,0)
		s.width=width-2
		s.fgcolor=fgcolor
		s.bgcolor=bgcolor
		s._allign='center'
		s.focus=s.parent.focus
		s.ftext=''
		s.utext=''
		s.fbg=''
		s.ubg=''
		s.textstring=text
		s.settext(markup='1')
		s.bg()



	def textallign(s,allign='center'):
		center = s.width // 2
		allign = center - ((len(s.textstring) ) // 2)
		start = s.loc.x + allign
		return start
	def settext(s,string=None,markup=''):
		start=s.textallign()
		s.ftext = f'\x1b[{start}G\x1b[1;38;2;{s.fgcolor.ansi()}m{s.textstring}'
		s.utext = f'\x1b[{start}G\x1b[2;38;2;{s.fgcolor.ansi()}m{s.textstring}'
	def bg(s):
		s.fbg=s.tpl.format(FOC='1', BGC=s.bgcolor.ansi(), X1OFF=s.loc.x, X2OFF=s.loc.x + s.width, TEXT=s.ftext)
		s.ubg=s.tpl.format(FOC='1;2', BGC=s.bgcolor.ansi(), X1OFF=s.loc.x, X2OFF=s.loc.x + s.width, TEXT=s.utext)
	def __str__(s):
		if s.focus:
			bg=f'\x1b[{s.loc.y};{s.loc.x}H'+s.fbg
		else:

			bg=f'\x1b[{s.loc.y};{s.loc.x}H'+s.ubg
		return bg


class Block:
	"""
	a line display that is framed of in size , and can be used to
	print lines to. it fills the linebuffer untill full and then
	starts autoscrolling new prints. it allows for scrolling back up
	and down, by default lines are not wrapped but cropped , the cropped
	charakters can be accessed in scroll mode by moving the viewport right

	"""
	def __init__(s,term,name,location=Coord(1,1),size=Coord(180,15),display=LineDisplay,border=True):
		s.term=term
		s.name=name
		s.loc=location
		s.size=size
		s.border=border
		s.focus=True
		s.boxsyms=' ─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱'
		s.lines={}
		s.displaytype=display
		s.display=None
		s.tpl={}
		s.tpl['LINE']='{XY}{BG}{FG}{L}{UNSET}{BG}{FG}{C}{UNSET}{BG}{FG}{R}{RESET}'
		s.tpl['BUFFER']={}
		# s.initspace()
		s.make_Box()



	def make_Box(s):

		if s.border:

			LCR={'L':s.boxsyms[13],'C':s.boxsyms[1]*(s.size.x),'R':s.boxsyms[17]}
			U='\x1b[39m'
			s.lines[1]=s.tpl['LINE'].format(XY=Coord(s.loc.x,s.loc.y),BG='',FG='',**LCR,RESET='',UNSET=U)

			for i in range(1,s.size.y-1):
				LCR = {'L': s.boxsyms[3], 'C': s.boxsyms[0] * (s.size.x), 'R': s.boxsyms[3]}
				s.lines[1+i]=s.tpl['LINE'].format(XY=Coord(s.loc.x,s.loc.y+i),BG='',FG='',**LCR,RESET='',UNSET=U)
			LCR = {'L': s.boxsyms[21], 'C': s.boxsyms[1] * (s.size.x ), 'R': s.boxsyms[25]}
			s.lines[i+2]=s.tpl['LINE'].format(XY=Coord(s.loc.x,s.loc.y+s.size.y-1),BG='',FG='',**LCR,RESET='',UNSET=U)

	def draw(s):
		print(''.join(s.lines.values()), end='', flush=True)


