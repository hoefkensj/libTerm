# /usr/bin/env pyhthon
import os, sys, select
from libTerm import Term,Mode
fd = sys.stdin.fileno()
buf = b""
term=Term()
term.mode(Mode.CONTROL)
while True:
    r, _, _ =
    if not r:
        continue

    buf += os.read(fd, 8)

    # Arrow keys
    if buf.startswith(b'\x1b[') and len(buf) >= 3:
        seq = buf[:3]
        buf = buf[3:]

        if seq == b'\x1b[D':
            print("LEFT")
        elif seq == b'\x1b[C':
            print("RIGHT")
        elif seq == b'\x1b[A':
            print("UP")
        elif seq == b'\x1b[B':
            print("DOWN")

    # Single character
    elif buf and buf[0] >= 32:
        print(chr(buf[0]))
        buf = buf[1:]