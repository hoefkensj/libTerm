#!/usr/bin/env python
from enum import IntEnum,StrEnum


class Mode(IntEnum):
	NONE	= 0
	none	= 0
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


class StoreStop(StrEnum):
	FIRST_OF_STORE	= "FIRST_OF_STORE"
	LAST_OF_STORE	= "LAST_OF_STORE"
