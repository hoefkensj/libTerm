#!/usr/bin/env python
from libTerm import Coord,Color,

def main(term):
	print(Types.Color(255, 0, 0))
	print(Types.Position(10, 20))
	print(Types.Size(80, 24))

if __name__ == '__main__':
	t = Types.Term()
	main(t)