# coding: utf8
import sys

# -------
# Pythons
# -------

# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)

# ---------
# Specifics
# ---------

if is_py2:
    from cStringIO import StringIO

    ord = ord
    chr = chr

    bytes = str
    str = unicode
    stdout = sys.stdout
    xrange = xrange


elif is_py3:
    from io import StringIO

    ord = lambda x: x
    chr = lambda x: bytes([x])

    str = str
    bytes = bytes
    stdout = sys.stdout.buffer
    xrange = range
