#!/usr/bin/env python
from libTerm import Coord
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
	@property
	def stop(s):
		return s._stop
	def __call__(s):
		return list(range(s.start,s.stop))






class LineDisplay:
	"""
	a line display that is framed of in size , and can be used to
	print lines to. it fills the linebuffer untill full and then
	starts autoscrolling new prints. it allows for scrolling back up
	and down, by default lines are not wrapped but cropped , the cropped
	charakters can be accessed in scroll mode by moving the viewport right

	"""
	def __init__(s,term,location=Coord(1,1),size=Coord(80,24)):
		s.term=term
		s.loc=location
		s.size=size
		s.wrap=False
		s.wrapsym='《》⟪⟫«‹›…»…'
		s._scroll=False
		s.v_viewrng=ViewRange(0,size.y)
		s.h_viewrng=ViewRange(0,size.x)
		s.data_lines={}
		s.data_idx=0
		s.print_lines={}
		s.tpl={}
		s.tpl['LINE']='{XY}{BG}{FG}{{SEL}}{MKUP}{{LINE}}{RESET}'


		s.m=0

	def print(s,line):
		"""
		Prints/Appends a line to the display
		:param line: the string/line to append
		:return:
		"""
		s.addline(line.rstrip('\n'))
		s.update()

	@property
	def linebuffer(s):
		buffer=[line for line in s.lines]
	def render(s):
		"""
		prints the buffer to stdout
		:return:
		"""

	def vscroll(s,val):
		"""
		adjusts the viewrange by val. resulting in the display "scrolling" up or down
		blocks the dispaly from autoscrolling on new input
		if the viewrange end is equal to the total linecount , or val is 0 ,
		autoscroll starts again.


		:flags _vscroll: if the display is in scroll modus or not


		:param val:
		:return:
		"""

		if not s._vscroll:
			last=len(s.data)
			first=last-s.size.y
			s.viewrange=(first,last)
			s._scroll=True
		first,last=s.viewrange
		first+=val
		last+=val
		s.viewrange=(first,last)
		for line, tpl in zip(s.data[first:last], s.tpl_lines):
			print(tpl.format(LINE=s.crop(line)), end='', flush=True)

	def lineformat(s):
		reset='\x1b[m'
		xy=f'\x1b[{{Y}};{s.loc.x}H'
		return s.tpl['line'].format(XY=xy,RESET=reset,FG=s.mkup['FG'],BG=s.mkup['BG'],MKUP=s.mkup['MKUP'])


	def crop(s,line):
		def cropped():
			start,stop = s.h_viewrng()
			suffix='\x1b[38;2;64;192;64m …\x1b[m' if len(line)>s.h_viewrng.size else False
			l=line.ljust(s.h_viewrng.size).rjust(s.h_viewrng.size)[start:stop]
			if suffix:
				l=l[:-2]+suffix
			return l
		return cropped

	def addline(s,line):
		s.data_lines[s.data_idx]=line
		s.data_idx+=1
		if s.data_idx>s.size.y:


	def update(s):
		for nr,idx in zip(range(0,s.size.y),s.viewrange()):
			s.print_lines[nr]=s.format(s.data_lines[idx])


	async def readbuffer(s):
		for line in [*s.buffer]:
			line=s.buffer.pop(0)
			s.append(line)
			s.sink+=[line]

	async def watch(s):
		while True:
			await s.notify.wait()
			s.notify.clear()
			s.loop.create_task(s.readbuffer())

	async def start(s):
		s.ctx.loop = asyncio.get_running_loop()
		s.ctx.loop.create_task(s.watch())
