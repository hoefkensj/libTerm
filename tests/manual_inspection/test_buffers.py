# /usr/bin/env pyhon
import sys

from libTerm import Term
from libTerm import Coord
import time



T=Term()
print(T.buffer.name)
time.sleep(1)
T.buffers.set(T.BUFFER.ALTERNATE)
print(T.buffer.name)
time.sleep(1)
T.buffers.set(T.BUFFER.DEFAULT)
print(T.buffer.name)
time.sleep(1)
