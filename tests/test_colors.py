# -*- coding: utf-8 -*-
import unittest
from itertools import product

from libTerm.types.class_color import Color, ColorSet, ColorPalette


class TestColors(unittest.TestCase):
	def assertTupleEqualInt(self, a, b):
		# helper: compare integer tuples elementwise
		self.assertEqual(tuple(int(x) for x in a), tuple(int(x) for x in b))

	def test_color_basic_and_bit_conversions(self):
		# Basic 8-bit input -> internal storage and conversion back
		c = Color(255, 128, 0, 8)
		# RGB8 should return the original 8-bit inputs
		self.assertTupleEqualInt(c.RGB8, (255, 128, 0))
		# RGB16 and RGB4 are computed from the same internal representation
		self.assertEqual(len(c.RGB16), 3)
		self.assertEqual(len(c.RGB4), 3)

	def test_ansi_formats_and_bits(self):
		c = Color(1, 2, 3, 8)
		# ansi should return semicolon separated values for requested bit depths
		self.assertEqual(c.ansi(8), "1;2;3")
		# asking unsupported bits should raise ValueError
		with self.assertRaises(ValueError):
			_ = c.ansi(7)

	def test_fromweb_hex_variants(self):
		# test 6-digit hex
		c1 = Color.fromweb('#FF8000')
		self.assertTupleEqualInt(c1.RGB8, (255, 128, 0))
		# test 3-digit hex
		c2 = Color.fromweb('#F80')
		self.assertTupleEqualInt(c2.RGB8, (255, 136, 0))

	def test_invert_negative(self):
		# Create a mid-range color and invert it: double-inverting should return original
		c = Color(10, 20, 30, 8)
		inv = ~c
		# Inverting twice should produce a color equivalent to the original
		inv2 = ~inv
		self.assertTupleEqualInt(inv2.RGB8, c.RGB8)

	def test_colorset_valid_and_invalid(self):
		fg = Color(10, 20, 30, 8)
		bg = Color(1, 2, 3, 8)
		ul = None
		cs = ColorSet(fg=fg, bg=bg, ul=ul)
		self.assertIs(cs.fg, fg)
		self.assertIs(cs.bg, bg)
		self.assertIs(cs.ul, ul)
		# invalid values should raise ValueError
		with self.assertRaises(ValueError):
			_ = ColorSet(fg="not-a-color", bg=None, ul=None)

	def test_palette_add_lookup_and_inverted(self):
		p = ColorPalette()
		cs1 = ColorSet(fg=Color(1, 1, 1, 8), bg=Color(2, 2, 2, 8))
		p.add('one', cs1)
		# callable access: palette(name, layer)
		self.assertIs(p('one', 'fg'), cs1.fg)
		self.assertIs(p('one', 'bg'), cs1.bg)
		# inverted palette should swap fg/bg
		inv = p.inverted
		self.assertIs(inv.fg, cs1.bg)
		self.assertIs(inv.bg, cs1.fg)

	def test_palette_update_and_updatecolor(self):
		p = ColorPalette()
		p.add('x', ColorSet(fg=Color(1, 1, 1, 8), bg=None))
		# update the whole set
		p.updateset('x', ColorSet(fg=Color(3, 3, 3, 8), bg=Color(4, 4, 4, 8)))
		self.assertTupleEqualInt(p('x', 'fg').RGB8, (3, 3, 3))
		# update a single layer via updatecolor (intended API)
		p.updatecolor('x', 'bg', Color(7, 8, 9, 8))
		self.assertTupleEqualInt(p('x', 'bg').RGB8, (7, 8, 9))

	def test_permutations_of_colorset_construction(self):
		# Create permutations of None and a couple of Colors for fg/bg/ul and ensure construction
		colors = (None, Color(0, 0, 0, 8), Color(255, 255, 255, 8))
		for fg, bg, ul in product(colors, repeat=3):
			cs = ColorSet(fg=fg, bg=bg, ul=ul)
			self.assertIs(cs.fg, fg)
			self.assertIs(cs.bg, bg)
			self.assertIs(cs.ul, ul)


if __name__ == '__main__':
	unittest.main()
