# /usr/bin/env pyhthon
import unittest
from libTerm import Store
import time

class TestStore(unittest.TestCase):
	def test_store(t):
		store=Store()
		store.save('a')
		t.assertEqual('a',store.value)
		store.save('b')
		t.assertEqual('b',store.value)
		store.prev()
		store.prev()
		t.assertEqual('a',store.value)
		store.prev()
		t.assertEqual('a',store.value)


		print(store.selected)

		# store.save('a')
		# store.save('b')
		# store.save('c')
		# store.save('d')
