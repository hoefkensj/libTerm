# /usr/bin/env pyhthon
from libTerm import Term,Color,Coord,Mode,Selector
import time

class Menu:
	def __init__(s,term,items,xy=None,coord=None):
		s._tplxy='\x1b[{Y};{X}H'
		s._tplit='{XY}{COLR}{NO}. {ITEM}{DESEL}'
		s._colr='\x1b[{SEL}38;2;192;192;192m'
		s._items=items
		s.term=term
		s.xy=xy or s.term.cursor.xy
		s.selector=Selector(len(s._items),start=1)
		s.selected=s.selector.read
		s.current=None
		s.items=[]
		s.menu=['MENU']
		s.changed=[]
		s.it_width = lambda: max([len(n) for n in s._items]) + 2
		s.nr_width = lambda: len(str(len(s._items)))
		s.__itemlist__()
		s.build()

	def __len__(s):
		return len(s.items)

	def __itemlist__(s):
		for i,arg in enumerate(s._items,start=1):

			XY = s._tplxy.format(Y=s.xy.y + i, X=s.xy.x)
			s.items+=[s._tplit.format(DESEL='\x1b[27m',COLR=s._colr,XY=XY,NO=str(i).rjust(s.nr_width()),ITEM=arg.ljust(s.it_width()))]

	def build(s):
		for i,item in enumerate(s.items,start=1):
			if  i == s.selected() :
				sel='7;'
				s.current=item.format(SEL='0;')
				listitem=item.format(SEL=sel)
			else:
				listitem = item.format(SEL='0;')

			s.menu+=[listitem]

	def next(s):
		cur=s.selected()
		s.selector.next()
		s.changed=[s.current.format(SEL='0;')]
		s.changed += [s.items[cur].format(SEL='7;')]
		s.current=s.items[cur]
		return s.update()

	def prev(s):
		s.selector.prev()
		cur=s.selected()
		s.changed=[s.current.format(SEL='0;')]
		s.changed += [s.items[cur].format(SEL='7;')]
		s.current=s.items[cur]
		return s.update()

	def update(s):
		return lambda :print(''.join(s.changed),end='',flush=True)
	def __str__(s):
		return ''.join(s.menu[1:]).format(SEL='')

term=Term()
term.buffer.switch()
term.mode=Mode.CONTROL
items=['aaaa','bbbbbb','cccccccccc','dd']
M=Menu(term,items ,xy=Coord(10,10))
print(M)
while True:
	if M.term.stdin.event:
		key=M.term.stdin.read()
		if key=='\x1b[B':
			update=M.next()
		elif key=='\x1b[A':
			update=M.prev()
		elif key=='q':
			break
		else:
			continue
		update()
	time.sleep(0.01)