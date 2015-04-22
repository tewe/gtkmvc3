#  Author: Roberto Cavada <roboogle@gmail.com>
#
#  Copyright (c) 2006 by Roberto Cavada
#
#  pygtkmvc is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  pygtkmvc is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <roboogle@gmail.com>.
#  Please report bugs to <roboogle@gmail.com>.


# This module is used only as a utility to import gtkmvc when not
# installed.

import time

from gi.repository import Gtk

# http://unpythonic.blogspot.com/2007/03/unit-testing-pygtk.html
def refresh_gui(delay=0):
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)
    time.sleep(delay)

if __name__ != "__main__":
    import os.path; import sys
    top_dir = os.path.dirname(os.path.abspath("."))
    # includes local version (for developers) if available
    if os.path.exists(os.path.join(top_dir, "gtkmvc")):
        sys.path = [top_dir] + sys.path
        pass
    import gtkmvc
    gtkmvc.require("1.99.0")
    import logging
    logging.getLogger("gtkmvc").setLevel(logging.DEBUG)
    pass
