#!/usr/bin/env python
import asyncio


class Controls:
	def __init__(s,**k):
		s.term = k.get('term')
		s.loop = k.get('loop')
		s.tty =  s.term.tty
		s.input= s.tty.input
		s.registry = {}
		s.keys = set()
		s.seqs = []
		s.sets = []
		s.keyin=None
		s.seqin=[]

		s.event=None
		s.partial = False
		s.loop.add_reader(s.input.fd,s.match)

	def regkey(s, key, func):
		s.registry[key]=func
		s.keys.add(key)
	def regseq(s, seq, func):
		s.registry[seq]=func
		s.seqs+=[seq]
	def regset(s, keyset, func):
		s.registry[keyset]=func
		s.sets+=[keyset]

	def readkey(s):
		s.keyin = s.input.read()
		s.seqin+=[s.keyin]

	def match(s,*a):

		def matchsingle():
			for matchkey in s.keys:
				if s.keyin == matchkey:
					s.registry[matchkey]()
		def matchseq():
			seqin=''.join(s.seqin)
			print('\x1b[7;1H',seqin)
			for seq in s.seqs:
				if seq.startswith(seqin):
					print('\x1b[8;1H',seqin,seq)
					s.partial = True
					if seqin == seq:
						s.registry[seq](seqin)
						s.seqin=[]
						s.partial=False
				else:
					s.partial=False
			if not s.partial:
				s.seqin=[]
		def matchset():
			for keyset in s.sets:
				if s.keyin in keyset:
					s.registry[keyset](s.keyin)

		s.readkey()
		matchsingle()
		matchseq()
		matchset()
		# print('ran match on key:',s.keyin,'seq:',s.seqin)genymootion incluseive
