# /usr/bin/env pyhthon
from libTerm import Term,Coord,Mode,Color
from time import sleep
from unicodedata import combining


# /usr/bin/env pyhthon
from libTerm import Term,Coord,Mode,Color

term=Term()

print(term.color.bg.RGB8)
print(term.color.bg.neg.RGB8)
print(term.color.bg.neg.RGB32)
print(term.color.fg.RGB4)
