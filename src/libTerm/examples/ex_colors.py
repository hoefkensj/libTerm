#!/usr/bin/env python
def main(term):
	print(f"{term.color.fg.RGB8=}")
	print(f"{term.color.bg.RGB8=}")
	print(f"{term.color.bg.neg.RGB8=}")
	print(f"{term.color.bg.neg.RGB32=}")
	print(f"{term.color.fg.RGB4=}")


from libTerm import Term
t=Term()
main(t)
print('press q to resume:')
while True:
	from time import sleep
	if t.stdin.check():
		key=t.stdin.read()
		print('\x1b[3;1HKey:\x1b[32m {KEY}\x1b[m'.format(KEY=key),end='',flush=True)
		if key=='q':
			print('continuing')
			break
	sleep(0.01)