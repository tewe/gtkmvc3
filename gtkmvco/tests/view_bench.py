"""
Shows that memoization (no longer) makes sense.
"""

import timeit

import _importer
import gtkmvc3

N = 1000

build = gtkmvc3.View(builder='adapter19.ui')

names = []
# Cause auto widget extraction.
for name in build:
    names.append(name)

# Dictionary
t = timeit.Timer("""
for name in names:
    build[name]
    """, "from __main__ import build, names")
print(t.timeit(N)) # 0.004

# No caching
t = timeit.Timer("""
for name in names:
    build._builder.get_object(name)
    """, "from __main__ import build, names")
print(t.timeit(N))  # 0.012
