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
	print('parsing')

	def parser():
		import asyncio
		def readstdin():
			nonlocal buf
			nonlocal loop
			buf += stdin.readraw()
			if len(buf)==23:
				loop.remove_reader(stdin.fd)
				loop.stop()
		print('parsingpp')
		buf = ''
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.add_reader(stdin.fd, readstdin)
		rgb = buf.split(':')[1].split('/')
		rgb = [int(i, base=16) for i in rgb]
		# rgb = TermColors.COLOR(*rgb, 16)
		return rgb
	return parser



	loop.run_forever()