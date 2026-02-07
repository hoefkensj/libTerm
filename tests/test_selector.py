# /usr/bin/env pyhthon
import unittest
from libTerm import Selector
import time

class TestSelector(unittest.TestCase):
	def test_base(t):
		sela=Selector((1,5),start=1)
		selb=Selector((-100,100),10,10,0)
		selc = Selector((1, int(1e9)), 1, 1, 0)
		def modrange(sel):
			if sel.read() == 10:
				sel.setstep(1, 10)
			elif sel.read() == 100:
				sel.setstep(10, 100)
			elif sel.read() == 1e3:
				sel.setstep(100, 1000)
			elif sel.read() == 1e4:
				sel.setstep(1e3, 1e4)
			return sel
		for i in range(2):
			for j in range(2):
				selc.next()
				modrange(selc)
		result=selc.read()
		t.assertEqual(10,result)
		result=selc.next()
		t.assertEqual(900000000,result)
	def test_store(t):


		s=Selector((-1,2),start=1)
		t.assertEqual(1,s.read())
		t.assertEqual(2,s.next())
		t.assertEqual(-1,s.next())
		t.assertEqual(2,s.prev())
