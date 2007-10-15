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

from converter import ConverterModel
from currencies import CurrenciesModel
from about import AboutModel

from gtkmvc import Model
import os.path

class ApplicationModel (Model):

    CURR_FILE = os.path.join(utils.globals.TOP_DIR, "currencies")

    def __init__(self):
        Model.__init__(self)

        self.currencies = CurrenciesModel()
        self.currencies.load(self.CURR_FILE)
        self.converter = ConverterModel(self.currencies)

        self.about = AboutModel()
        return
        
    
    pass # end of class