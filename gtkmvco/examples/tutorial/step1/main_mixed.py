# Author: Roberto Cavada, Copyright 2004
#
# This is free software; you can redistribute it and/or 
# modify it under the terms of the GNU Lesser General Public 
# License as published by the Free Software Foundation; either 
# version 2 of the License, or (at your option) any later version.
#
# These examples are distributed in the hope that they will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU 
# Lesser General Public License for more details.

import gtk
from model import MyModel
from ctrl_no_glade import MyControllerNoGlade
from ctrl_glade import MyController
from view_no_glade import MyViewNoGlade
from view_glade import MyView

m = MyModel()

v1 = MyViewNoGlade()
v2 =  MyView()

c1 = MyControllerNoGlade(m, v1)
c2 = MyController(m, v2)

gtk.main()
