#!/usr/bin/env python
import sys

def LOCparser(stdin):
	def parser():
		buf = ' '
		while buf[-1] != "R" and len(buf) <=32:
			buf += stdin.readraw().decode('UTF-8')
		return buf
	return parser





