#!/usr/bin/env python
import sys

def LOCparser(stdin):
	def parser():
		buf = ' '
		while buf[-1] != "R" and len(buf) <=32:
			buf += stdin.readraw().decode('UTF-8')
		return buf
	return parser





def COLparser(stdin):
	def parser():
		from libTerm import TermColors
		buf = ''
		try:
			for i in range(23):
				buf += sys.stdin.read(1)
			rgb = buf.split(':')[1].split('/')
			rgb = [int(i, base=16) for i in rgb]
			rgb = TermColors.COLOR(*rgb, 16)
		except Exception as E:
			# print(E)
			rgb = None
		return rgb