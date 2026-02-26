#!/usr/bin/env python
from libTerm import examples as ex

modules = [
		ex.ex_arrowkeys,
		ex.ex_basic,
		ex.ex_menu_grid_big,
		ex.ex_menu_grid_simple,
		ex.ex_menu_list_simple,
		ex.ex_colors,
		ex.ex_printkeys,
		ex.ex_snake_automatic,
		ex.ex_snake_manual,
	]
from libTerm import Term
term = Term()
for module in modules:
	print(f"Running example: {module.__name__}")
	module.run(term)
