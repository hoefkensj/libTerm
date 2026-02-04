#/usr/bin/env pyhthon
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Color:
	R: int = field(default=0, metadata={'range': (0, 4294967296)})
	G: int = field(default=0, metadata={'range': (0, 4294967296)})
	B: int = field(default=0, metadata={'range': (0, 4294967296)})
	BIT: int = field(default=8, metadata={'set': (4, 8, 16, 32)})

	def __post_init__(self):
		if self.BIT not in (4, 8, 16, 32):
			raise ValueError(f"BIT must be one of 4,8,16,32. Got {self.BIT}")

		max_val = (1 << self.BIT) - 1

		for ch in ("R", "G", "B"):
			v = getattr(self, ch)
			if not isinstance(v, int) or not (0 <= v <= max_val):
				raise ValueError(f"{ch} must be 0..{max_val} for {self.BIT}-bit input")

		# convert input into internal 32-bit by left-shifting
		shift = 32 - self.BIT
		object.__setattr__(self, "R", self.R << shift)
		object.__setattr__(self, "G", self.G << shift)
		object.__setattr__(self, "B", self.B << shift)
		object.__setattr__(self, "BIT", 32)

	def __invert__(s):
		R=4294967296-s.R
		G=4294967296-s.G
		B=4294967296-s.B
		return Color(R,G,B,32)
	# ----- Internal storage -----
	@property
	def RGB32(self):
		return self.R, self.G, self.B

	# ----- Truncated outputs -----
	@property
	def RGB16(self):
		return tuple(v >> 16 for v in self.RGB32)

	@property
	def RGB8(self):
		return tuple(v >> 24 for v in self.RGB32)

	@property
	def RGB4(self):
		return tuple(v >> 28 for v in self.RGB32)

	# ----- ANSI decimal output -----
	def ansi(self, bits: int = 8) -> str:
		if bits == 32:
			rgb = self.RGB32
		elif bits == 16:
			rgb = self.RGB16
		elif bits == 8:
			rgb = self.RGB8
		elif bits == 4:
			rgb = self.RGB4
		else:
			raise ValueError("bits must be 4,8,16,32")

		return ";".join(str(v) for v in rgb)
	@property
	def neg(s):
		return s.__invert__()
