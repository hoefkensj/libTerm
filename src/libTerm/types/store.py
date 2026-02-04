# /usr/bin/env pyhthon


class Store():
	def __init__(s, **k):
		"""Simple contiguous store backed by a list of values.

		Keys are 1-based integers (1..n). Internally values are stored in
		`s._values` where index 0 corresponds to key 1.

		Pointer semantics:
		- s._pointer ranges from -1 .. len(s._values)
		- -1 means before-first
		- 0..len-1 means index into values (current)
		- len means after-last

		By default the store has unlimited size; use `setmax` to bound it.
		"""
		s._store = {0:None,}
		s._tail=1
		s._size=1
		s._current= 0
		s._pointer = lambda:s._store.values.get(s._current)
		s._max = None
		s._selector=Selector(s.size,start=1)
		s._selected = None
		s._value=None
		s._keys=[]
	def __update_selector__(s):
		s._selector=Selector((1,s.size+1))
	@property
	def selected(s):
		s._selected=s._selector.read()
		return s._selected,s.value
	def select(s,idx):
		if idx>s.size:
			idx=s.size
		s._selector.write(idx)


	@property
	def size(s):
		s._size=len(s._store)
		return s._size

	def max(s, mx=None):
		if mx is not None :
			if not isinstance(mx, int) or mx < 1:
				raise ValueError('maximum must be a positive int or None')
			s._max=mx

		if s._max is None and mx is None:
			s._max = 4294967295

		return s._max

	@property
	def value(s):
		s._value=s._store[s._selected]
		return s._value
	@value.setter
	def value(s,val):
		s._store[s.selected]=val

	def save(s, value):
		if not (s.size>=s.max()):
			idx=s.size
			s._store[idx]=value
			s._keys+=[idx]
			s._tail+=1
		return idx,s._store[idx]

	def remove(s):
		current=s._selector.read()
		value=s._store.pop(current)
		return value
	def remove_index(s,idx):
		result=None
		if idx > 0 and idx in s._store.values():
			val=s._store[idx]
			oldstore={**s._store}
			tomove={k:oldstore[k] for k in oldstore if k>idx}
			s._store={k:oldstore[k] for k in oldstore if k<idx}
			for key in tomove:
				s._store[key-1]=oldstore[key]

			result= {idx:val}
		return result

	def clear(s):
		s._store.clear()
		s._store={0:None,}
		s._tail = 1
		s._current=0
		s._selector=Selector(s.size())
		s.read()
		return

	def prev(s):
		key=s._selector.prev
		return s._store.get(key)

	def next(s):
		s.select(s.select.next())
		return s._store.get(s.selected)

	def replace(s,value, idx: int=None):
		if idx is None:
			idx=s.selected
		if 0 < idx < s.size:
			s._store[idx]=value


	def __len__(s):
		result = len(s._store.values()-1)
		return result

	def keys(s):
		result = list(range(1, len(s._store.values()) + 1))
		return result
