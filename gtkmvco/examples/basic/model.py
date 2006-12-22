#  Author: Roberto Cavada <cavada@irst.itc.it>
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
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <cavada@irst.itc.it>.
#  Please report bugs to <cavada@irst.itc.it>.


import _importer
from gtkmvc import Model


class MyModel (Model):
    """Our model contains a numeric counter and a numeric value that
    holds the value that the counter must be assigned to when we the
    model is reset"""

    __properties__ = {
        'counter' : 0, 
        'reset_value' : 0,
        }

    def __init__(self):
        Model.__init__(self)
        return

    def reset(self): self.counter = self.reset_value

    pass # end of class
    
