# /usr/bin/env pyhthon
import unittest
from libTerm.types.selector import Selector

class TestSelector(unittest.TestCase):
	results=[]
	S=Selector((1,20),dn=-5,up=+5,start=-5)
	results.append(S.read())
	for i in range(30):
		results.append(S.next())
	S.setstep(-1, 1)
	for i in range(30):
		results.append(S.next())
	results.append(S.write(20))
	results.append(S.read())
	S.expand(15)
	results.append(S.read())
	for i in range(30):
		results.append(S.next())
	results.append('21',S.next())
	results.append(S.next())
	results.append(S.next())
	results.append(S.next())
	results.append(S.next())
	results.append(S.next())
	print(results)