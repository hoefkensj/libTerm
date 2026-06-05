#!/usr/bin/env python
# !/usr/bin/env python
from select import select
import os,sys
import asyncio

class Input():
	def __init__(s,**k):
		# super().__init__()
		s.term = k.get('term')
		s.tty=k.get('tty')
		s.std=sys.stdin
		s._buffer = []
		s._last=''
		s._event = True
		s._count = 0
		s._notify_controls=None
		s.notify = asyncio.Event()
		s.loop = None

	def asyncstart(s):
		s.loop=s.term.loop
		s.loop.add_reader(s.fd,s._read)


	def fileno(s):
		return sys.stdin.fileno()
	@property
	def fd(s):
		return sys.stdin.fileno()

	@property
	def isatty(s):
		return os.isatty(s.fd)


	@property
	def event(s):
		s._event = select([s.fd], [], [], 0)[0] != []
		return s._event


	@property
	def count(s):
		return s._count


	def _read(s):

		ret = ''.join([str(i) for i in s._buffer])
		s._last+=ret

		s._notify_controls()
		return ret


	def read(s):
		s.sync()
		ret = ''.join([str(i) for i in s._buffer])
		s.flush()

		return ret

	def readraw(s,bits=8):
		raw=os.read(s.fd, bits)
		return raw

	def sync(s):
		while select([s.fd], [], [], 0)[0]:
			s._buffer += [os.read(s.fd, 8).decode('UTF-8')]
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
		s.term.attr.echo=False
		s.term.attr.setcbreak()
		s.term.modes.set(s.term.MODE.CONTROL)
		# s.term.tty.output.write(ansi)
		parser=ansi.parser(s)
		try:
			s.tty.output.write(ansi)
			s.tty.output.flush()
			result = parser()

		finally:
			s.term.attr.set(s.term.attr.restore())
		return result



