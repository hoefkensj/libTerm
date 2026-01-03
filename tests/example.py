# /usr/bin/env pyhthon
from libTerm import Term,Color,Coord

term=Term()
print(term.size.xy)
print(term.color.bg)
print(term.cursor.xy)

CursorCoord=Coord(10,5)
term.cursor.xy=CursorCoord
print(term.cursor.xy)
term.mode='ctrl'
print(input())
