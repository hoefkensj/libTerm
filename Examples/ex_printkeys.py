# /usr/bin/env pyhthon
from libTerm import Term,Mode

T=Term()
T.mode=Mode.CONTROL
T.buffer.alternate()
print('press qq(double q) to quit!')
Qs=[]
while True:

	if T.stdin.event:
		key=T.stdin.read()
		print(repr(key))
		Qs.append(key)
	if 'qq' in ''.join(Qs):
		break
T.buffer.default()