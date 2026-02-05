# /usr/bin/env pyhthon
import unittest
from libTerm import Selector
import time

class TestSelector(unittest.TestCase):
	def test_selector(t):
		sela=Selector((1,5),start=1)
		selb=Selector((-100,100),10,10,0)
		selc = Selector((1, int(1e9)), 1, 1, 0)
		for i in range(100):
			if selc.read() == 10:
				selc.setstep(1, 10)
			elif selc.read() == 100:
				selc.setstep(10, 100)
			elif selc.read() == 1e3:
				selc.setstep(100, 1000)
			elif selc.read() == 1e4:
				selc.setstep(1e3, 1e4)
			elif selc.read() == 1e5:
				selc.setstep(1e4, 1e5)
			elif selc.read() == 1e6:
				selc.setstep(1e5, 1e6)
				selc.next()
			result=selc.read()

		t.assertEqual(1000000000,result)



# 		sel2=Selector((100,500),start=1)
# 	print(sel2.range)
# 	print(sel2.write(400))
# 	print(sel2.next())
# 	print(sel2.next())
# 	print(sel2.next())
# 	print(sel2.write(250))
# 	print(sel2.next())
# 	print(sel2.read())
#
#
# ())







	time.sleep(15)