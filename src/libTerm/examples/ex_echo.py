#!/usr/bin/env python
import sys
from libTerm import Term

t=Term()

t.attr.echo=True
print('bls')
print('\n\n\n\n','test')

input()
t.attr.echo=False
print('bls')
print('\n\n\n\n','test')
input()
sys.exit()