#!/usr/bin/env python
import os,sys
if not sys.stdin.isatty():
	try:
		from libTerm.term.mock import Term
	except Exception as E:
		print(E,"->Failed loading Term , falling back to VirtualTerm")
		from libTerm.term.virt import VirtTerm as Term

elif os.name == 'nt':
	from libTerm.term.winnt import Term
else:
	from libTerm.term.posix import Stdin,Cursor,TermAttrs,TermBuffers,TermColors
	from libTerm.term.posix import Term

