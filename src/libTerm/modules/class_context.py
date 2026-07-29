#!/usr/bin/env python
import asyncio

from libTerm.modules.class_controls import Controls
from libTerm import Coord
class Context():
	def __init__(s,term,loop=None,name=None):
		s.term=term
		s.loop=loop
		s.name=name
		s._frames={}
		s._spacefill=[]
		s.fid=0
		s.focusid=0
		s.frame=None
		s.controls=None
		s._location=Coord(1,1)
		s._size=Coord(*s.term.size.xy)
		s._show=False

	def enableControls(s,state):
		if state:
			s.controls=Controls(term=s.term, loop=s.loop)
		else:
			s.controls=None

	def addFrame(s,frame):
		fid=len(s._frames)+1
		s._frames[fid]=frame
		if fid>0 and s.focusid==0:
			s.focusid=1
			s._frames[1].focus()
		if s.frame is None:
				s.frame=frame
		return fid

	def selectFrame(s,n=1):
		s.frame=s._frames.get(n)
		if s.frame is not None:
			s.frame.focus(True)
			s.frame.draw()
			s.focusid=n

	def focusnext(s,*a):
		if s.frame is not None:
			s.frame.focus(False)
		s.focusid+=1
		if s.focusid>len(s._frames):
			s.focusid=0
		s.selectFrame(s.focusid)

	def show(s):
		if s._show is False:
			s._show=True
			for f in s._frames:
				s._frames[f].show()
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

