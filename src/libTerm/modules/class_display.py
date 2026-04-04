#!/usr/bin/env python
from libTerm import Coord,Color,ColorSet,ColorPalette
from libTerm import Term
from libTerm.components import enums

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

markup=Markup('display')
markup.line=Markup('line')
markup.line.default=Markup('default')
markup.line.default.colors=ColorSet(fg=Color(160,160,160),bg=Color(16,16,16))
markup.line.default.mkup=''
markup.line.selected=Markup('selected')
markup.line.selected.colors=ColorSet(fg=Color(255,255,255),bg=Color(64,192,64))
markup.line.selected.mkup='\x1b[7m'
markup.lnr=Markup('lnr')
markup.lnr.default=Markup('default')
markup.lnr.default.colors=ColorSet(fg=Color(128,128,128),bg=Color(64,64,64))
markup.lnr.default.mkup=''
markup.lnr.selected=Markup('selected')
markup.lnr.selected.colors=ColorSet(fg=Color(255,255,255),bg=Color(64,192,64))
markup.lnr.selected.mkup=''



class LineDisplay:
	"""
	a line display that is framed of in size , and can be used to
	print lines to. it fills the linebuffer untill full and then
	starts autoscrolling new prints. it allows for scrolling back up
	and down, by default lines are not wrapped but cropped , the cropped
	charakters can be accessed in scroll mode by moving the viewport right

	"""
	def __init__(s,term,location=Coord(1,1),size=Coord(80,5),linenrs=True):
		s.term=term
		s._loc=location
		s._scroll=False
		s._shift=False
		s._size=size

		s.linenrs=linenrs
		s.wrapsyms='⟪«‹… …›»⟫'
		s.overflow=False
		s.wrap=False
		s.v_viewrng=ViewRange(1,s.size.y)
		s.h_viewrng=ViewRange(1,s.size.x)
		s.data_lines={}

		s.data_idx=0
		s.print_buffer={}
		s.mkup=markup

		s.tpl={}
		s.tpl['LINE']='{XY}{{LNR}}{BG}{FG}{{SEL}}{MKUP} {{LINE}}{UNSET}'
		s.tpl['LNR']='{BG}{FG}{{SEL}}{MKUP}{{NR}}{UNSET}'
		s.tpl['BUFFER']={}
		s.make_linebuffer()

	@property
	def location(s):
		return s._loc

	@property
	def loc(s):
		return s._loc

	@location.setter
	def location(s,val):
		s._loc=val
		s.make_linebuffer()
		s.initspace()
	@property
	def size(s):
		return s._size

	@size.setter
	def size(s,val):
		s._size=val
		s.make_linebuffer()
		s.initspace()

	def printrng(s,xy):
		x={}
		y={}
		x['start']=s.loc.x
		y['start']=s.loc.y
		x['stop']=s.loc.x+s.size.x
		y['stop']=s.loc.y+s.size.y
		XY={'x':x,'y':y}

		return XY.get(xy)

	def print(s,line):
		"""
		Prints/Appends a line to the display
		:param line: the string/line to append
		:return:
		"""
		s.addline(line.rstrip("\n"))
		s.update()
		s.render()

	def initspace(s):
		# s.printrng('y')
		for l in range(1,s.size.y+1):
			line = s.tpl['BUFFER'][l]
			wipe = ' ' * (s.size.x-3)
			gutter=s.tpl['LNR'].format(
				SEL='',
				NR='   ',
				UNSET='\x1b[29m',
				FG=s.mkup.lnr.default.colors.fg.ansifg,
				BG=s.mkup.lnr.default.colors.bg.ansibg,
				MKUP=s.mkup.lnr.default.mkup).format(SEL='', NR='    ')
			print(line['LINE'].format(SEL='',LINE=wipe,LNR=gutter))


	def make_linebuffer(s):
		xy = f'\x1b[{{Y}};{s.loc.x}H'
		reset='\x1b[m'
		rng=s.printrng('y')
		vp=range(rng['start'],rng['stop'])
		for l,line in enumerate(vp,start=1):
			bg=s.mkup.line.default.colors.bg+Color(l,l*2,l*3)
			linefmt=s.tpl['LINE'].format(
				XY=xy.format(Y=line),
				UNSET=reset,
				FG=s.mkup.line.default.colors.fg.ansifg,
				BG=bg.ansibg,
				MKUP=s.mkup.line.default.mkup)
			lnrfmt=s.tpl['LNR'].format(
				UNSET=reset,
				FG=s.mkup.lnr.default.colors.fg.ansifg,
				BG=s.mkup.lnr.default.colors.bg.ansibg,
				MKUP=s.mkup.lnr.default.mkup
			)
			s.tpl['BUFFER'][l]={}
			s.tpl['BUFFER'][l]['LNR']=lnrfmt
			s.tpl['BUFFER'][l]['LINE']=linefmt

	def update(s):
		lnr=''
		adjust=0
		if not s.overflow:
			for l,idx in enumerate(s.data_lines,start=1):
				tpls=s.tpl['BUFFER'][l]
				line=s.data_lines[idx]
				if s.linenrs:
					nr=f'{idx}. '.rjust(4)
					lnr=tpls['LNR'].format(SEL='',NR=nr)
					adjust=-4
				if not s.wrap:
					line=line['crop'](adjust=adjust)
				s.print_buffer[l]=tpls['LINE'].format(SEL='',LINE=line,LNR=lnr)

		else:
			for l in range(1,s.size.y+1):
				tpls=s.tpl['BUFFER'][l]
				offset=s.v_viewrng.start+l
				line=s.data_lines[offset]
				if s.linenrs:
					nr = f'{offset}. '.rjust(4)
					lnr = tpls['LNR'].format(SEL='', NR=nr)
					adjust = -4
				if not s.wrap:
					line=line['crop'](adjust=adjust)

				s.print_buffer[l]=tpls['LINE'].format(SEL='',LINE=line,LNR=lnr)

	def render(s):
		"""
		prints the buffer to stdout
		:return:
		"""
		for idx in s.print_buffer:
			print(s.print_buffer[idx])

	def crop(s,line):
		def cropped(adjust=0):
			start  =s.h_viewrng.start
			stop   =s.h_viewrng.stop+adjust
			suffix ='\x1b[38;2;64;192;64m…\x1b[39m' if len(line)>(s.h_viewrng.size+adjust)else False
			l      =line.ljust(s.h_viewrng.size).rjust(s.h_viewrng.size)[start:stop]
			crop=line.ljust(s.h_viewrng.size).rjust(s.h_viewrng.size)[stop:]
			if crop.strip(' ')=='':
				suffix=' '
			if start > 1:
				prefix=' \x1b[38;2;64;192;64m…\x1b[39m'
				l=prefix+l[1:]

			if suffix:
				l=l[:-2]+suffix

			return l
		return cropped

	def addline(s,line):
		s.data_idx+=1
		s.data_lines[s.data_idx]={'data':line,'crop':s.crop(line)}
		if not s._scroll:
			s.v_viewrng.stop=s.data_idx
			print('\x1b[2;1H',s.data_idx,s.v_viewrng)
		if s.data_idx > s.size.y:
			s.overflow=True

	def scroll(s, val):
		v=val
		if not s._scroll:
			s._scroll = True
		if s._scroll:
			if s.v_viewrng.stop+1 == s.data_idx:
				s._scroll = False
			elif s.v_viewrng.start == 1:
				v=0
			elif val ==0:
				s._scroll= False
		s.v_viewrng.shift(v)
		s.update()
		s.render()

	def shift(s,val):
		if not s._shift:
			s._shift = True
		s.h_viewrng.shift(val)
		s.update()
		s.render()



