#!/usr/bin/env python
import unittest
from libTerm import Selector
import time

class TestSelector(unittest.TestCase):
	def test_base(t):
		sela=Selector((1,50))
		t.assertEqual(1,sela.read())
		t.assertEqual(2,sela.next())
		t.assertEqual(48,sela.write(48))
		t.assertEqual(49,sela.next())
		t.assertEqual(50,sela.next())
		t.assertEqual(1,sela.next())
		print('\x1b[120G',sela.prev())
	def test_onebase(t):
		sela=Selector(50)
		t.assertEqual(1,sela.read())
		t.assertEqual(2,sela.next())
		t.assertEqual(48,sela.write(48))
		t.assertEqual(49,sela.next())
		t.assertEqual(50,sela.next())
		t.assertEqual(1,sela.next())
		print('\x1b[120G',sela.prev())

	def test_step(t):
		selb = Selector((4, 400),up=4,dn=-8)
		t.assertEqual(4, selb.read())
		t.assertEqual(8, selb.next())
		t.assertEqual(397, selb.prev())
		t.assertEqual(389, selb.prev())

	def test_modstep(t):
		selc = Selector((0, int(1e9)), 1, 1, 9)
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
		t.assertEqual(40,result)
		result=selc.next()
		t.assertEqual(50,result)

	def test_zeroone(t):
		selc=Selector((0,1))
		t.assertEqual((0,1),selc.range)
		t.assertEqual(0,selc.read())
		t.assertEqual(1,selc.next())
		t.assertEqual(0,selc.write(6))
	def test_zero(t):
		selc=Selector(0)
		t.assertEqual((0,1),selc.range)
		t.assertEqual(0,selc.read())
		t.assertEqual(1,selc.next())
		t.assertEqual(0,selc.write(6))
	def test_equal(t):
		selc=Selector((8,8))
		t.assertEqual((8,8),selc.range)
		t.assertEqual(8,selc.read())
		t.assertEqual(8,selc.next())
		t.assertEqual(8,selc.write(6))


	def test_store(t):


		s=Selector((-1,2),start=1)
		t.assertEqual(1,s.read())
		t.assertEqual(2,s.next())
		t.assertEqual(-1,s.next())
		t.assertEqual(2,s.prev())
