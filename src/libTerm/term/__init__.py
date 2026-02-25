#!/usr/bin/env python
import os
if os.name == 'posix':
	from libTerm.term.posix import Term
if os.name == 'nt':
	from libTerm.term.winnt import Term









