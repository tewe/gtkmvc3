#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (C) 2007-2015 by Roberto Cavada
#
#  gtkmvc3 is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  gtkmvc3 is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on gtkmvc3 see <https://github.com/roboogle/gtkmvc3>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <https://github.com/roboogle/gtkmvc3/issues>
#  or to <roboogle@gmail.com>.

GTKMVC_DIR = None
PROGEN_DIR = None

# Tries to find gtkmvc3

import imp
import os
try: fn, path, desc = imp.find_module("gtkmvc3")
except ImportError: pass
if os.path.isdir(path):
    GTKMVC_DIR = path
    PROGEN_DIR = os.path.join(GTKMVC_DIR, "progen")
    pass