# /usr/bin/env python


class Selector:
	"""Cyclic Selector,configurable range and step-size
		note: a range of (1,10) includes both 1 and 10:
		10 <- 1 2 3 4 5 6 7 8 9 10 ->1
	"""
	def __init__(s, range,dn=-1,up=1,start=0):
		s.step={}
		s.step['dn']= None
		s.step['up']= None
		s._shift = 0
		s._range = 0
		if isinstance(range,float|int):
			range=(0,range)
		s.setrange(range)
		s.setstep(dn,up)
		s._up=s._wrapper(s.step['up'])
		s._dn=s._wrapper(s.step['dn'])
		s._wr=s._wrapper(0)
		s._value = s._wr(start)

	def _update_wrappers(s):
		s._up=s._wrapper(s.step['up'])
		s._dn=s._wrapper(s.step['dn'])
		s._wr=s._wrapper(0)

	def _wrapper(s,i):
		def wrap(v):
			return ~(~(v + i) * -~-s._range) % s._range
		return wrap
	@property
	def range(s):
		o=s._shift
		r=s._range
		rng=map(lambda n:n+o,r)
		return tuple(rng)

	def setrange(s,span):
		bot,top=span
		top+=1
		s._range=top-bot
		s._shift=bot
		s._update_wrappers()

	def setstep(s,dn=None,up=None):
		if dn is None and s.step['dn'] is None:
			s.step['dn']=-1
		else:
			s.step['dn']=dn or s.step['dn']
		if up is None and s.step['up'] is None:
			s.step['up']=1
		else:
			s.step['up']=up or s.step['up']
		s._update_wrappers()
	def expand(s,size=1):
		if size>=0:
			s._range+=size
		else:
			s._shift+=size
		s._update_wrappers()

	def contract(s,size=1):
		if size>=0:
			s._range-=size
		else:
			s._shift-=size
		s._update_wrappers()

	def next(s):
		s._value = s._up(s._value)
		return s._value+s._shift

	def prev(s):
		s._value = s._dn(s._value)
		return s._value+s._shift

	def read(s):
		return s._value+s._shift
	def write(s, val):
		s._value=s._wr(val-s._shift)
		return s._value+s._shift




if __name__ == '__main__':
	S=Selector((1,20),dn=-5,up=+5,start=-5)
	print(S.read())
	for i in range(30):
		print(S.next())
	S.setstep(-1, 1)
	for i in range(30):
		print(S.next())
	print(S.write(20))
	print(S.read())
	S.expand(15)
	print(S.read())
	for i in range(30):
		print(S.next())
	print('21',S.next())
	print(S.next())
	print(S.next())
	print(S.next())
	print(S.next())
	print(S.next())



