#!/usr/bin/env python
import asyncio

from libTerm import Term


def head():
	return "\x1b[2J\x1b[1;1H\x1b[1;4mReading State,Properties and Data from the terminal :\x1b[m"
def section(ROOT,KEY,VAL,SUBS):
	ret=''
	if ROOT!='':
		ret+=f'\n\x1b[1m{ROOT}:\n\t{SUBS}:\x1b[m'
	ret+=f'\n\x1b[4m{KEY}\x1b[20G{VAL}\x1b[40GDescription\x1b[m'
	return ret

def makeprint(dct,mkup):
	toprint=[]
	for key in dct:
		line=[]
		col = 0
		for value in dct[key]:
			if not isinstance(dct[key][value], list):
				line += ['{C}{val}'.format(C=mkup[col], val=dct[key][value])]
			else:
				line += ['{C}{val}'.format(C=mkup[col], val=dct[key][value][0])]
				for line in dct[key][value][1:]:
					line += ['\n{C}{val}'.format(C=mkup[col], val=line)]
			col += 1
		toprint += [''.join(line)]
	return toprint
def LIBTERM(term):
	def Props(props):
		mkup=['\x1b[4G\x1b[36m','\x1b[20G\x1b[33m','\x1b[40G\x1b[37m']
		def propadd(props, prop, val, desc):
			props[len(props)] = {
				'prop': prop,
				'val': val,
				'desc': desc
			}
			return props

		props=propadd(props,*['.pid',f'{term.pid}','# Process ID of the current process.'])
		props=propadd(props,*['.ppid',f'{term.ppid}','# Process ID of the parent process.Usually the shell that started the program.'])
		props=propadd(props,*['.mode',f'\x1b[31mMode.\x1b[33m{term.MODE(term.mode).name}', '# The current mode of the terminal'])
		props=propadd(props,*['.buffer',f'\x1b[31mBuffer.\x1b[33m{term.buffers.buffer.name}', '# The current Buffer of the terminal'])
		# props=propadd(props,*['.echo',f'{term.echo}','# Whether the terminal is currently echoing input.'])
		# props=propadd(props,*['.canonical',f'{term.canonical}','# Whether the terminal is currently in canonical mode.'])
		return '\n'.join([section(ROOT='libTerm',KEY='Property',VAL='Value',SUBS	='.'.join(['','Term()'])),*makeprint(props,mkup)])

	def Comp(comps):
		def compadd(comps, comp, cls, desc):
			comps[len(comps)] = {
				'comp': comp,
				'class': cls,
				'desc': desc}
			return comps

		comps = {}
		# comps = compadd(comps, *['.pts',f'{term.pts.__class__.__name__}','# The Terminal device.'])
		# comps = compadd(comps, *['.stdin', f'{term.stdin.__class__.__name__}', '# (class) Representing The terminal standard input, which can be used to read input events from the terminal.'])
		# comps = compadd(comps, *['.stdout',f'{term.stdout.__class__.__name__}','# (class) Representing The terminal standard output of the terminal'])
		comps = compadd(comps, *['.attr', f'{term.attr.__class__.__name__}', '# Representing The terminal attributes, which can be used to get and set various terminal settings.'])
		comps = compadd(comps, *['.modes', f'{term.modes.__class__.__name__}', '# Representing Different Modes (combination of attrs) of the terminal'])
		comps = compadd(comps, *['.size', f'{term.size.__class__.__name__}', '# (class) Representing The terminal size, which provides the current width and height of the terminal.'])
		comps = compadd(comps, *['.cursor', f'{term.cursor.__class__.__name__}', '# (class) Representing The terminal cursor, which can be used to control the position and visibility of the cursor.'])
		# comps = compadd(comps, *['.colors', f'{term.colors.__class__.__name__}', '# (class) Representing The terminal color settings: foreground(fg),background(bg) and underline(ul) colors.'])
		mkup = ['\x1b[4G\x1b[32m', '\x1b[20G\x1b[31m', '\x1b[40G\x1b[37m']
		return '\n'.join([section(ROOT='',KEY='Component',VAL='Class',SUBS='.'.join(['','Term()'])),*makeprint(comps,mkup)])

	return Props({}),Comp({})


def cursor():
	print('\x1b[1mlibTerm:')
	print('  .Term.Cursor():\x1b[m')
	print('    \x1b[4mProperty', '\x1b[20GValue', '\x1b[40GDescription\x1b[m')
	props = {}

	props = propadd(props, *['.term', f'{term.cursor.term}', '# Link to the parent(Term()'])
	props = propadd(props, *['.ansi', f'{'\n'.join([str(item) for item in term.cursor.ansi.__members__.items()])}', '# Ansi Enums'])
	props = propadd(props, *['.move', f'{term.cursor.move}', '# Ansi Move Enums'])
	props = propadd(props, *['.visible', f'{term.cursor.visible}', '# Whether the terminal is showing the cursor'])
	props = propadd(props, *['.hidden', f'{term.cursor.hidden}', '# Whether the terminal is hiding the cursor'])
	mkup = ['\x1b[4G\x1b[36m', '\x1b[20G\x1b[33m', '\x1b[40G\x1b[37m']

	for key in props:
		col = 0

		for value in props[key]:
			if not isinstance(props[key][value], list):
				print('{C}{val}'.format(C=mkup[col], val=props[key][value]), end='', flush=True)
			else:
				print('{C}{val}'.format(C=mkup[col], val=props[key][value][0]), end='', flush=True)
				for line in props[key][value][1:]:
					print('\n{C}{val}'.format(C=mkup[col], val=line), end='', flush=True)
			col += 1
		print()

def CheckInputKey(term,key,cb=None):
	def checkinput():
		pressedkey = term.stdin.read()
		if pressedkey== key:
			print('\x1b[3;1HKey:\x1b[32m {KEY}\x1b[m'.format(KEY=key),end='',flush=True)
	return checkinput

def RegKey(term,key,cb=None):
	def match():
		pressedkey = term.tty.stdin.read()
		if pressedkey== key:
			cb()
	matchkey=key
	loop=asyncio.get_event_loop()
	loop.add_reader(term.tty.input.fileno(),match)

class Controls:
	CSI=Term.ANSI.CSI
	prev=''
	def __init__(s,term):
		s.term=term
		s.keymap={
		}
		s.keys=set()
		s.start()

	def register(s,name,key,cb):
		s.keymap[name]={}
		s.keymap[name]['key']=key
		s.keymap[name]['cb']=cb
		s.keys^=set(key)
	def __call__(s):
		key=s.term.stdin.read()
		print('\x1b[3;1HKey:\x1b[32m {KEY}\x1b[m'.format(KEY=repr(key)),end='',flush=True)
		if key==s.CSI+'B':
			print('Down')
		elif key==s.CSI+'A':
			print('Up')
		elif key==s.CSI+'C':
			print('Right')
		elif key==s.CSI+'D':
			print('Left')
		elif key=='\t':
			print('Tab')
		elif key=='\n':
			print('Enter')
		elif key=='q':
			if s.cb is not None:
				s.cb()
	def start(s):
		s.loop=asyncio.get_event_loop()
	def watch(s):
		s.loop.add_reader(s.term.tty.input.fileno(),s)


def main(term):
	import asyncio
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	ctrl=Controls(term)
	ctrl.register('next'	,'q',fnNext	)
	ctrl.start()

	# setting the terminal to control mode, this will allow us to read the input events and control the output
	term.mode=term.MODE.CONTROL
	props,comps=LIBTERM(term)

	print(props.format(ROOT='libTerm'))
	print(comps.format(ROOT='libTerm'))
	print('press q to resume:')

	loop.run_forever()


def fnNext():
	loop=asyncio.get_event_loop()
	print('continuing')
	loop.stop()



# while True:
# 	if term.stdin.check:
# 		key=term.stdin.read()
# print('half terminal size:',repr(term.size.xy/2))
# print('background color: ' ,'\n\tinternal:',term.color.bg, '\n\t16bit:',term.color.bg.RGB16,'\n\tANSI:',repr(term.color.bg.ansi()))
# print(term.cursor.xy)
# term.mode=Term.MODE.CTRL

#
#
# term.cursor.xy=Coord(10,5)
# print('#',end='',flush=True)
# term.cursor.move.down()
# print('#',end='',flush=True)
# term.cursor.move.right()
# print('#',end='',flush=True)
# term.cursor.move.up(2)
# print('#',end='',flush=True)
# term.cursor.move.abs(X=2,Y=12)
# print('#',end='',flush=True)

# term.mode=Term.MODE.normal
if __name__ == '__main__':
	import atexit
	from libTerm import Term
	def ExitProcedure(t):
		t.ANSI.cls()
		t.mode = t.MODE.DEFAULT
		t.buffer = t.BUFFER.DEFAULT
		print('done')
	print('pre1')
	t=Term()
	print('pre2')
	# t.ANSI.cls()
	# atexit.register(ExitProcedure,t)
	# print('pre4')
	main(t)
	print('post 1')
#
# # sys.stdout = io.TextIOWrapper(sys.stdout.detach(), newline=None, encoding="utf-8", buffering=1)
# sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", newline=None, buffering=1, closefd=False)
# import sys,io

