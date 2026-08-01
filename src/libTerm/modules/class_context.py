#!/usr/bin/env python
import asyncio

from libTerm.modules.class_controls import Controls
from libTerm.modules.class_frame import Frame
from libTerm import Coord
class Context():
	def __init__(s,term,loop=None,name=None):
		s.term=term
		s.loop=loop
		s.name=name
		s._frames={}
		s._spacefill=[]
		s._frameid=0
		s._idcount=0
		s._focusid=0
		s.frame=None
		s.controls=None
		s._location=Coord(1,1)
		s._size=Coord(*s.term.size.xy)
		s._show=False

	def _mkframeid(s):
		s._idcount+=1
		return s._idcount

	def enableControls(s,state):
		if state:
			s.controls=Controls(term=s.term, loop=s.loop)
		else:
			s.controls=None

	def addFrame(s,**k):
		fid=s._mkframeid()
		frm=Frame(s, **k)
		s.__setattr__(k.get('name'),frm)
		s._frames[fid]=frm
		if s._focusid==0:
			s.focusFrame(fid)
		frm.show(True)
		return frm

	def focusFrame(s,frameid):
		frameid=frameid%(s._idcount+1)
		if s.frame is not None:
			s.frame.focus(False)
		s.frame=s._frames.get(frameid)
		if frameid !=0:
			s.frame.focus(True)
			s._frameid=frameid
		s._focusid=frameid

	def focusNext(s,*a):
		s.focusFrame(s._focusid+1)

	def show(s,state=True):
		s._show=state
		for f in s._frames:
			s._frames[f].show(state)

	def ExitProcedure(s):
		s.term.mode = s.term.MODE.DEFAULT
		s.term.buffer = s.term.BUFFER.DEFAULT

	def __enter__(s):
		print('enter')
		s.__startup__()

	def __startup__(s):
		# s.term.buffer = s.term.BUFFER.ALTERNATE
		if s.loop is None:
			s.loop=s._getLoop()
		s.loop.run_forever()

	def __exit__(s):
		pass

	def _getLoop(s):
		try:
			loop=asyncio.get_running_loop()
		except Exception:
			loop=asyncio.new_event_loop()
		return loop

