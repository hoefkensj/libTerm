#!/usr/bin/env python
def LOCparser(term):
	def parser():
		buf = ' '
		while buf[-1] != "R" and len(buf) <=32:
			buf += term.stdin.readraw().decode('UTF-8')
		return buf
	return parser