#!/usr/bin/env python


class Screen:
	"""
	collection of Frames that are tiled, and share borders
	controls wich frame has focus and thereby gets input
	redraws all frames on terminal resize
	"""
	def __init__(s):
		...
	def addFrame(s,name):
		"""
		adds a frame to the screen with title.
		resizes any existing frames
		:param name:
		:return:
		"""
	def focus(s,frame):
		...
	def hide(s,frame):
		...
