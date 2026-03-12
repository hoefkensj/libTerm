#!/usr/bin/env python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Color:
	R: int = field(default=0, metadata={'range': (0, 4294967296)})
	G: int = field(default=0, metadata={'range': (0, 4294967296)})
	B: int = field(default=0, metadata={'range': (0, 4294967296)})
	BIT: int = field(default=8, metadata={'set': (4, 8, 16, 32)})

	def __post_init__(s):
		if s.BIT not in (4, 8, 16, 32):
			raise ValueError(f"BIT must be one of 4,8,16,32. Got {s.BIT}")

		max_val = (1 << s.BIT) - 1

		for ch in ("R", "G", "B"):
			v = getattr(s, ch)
			if not isinstance(v, int) or not (0 <= v <= max_val):
				raise ValueError(f"{ch} must be 0..{max_val} for {s.BIT}-bit input")

		# convert input into internal 32-bit by left-shifting
		shift = 32 - s.BIT
		object.__setattr__(s, "R", s.R << shift)
		object.__setattr__(s, "G", s.G << shift)
		object.__setattr__(s, "B", s.B << shift)
		object.__setattr__(s, "BIT", 32)

	def __invert__(s):
		# return bitwise negation within 32-bit space
		max32 = (1 << 32) - 1
		R = max32 - s.R
		G = max32 - s.G
		B = max32 - s.B
		return Color(R, G, B, 32)


	@property
	def RGB32(s):
		"""Colors are stored in this format internally"""
		return s.R, s.G, s.B

	@property
	def RGB16(s):
		"""
		:return: color in 16bit format:
		"""
		return tuple(v >> 16 for v in s.RGB32)

	@property
	def RGB8(s):
		"""

		:return: color in 8bit format
		"""
		return tuple(v >> 24 for v in s.RGB32)

	@property
	def RGB4(s):
		"""

		:return: colorin 4bit format
		"""
		return tuple(v >> 28 for v in s.RGB32)

	def ansi(s, bits: int = 8) -> str:
		"""

		:param bits: the desired bit depth of the output,ansi default is 8bit (0-255) per channel
		:return: the color values in  8bit per channel formatted as R;G;B for easy inclusion in ansi escapes
		"""
		if bits == 32:
			rgb = s.RGB32
		elif bits == 16:
			rgb = s.RGB16
		elif bits == 8:
			rgb = s.RGB8
		elif bits == 4:
			rgb = s.RGB4
		else:
			raise ValueError("bits must be 4,8,16,32")

		return ";".join(str(v) for v in rgb)

	@property
	def ansifg(s):
		"""

		:return: the color formatted for use as an ANSI ESC Seq foreground color (ESC [ 38;2;R;G;B m)
		"""
		return f"\x1b[38;2;{s.ansi(8)}m"
	@property
	def ansibg(s):
		"""

		:return: the color formatted for use as an ANSI ESC Seq background color (ESC [ 48;2;R;G;B m)
		"""
		return f"\x1b[48;2;{s.ansi(8)}m"
	@property
	def ansiul(s):
		"""

		:return: the color formatted for use as an ANSI ESC Seq underline color (ESC [ 58;2;R;G;B m)
		"""
		return f"\x1b[58;2;{s.ansi(8)}m"

	@property
	def neg(s):
		"""

		:return: the negative of the color in 32bit format
		"""
		return s.__invert__()

	@staticmethod
	def fromweb(hexstr='#FFFFFF'):
		"""Create a Color from a web hex string like '#RRGGBB' or '#RGB'."""
		h = hexstr.lstrip('#')
		if len(h) == 6:
			r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
		elif len(h) == 3:
			r, g, b = (int(h[i]*2, 16) for i in range(3))
		else:
			raise ValueError("Hex string must be in format '#RRGGBB' or '#RGB'")
		return Color(r, g, b)


class ColorSet():
	def __init__(s, fg=None, bg=None, ul=None):
		"""
		Stores a set of colors for foreground, background, and underline. Each can be a Color instance or None.
		:param fg: foreground color (Color or None)
		:param bg: background color (Color or None)
		:param ul: underline color (Color or None)
		"""
		# accept either Color instances or None
		valid = True
		for c in (fg, bg, ul):
			if not (isinstance(c, Color) or c is None):
				valid = False
		if not valid:
			raise ValueError("fg(foreground), bg(background), and ul(underline) must be instances of Color or None")
		s.fg = fg
		s.bg = bg
		s.ul = ul


class ColorPalette():
	def __init__(s, ):
		s.size = 0
		s.keys = {}

	def add(s, name, colorset):
		s.__setattr__(name, colorset)
		s.keys[s.size] = name
		s.size += 1

	def updateset(s, name, colorset):
		s.__setattr__(name, colorset)

	def updatecolor(s, name, layer, color):
		cs = getattr(s, name)
		ds = {}
		ds['fg'] = getattr(cs, 'fg')
		ds['bg'] = getattr(cs, 'bg')
		ds['ul'] = getattr(cs, 'ul')
		ds[layer] = color
		s.updateset(name, ColorSet(**ds))

	def __call__(s, name, layer):
		cs = getattr(s, name)
		return getattr(cs, layer)

	@property
	def inverted(s):
		# return inverted ColorSet of the most recently added palette entry (swap fg/bg)
		if s.size == 0:
			return ColorSet(None, None)
		last_name = s.keys[s.size - 1]
		cs = getattr(s, last_name)
		return ColorSet(fg=cs.bg, bg=cs.fg)
