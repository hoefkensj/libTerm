#!/usr/bin/env python
from libTerm.examples import ex_basic,ex_arrowkeys,ex_printkeys,ex_colors,ex_menu_list_simple,ex_menu_grid_simple,ex_menu_grid_big,ex_snake_automatic,ex_snake_manual
import time
modules = [
		ex_arrowkeys,
		ex_basic,
		ex_menu_grid_big,
		ex_menu_grid_simple,
		ex_menu_list_simple,
		ex_colors,
		ex_printkeys,
		ex_snake_automatic,
		ex_snake_manual,
	]
# class Examples:
# 	def __init__(s):
# 		s.ex=[]
#
#
# 	def getexamples(s):
# 		from libTerm import examples as ex
# 		s.ex=[module for module in ex]
#
#
# 	async def keyscan(term):
# 		import asyncio
# 		loop=asyncio.get_running_loop()
# 		event = term.stdin.sync
# 		print('press n for next example')
# 		while True:
# 			await asyncio.wait_for(event)
# 			key = term.stdin.read()
# 			if key in 'NnPpQa':

def runExamples(term):
	for module in modules:
		print(module.__name__)
		time.sleep(1)
		term.Ansi.cls()
		time.sleep(1)
		print(f"Running example: {module.__name__}")
		time.sleep(1)
		module.main(term)

def main():
	import atexit
	from libTerm import Term
	def ExitProcedure(t):
		t.Ansi.cls()
		t.mode = t.MODE.DEFAULT
		t.buffer = t.BUFFER.DEFAULT
	t=Term()
	t.mode=t.MODE.CONTROL
	t.buffer = t.BUFFER.ALTERNATE
	t.Ansi.cls()
	atexit.register(ExitProcedure,t)