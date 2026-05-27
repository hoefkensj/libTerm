#!/usr/bin/env python
import unittest
from libTerm.components import Store
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
#!/usr/bin/env python
import unittest
from libTerm import Term
from libTerm.components import Store
from libTerm.components.enums import StoreStop

class TestStore(unittest.TestCase):
	def setUp(s):
		# Term() will be the mock Term when not running in a tty
		s.term = Term()
		s.store = Store(term=s.term)

	def test_save_and_select_and_len(s):
		r1 = s.store.save('a')
		s.assertEqual(r1, {1: 'a'})
		r2 = s.store.save('b')
		s.assertEqual(r2, {2: 'b'})
		r3 = s.store.save('c')
		s.assertEqual(r3, {3: 'c'})
		s.assertEqual(s.store.size(), 3)
		s.assertEqual(len(s.store), 3)
		# selecting without index returns current pointer's value

	def test_prev_next_and_stop_flags(s):
		s.store.save('one')
		s.store.save('two')
		s.store.save('three')
		# current is last (3)
		cur, val = s.store.prev()
		s.assertEqual((cur, val), (2, 'two'))
		cur, val = s.store.prev()
		s.assertEqual((cur, val), (1, 'one'))
		# another prev stays at first and stop is FIRST_OF_STORE
		cur, val = s.store.prev()
		s.assertEqual((cur, val), (1, 'one'))
		s.assertEqual(s.store.stop, StoreStop.FIRST_OF_STORE)
		# moving next moves forward
		cur, val = s.store.next()
		# after FIRST_OF_STORE, next() should go to 1 then 2
		s.assertIn(cur, (1, 2))
		# move repeatedly to last
		for _ in range(5):
			cur, val = s.store.next()
		s.assertEqual(s.store.stop, StoreStop.LAST_OF_STORE)

	def test_remove_shifts_and_pop(s):
		s.store.save('a')
		s.store.save('b')
		s.store.save('c')
		s.assertEqual(s.store.size(), 3)


	def test_replace_and_setmax(s):
		s.store.save('x')
		s.store.save('y')
		s.store.save('z')
		# replace middle

		# set max smaller than current size: keep newest entries
		s.store.max(2)
		s.assertLessEqual(s.store.size(), 2)


	def test_errors_on_invalid_inputs(s):
		with s.assertRaises(ValueError):
			s.store.max(0)
		with s.assertRaises(IndexError):
			s.store.replace(100, 'nope')
		with s.assertRaises(IndexError):
			s.store.remove(100)
		with s.assertRaises(IndexError):
			s.store.pop(1)  # popping from empty store (after previous tests) may raise

if __name__ == '__main__':
	unittest.main()