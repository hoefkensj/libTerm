#!/usr/bin/env python
# !/usr/bin/env python
from select import select
import os

import asyncio
import sys
import os

class Stdin():
	def __init__(s,**k):
		# super().__init__()
		s.isreal = os.isatty(0)
		s.term = k.get('term')
		s._buffer = []
		s._aevent = asyncio.Event()
		s._event = False
		s._count = 0
		s._loop = None
		s._task =None
		s._watching=False

	def _aloop(s):
		try:
			s._loop = asyncio.get_running_loop()
		except RuntimeError:
			s._loop = asyncio.new_event_loop()
			asyncio.set_event_loop(s._loop)


	@property
	def event(s):
		if not s._watching:
			event=s.watch()
		else:
			s._loop. s._aevent.wait()

		event=s._event
		if event:
			s._aevent.clear()
			s._event = False
			s._watching=False
		return event

	def check(s):
		if select([s.term.fd], [], [], 0)[0] != []:
			s._aevent.set()
			s._event=True
		return s.event

	def watch(s):
		def callback():
			s._aevent.set()
			s._event=True
			s._watching=False
		if s._loop is None:
			s._aloop()
		s._loop.add_reader(s.term.fd, callback)
		s._watching=True
		return s._aevent.is_set()

	@property
	def count(s):
		return s._count

	def raw(s):
		if select([s.term.fd], [], [], 0)[0]:
			return os.read(s.term.fd, 8)
		else :
			return b''

	def read(s):
		s.buffer()
		ret = ''.join([i.decode('UTF-8') for i in s._buffer])
		s.flush()
		return ret

	def buffer(s):
		while select([s.term.fd], [], [], 0)[0]:
			s._buffer += [os.read(s.term.fd, 8)]
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


	def query(s,ansi,parser):
		result='notatty'
		if s.isreal:
			s.term.setcbreak()
			try:
				sys.stdout.write(ansi)
				sys.stdout.flush()
				result = parser()
			finally:
				s.term.tcsetattr(s.term.attr.restore())
		return result

