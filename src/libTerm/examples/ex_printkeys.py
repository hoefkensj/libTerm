#!/usr/bin/env python
from libTerm import Term
from libTerm.types import Mode
T=Term()
print('press qq(double q) to quit!')
Qs=[]
while True:

	if T.stdin.event:
		key=T.stdin.read()
		print(repr(key))
		Qs.append(key)
	if 'qq' in ''.join(Qs):
		break
T.buffers.default()