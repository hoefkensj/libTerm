#!/usr/bin/env python
def main(term):
	print(f"{term.color.fg.RGB8=}")
	print(f"{term.color.bg.RGB8=}")
	print(f"{term.color.bg.neg.RGB8=}")
	print(f"{term.color.bg.neg.RGB32=}")
	print(f"{term.color.fg.RGB4=}")


if __name__ == "__main__":
	from libTerm import Term
	t=Term()
	main(t)
