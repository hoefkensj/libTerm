#!/usr/bin/env python
# !/usr/bin/env python
from select import select
import os,sys
class Stdin():
	def __init__(s,**k):
		# super().__init__()
		s.term = k.get('term')
		s.fd=s.term.stdfd[0]
		s._buffer = []
		s._event = True
		s._count = 0

	@property
	def event(s):
		s._event = select([s.fd], [], [], 0)[0] != []
		return s._event


	@property
	def count(s):
		return s._count

	def read(s):
		s.sync()
		ret = ''.join([i.decode('UTF-8') for i in s._buffer])
		s.flush()
		return ret
	def readraw(s,bits=8):
		raw=os.read(s.fd, bits)
		return raw
	def sync(s):
		while select([s.fd], [], [], 0)[0]:
			s._buffer += [os.read(s.fd, 8)]
			s._count += 1
		return s._count

	def getbuffer(s):
		return s._buffer

	def getch(s):
		c=''
		if len(s._buffer) != 0:
			c = s._buffer.pop(-1)
		return c

	def flush(s):
		s._buffer = []

	def query(s,ansi):
		print(ansi,end='',flush=True)
		parser=ansi.parser(s)
		s.term.attr.setcbreak()
		try:
			sys.stdout.write(ansi)
			sys.stdout.flush()
			result = parser()

		finally:
			s.term.attr.set(s.term.attr.restore())
		return result



