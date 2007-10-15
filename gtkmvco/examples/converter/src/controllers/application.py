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
from converter import ConverterCtrl

from currencies import CurrenciesCtrl
from views.currencies import CurrenciesView

from about import AboutCtrl
from views.about import AboutView

from gtkmvc import Controller

import gtk

class ApplicationCtrl (Controller):
    """Controller of the top-level window (application)""" 

    def __init__(self, model):
        Controller.__init__(self, model)

        self.converter = ConverterCtrl(model.converter)
        return

    def register_view(self, view):
        """Creates treeview columns, and connect missing signals"""
        Controller.register_view(self, view)

        self.view.create_sub_views(self.converter)
        return

    def quit(self):
        gtk.main_quit()
        return
    
    # ----------------------------------------
    #               gtk signals
    # ----------------------------------------
    def on_tb_editor_clicked(self, tb):
        c = CurrenciesCtrl(self.model.currencies)
        v = CurrenciesView(c)
        return
        
    def on_tb_about_clicked(self, tb):        
        c = AboutCtrl(self.model.about)
        v = AboutView(c)
        v.run() # this runs in modal mode
        return

    def on_window_app_delete_event(self, w, e):
        self.quit()
        return True

    def on_tb_quit_clicked(self, bt): self.quit()
        
    
    # ----------------------------------------
    #          observable properties
    # ----------------------------------------
    
    pass # end of class

