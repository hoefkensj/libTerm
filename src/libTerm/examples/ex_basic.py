#!/usr/bin/env python
from libTerm import Term,Color,Coord
from termios import tcgetwinsize
import time
term=Term()
print()
print('terminal size:','libterm:',repr(term.size.getsize()),'termios: ', tcgetwinsize(term.fd))
print('half terminal size:',repr(term.size.xy/2))
print('background color: ' ,'\n\tinternal:',term.color.bg, '\n\t16bit:',term.color.bg.RGB16,'\n\tANSI:',repr(term.color.bg.ansi()))
print(term.cursor.xy)
term.mode=Term.MODE.CTRL
print('press q to resume:')
while True:
	if term.stdin.event:
		key=term.stdin.read()
		print('\x1b[3;1HKey:\x1b[32m {KEY}\x1b[m'.format(KEY=key),end='',flush=True)
		if key=='q':
			print('continuing')
			break
	time.sleep(0.01)



term.cursor.xy=Coord(10,5)
print('#',end='',flush=True)
term.cursor.move.down()
print('#',end='',flush=True)
term.cursor.move.right()
print('#',end='',flush=True)
term.cursor.move.up(2)
print('#',end='',flush=True)
term.cursor.move.abs(X=2,Y=12)
print('#',end='',flush=True)

term.mode=Term.MODE.normal


