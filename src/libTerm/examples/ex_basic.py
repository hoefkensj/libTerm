#!/usr/bin/env python
from libTerm import Term
from libTerm.types import Mode,Buffer



def head():
	return "\x1b[2J\x1b[1;1H\x1b[1;4mReading State,Properties and Data from the terminal :\x1b[m"
def section(root,subs):
	return '\n\x1b[1m{ROOT}:\n\t{SUBS}:\x1b[m\n\x1b[4mProperty\x1b[20GValue\x1b[40GDescription\x1b[m'

def Props(props):
	mkup=['\x1b[4G\x1b[36m','\x1b[20G\x1b[33m','\x1b[40G\x1b[37m']
	def propadd(props, prop, val, desc):
		props[len(props)] = {
			'prop': prop,
			'val': val,
			'desc': desc
		}
		return props
	def makeprint(toprint):
		for key in props:
			col = 0
			for value in props[key]:
				if not isinstance(props[key][value], list):
					toprint += ['{C}{val}'.format(C=mkup[col], val=props[key][value])]
				else:
					toprint += ['{C}{val}'.format(C=mkup[col], val=props[key][value][0])]
					for line in props[key][value][1:]:
						toprint += ['\n{C}{val}'.format(C=mkup[col], val=line)]
				col += 1
				toprint += ['\n']
		return toprint
	props=propadd(props,*['.pid',f'{term.pid}','# Process ID of the current process.'])
	props=propadd(props,*['.ppid',f'{term.ppid}','# Process ID of the parent process.Usually the shell that started the program.'])
	props=propadd(props,*['.stdfd',f'{term.stdfd}','# File descriptor for the terminal input,output,error.'])
	props=propadd(props,*['.tty',f'{term.tty}','# The name of the terminal device.'],)
	props=propadd(props,*['.echo',f'{term.echo}','# Whether the terminal is currently echoing input.'])
	props=propadd(props,*['.canonical',f'{term.canonical}','# Whether the terminal is currently in canonical mode.'])
	props=propadd(props,*['.mode',f'\x1b[31mMode.\x1b[33m{term.MODE(term.mode).name}', [
		'# The current mode of the terminal:',
		'# Value is set with the Mode(Enum) class:',
		'#   - Mode.NORMAL  : The normal mode  : the terminal behaves as usual.)',
		'#   - Mode.CONTROL : The control mode : input events are instant and not echo-ed']])
	return ''.join(makeprint([section('libTerm','.'.join(['','Term()']))]))

def Comp(comps):
	def compadd(comps, comp, cls, desc):
		comps[len(comps)] = {
			'comp': comp,
			'class': cls,
			'desc': desc}
		return comps

	comps = {}
	comps = compadd(comps, *['.attr', f'{term.attr.__class__.__name__}', '# Representing The terminal attributes, which can be used to get and set various terminal settings.'])
	comps = compadd(comps, *['.size', f'{term.size.__class__.__name__}', '# (class) Representing The terminal size, which provides the current width and height of the terminal.'])
	comps = compadd(comps, *['.cursor', f'{term.cursor.__class__.__name__}', '# (class) Representing The terminal cursor, which can be used to control the position and visibility of the cursor.'])
	comps = compadd(comps, *['.stdin', f'{term.stdin.__class__.__name__}', '# (class) Representing The terminal standard input, which can be used to read input events from the terminal.'])
	comps = compadd(comps, *['.color', f'{term.color.__class__.__name__}', '# (class) Representing The terminal color settings: foreground(fg),background(bg) and underline(ul) colors.'])
	mkup = ['\x1b[4G\x1b[32m', '\x1b[20G\x1b[31m', '\x1b[40G\x1b[37m']
	print('\x1b[1mlibTerm\x1b[m:')
	print('\x1b[1m  .Term():\x1b[m')
	print('\x1b[4G\x1b[4mComponent', '\x1b[20GClass', '\x1b[40GDescription\x1b[m')
	# print('\x1b[1mTerm()\x1b[20GlibTerm.term.structs.\x1b[m')
	for key in comps:
		col = 0

		for value in comps[key]:
			if not isinstance(comps[key][value], list):
				print('{C}{val}'.format(C=mkup[col], val=comps[key][value]), end='', flush=True)
			else:
				print('{C}{val}'.format(C=mkup[col], val=comps[key][value][0]), end='', flush=True)
				for line in comps[key][value][1:]:
					print('\n{C}{val}'.format(C=mkup[col], val=line), end='', flush=True)
			col += 1
		print()


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


def main(term):
	term=term
	# setting the terminal to control mode, this will allow us to read the input events and control the output
	term.mode=Mode.CONTROL
	props=Props({})
	print(props)
	print('press q to resume:')
	while True:
		from time import sleep
		if term.stdin.event:
			key=term.stdin.read()
			print('\x1b[3;1HKey:\x1b[32m {KEY}\x1b[m'.format(KEY=key),end='',flush=True)
			if key=='q':
				print('continuing')
				break
		sleep(0.01)











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
	term=Term()
	# Switch to the alternate buffer, so we don't mess with the main buffer of the terminal,
# and we can easily switch back to it when we are done.
	term.buffer=Buffer.ALTERNATE
	main(term)
