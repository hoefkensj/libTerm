#!/usr/bin/env python
from libTerm import Term,Coord,Color,ColorSet,Ansi
from libTerm.modules.class_menu import Menu
import atexit,asyncio

class Caesar:
	def __init__(s,term):
		s.t=term
		s._string=''
		s._cyphertext=''
	def encrypt(s):
		s._cyphertext=''.join([chr((ord(c)+3-32)%95+32) for c in s._string])
	def decrypt(s):
		s._string=''.join([chr((ord(c)-3-32)%95+32) for c in s._cyphertext])
	def run(s,algo):
		print(Coord(5, 10))
		s.t.mode = t.MODE.DEFAULT
		if algo==1:
			s._string=input('\x1b[mEnter string to encrypt:\x1b[32m ')
			s.encrypt()
		elif algo==2:
			s._cyphertext=input('\x1b[mEnter string to decrypt:\x1b[31m')
			s.decrypt()
		s.print()
		t.mode = t.MODE.CONTROL
	def print(s):
		print(Coord(5,13))
		print('\x1b[0;33mPlainText  : \x1b[1;32m',s._string)
		print('\x1b[0;33mCypherText : \x1b[1;31m',s._cyphertext)


def ExitProcedure(t):
	t.ANSI.cls()
	t.mode = t.MODE.DEFAULT
	t.buffer = t.BUFFER.DEFAULT

def Quit(t):
	t.mode=t.MODE.default
	loop=asyncio.get_running_loop()
	loop.stop()

def Loop(term,M):
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.add_reader(term.stdin.fd, Controls(term,M))
	loop.run_forever()

def Controls(term,M):
	prev=''
	CSI=Ansi.CSI
	caesar=Caesar(term)
	def controls():
		key=term.stdin.read()
		if   key == 'q'    : Quit(term)
		elif key == CSI+'B': M.next()
		elif key == CSI+'A': M.prev()
		elif key == '\n'   : caesar.run(M.choose()[0])
		elif key in '0123456789':
			nonlocal prev
			prev+=key
			if int(prev)>len(M)+1:
				prev=str(1)
			M.select(int(prev))
	return controls

# 	return control
#

def main(term):
	items = ['Encrypt', 'Decrypt', 'Quit (q)']
	M=Menu(term,items ,location=Coord(5,5),nums=True,colors=ColorSet(Color(192,192,0)))
	M.draw()
	Loop(term,M)

if __name__ == '__main__':
	t        = Term()
	t.mode   = t.MODE.CONTROL
	t.buffer = t.BUFFER.ALTERNATE
	t.ANSI.cls()
	atexit.register(ExitProcedure,t)
	main(t)


