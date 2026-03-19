#!/usr/bin/env python
from libTerm import Term,Coord,Color
class Bar:
	def __init__(s,ctx=None,parent=None,text='',location=None,width=None,fgcolor=Color(0,0,0),bgcolor=Color(32,128,128),allign='center'):
		s.ctx=ctx
		s.parent=parent
		s.tpl='\x1b[{X1OFF}G\x1b[{FOC};48;2;{BGC}m\x1b[K{TEXT}\x1b[{X2OFF}G\x1b[m\x1b[K'
		s.loc=location
		s.width=width
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


class Frame:
	def __init__(s,ctx,name,title=None,location=None, size=None):
		s.ctx   = ctx
		s.name  = f'frm_{name}'
		s.title = title
		s.loc   = location
		s.size  = size
		s.disp  = None
		s.focus = False
		s._border=None



	def draw(s):
		print(str(Bar(text=s.name,width=s.size.x,location=s.loc)), end='', flush=True)


	def makeDisplay(s):
		pass
from libTerm import Mode
from time import sleep

t=Term()
t.buffer.switch()
t.mode=Mode.control

f=Frame(ctx=None,name='test',location=Coord(5,5),size=Coord(80,15))
b=Bar(parent=f,text=f.name,location=f.loc,width=f.size.x,)
bb=Bar(parent=f,text='bottom',location=Coord(f.loc.x,f.loc.y+f.size.y),width=f.size.x,)
print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
print(b,bb,end='',flush=True)
sleep(5)