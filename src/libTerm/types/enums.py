# /usr/bin/env pyhthon
from enum import IntEnum


class Mode(IntEnum):
	NONE	= 0
	none	= 1
	NRML	= 1
	nrml	= 1
	NORMAL  = 1
	normal  = 1
	DEFAULT = 1
	default = 1
	CTL	 = 2
	ctl	 = 2
	CTRL	= 2
	ctrl	= 2
	CONTROL = 2
	control = 2
	inp     = 3
	Inp     = 3
	Input   = 3
	INP      = 3
	INPUT      = 3


class Stop(IntEnum):
	FIRST_OF_STORE	= 1
	LAST_OF_STORE	= -1
