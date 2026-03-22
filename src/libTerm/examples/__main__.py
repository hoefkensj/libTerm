#!/usr/bin/env python
import importlib
import pkgutil
import time
from libTerm.term import Term

def discover_modules():
	"""Return a sorted list of example module names in the libTerm.examples package.
	Modules starting with an underscore are ignored.
	"""
	import libTerm.examples as examples_pkg
	names = []
	for finder, name, ispkg in pkgutil.iter_modules(examples_pkg.__path__):
		if name.startswith('_'):
			continue
		# skip package resources and obvious non-example names
		if name == 'test':
			continue
		names.append(name)
	names.sort()
	return names
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

def runExample(term):
	mods=[modname for modname in discover_modules()]
	current=0
	max=len(mods())
	def nextmod():
		nonlocal current
		current=(current+1)%max
		return current
	def run():
		mod=mods[nextmod()]
		term.ANSI.cls()
		time.sleep(1)
		print('\x1b[1;1H', mod)
		time.sleep(1)
		# import and run the module lazily so modules are only loaded when their turn comes
		try:
			module = importlib.import_module(f'libTerm.examples.{mod}')
			if hasattr(module, 'main'):
				term.ANSI.cls()
				module.main(term)
			else:
				print(f"module {mod} has no main(), skipping")
		except Exception as e:
			print(f"Error importing/running {mod}: {e}")
	def runnext():
		key=term.stdin.read()

		if key == '\n':
			run()

	return runnext

def Control(term):
	import asyncio
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.stdin.fd, runExample(term))
	loop.run_forever()

def main():
	import atexit
	def ExitProcedure(t):
		t.ANSI.cls()
		t.mode = t.MODE.NORMAL
		t.buffer = t.BUFFER.DEFAULT
	t=Term()
	t.mode=t.MODE.CONTROL
	t.buffer = t.BUFFER.ALTERNATE
	t.ANSI.cls()
	atexit.register(ExitProcedure,t)
	Control(t)

if __name__=='__main__':
	main()