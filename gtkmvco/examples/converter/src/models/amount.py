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
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author <cavada@irst.itc.it>.
#  Please report bugs to <cavada@irst.itc.it>.


import utils._importer
import utils.globals

from gtkmvc import Model


class AmountModel (Model):
    """This model represents a single pair of amount/currency. The
    model contains: the model of the available currencies, the amount,
    and an iterator within the currencies model pointing to the
    currently selected currency which the amount refer to."""

    __properties__ = {
        'amount' : 0.0,
        'iter'   : None,
        }

    def __init__(self, currencies_model):
        Model.__init__(self)
        
        self.currencies = currencies_model
        return

    def get_currency(self):
        if self.iter is None: return None
        return self.currencies[self.iter][0]
    
    pass # end of class