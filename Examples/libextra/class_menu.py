# /usr/bin/env pyhthon
from libTerm import Selector
class Menu:
	def __init__(s,term,items,templates=None,xy=None,coord=None):
		s.term=term
		s._tpl=['\x1b[{Y};{X}H','{XY}{CONR}{NO}. {COIR}{ITEM}{DESEL}','\x1b[{SEL}38;2;64;128;255{MOD}m']
		s._items=items
		s.selector=Selector((1,len(s._items)),start=0)
		s.selector.select(1)
		s.selected=s.selector.getselection
		s.items=['MENU']
		s.menu=[]
		s.changed=[]
		s.updated=''
		s.init=False
		s.it_width = max([len(n) for n in s._items]) + 2
		s.nr_width = len(str(len(s._items)))
		s.build(xy)

	def __len__(s):
		return len(s.items)

	def build(s,xy):
		for i,arg in enumerate(s._items,start=1):
			XY = s._tpl[0].format(Y=xy.y + i, X=xy.x)
			s.items+=[s._tpl[1].format(
				DESEL='\x1b[27m',
				CONR=s._tpl[2],
				XY=XY,
				COIR=s._tpl[2],
				NO=str(i).rjust(s.nr_width),
				ITEM=arg.ljust(s.it_width))]

		for i,item in enumerate(s.items[1:],start=1):
			s.menu += [item.format(SEL='0;',MOD='')]
			if s.selected() == i:
				s.menu[-1]=item.format(SEL='7;',MOD='')


	def next(s):
		s.changed=[s.items[s.selected()].format(SEL='0;',MOD='')]
		s.selector.next
		s.changed+=[s.items[s.selected()].format(SEL='7;',MOD='')]
		return s.update()

	def prev(s):
		s.changed=[s.items[s.selected()].format(SEL='0;',MOD='')]
		s.selector.prev
		s.changed+=[s.items[s.selected()].format(SEL='7;',MOD='')]
		return s.update()

	def update(s):
		s.updated=''.join(s.changed)
		print(s.updated,end='',flush=True)

	def choose(s,markup='\x1b[7;0;32m'):
		s.changed = [s.items[s.selected()].format(SEL='0;3;4,5;',MOD=f'm{markup.rstrip("m")}')+'\x1b[m']
		s.update()
		return [s.selected(),s._items[s.selected()-1]]
	def draw(s):
		print(''.join(s.menu),end='',flush=True)

	def __str__(s):
		return ''.join(s.menu)+s.updated