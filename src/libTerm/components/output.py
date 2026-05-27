#!/usr/bin/env python
import os,sys
class Output:
	def __init__(s,**k):
		# super().__init__()
		s.term = k.get('term')
		s.tty = k.get('tty')
		s.std=sys.stdout

	def fileno(s):
		return sys.stdout.fileno()
	@property
	def fd(s):
		return sys.stdout.fileno()

	@property
	def isatty(s):
		return os.isatty(s.fd)

	def write(s, data):
		if isinstance(data, str):
			data = data.encode('UTF-8')
		s.std.write(data.decode('UTF-8'))
	def flush(s):
		s.std.flush()


