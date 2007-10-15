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


from models.currency import CurrencyModel
from currency import CurrencyCtrl

import utils._importer
from gtkmvc import Controller
import gtk

class CurrenciesCtrl (Controller):
    """Controller of 'Currencies' dialog.""" 

    def __init__(self, model):
        Controller.__init__(self, model)

        self.adding_model = None
        self.editing_model = None
        self.editing_iter = None
        return

    def register_view(self, view):
        """Creates treeview columns, and connect missing signals"""
        Controller.register_view(self, view)

        self.setup_columns()

        # connects tv messages
        tv = self.view['tv_categories']
        sel = tv.get_selection()
        sel.connect('changed', self.on_selection_changed)

        # connects other messages
        return

    def setup_columns(self):
        """Creates the treeview stuff"""
        tv = self.view['tv_categories']

        # sets the model
        tv.set_model(self.model)
        
        # creates the columns
        cell = gtk.CellRendererText()
        tvcol = gtk.TreeViewColumn('Name', cell)

        def cell_data_func(col, cell, mod, it):
            if mod[it][0]: cell.set_property('text', mod[it][0].name)
            return
        tvcol.set_cell_data_func(cell, cell_data_func)
        
        tv.append_column(tvcol)                
        return

    def show_curr_model_view(self, model, select):        
        """A currency has been added, or an existing curreny has been
        selected, and needs to be shown on the right side of the
        dialog"""
        c = CurrencyCtrl(model)
        self.view.add_currency_view(c, select)                
        return

    def unselect(self):
        """Unselects selected currency"""
        self.view['tv_categories'].get_selection().unselect_all()
        return

    def apply_modification(self):
        """Modifications on the right side need to be committed"""
        self.__changing_model = True

        if self.adding_model: self.model.add(self.adding_model)
        elif self.editing_model and self.editing_iter:
            # notifies the currencies model
            path = self.model.get_path(self.editing_iter)
            self.model.row_changed(path, self.editing_iter)            
            pass            
        
        self.view.remove_currency_view()
        self.adding_model = None
        self.editing_model = None
        self.editing_iter = None

        self.unselect()
        self.__changing_model = False
        return

    
    # ----------------------------------------
    #               gtk signals
    # ----------------------------------------
    def on_button_add_clicked(self, button):
        self.unselect()
        
        # creates a model, and shows it
        self.adding_model = CurrencyModel()
        self.show_curr_model_view(self.adding_model, True)
        self.editing_iter = None
        self.editing_model = None

        self.__changing_model = False
        return

    def on_button_delete_clicked(self, button):
        sel = self.view['tv_categories'].get_selection()
        m,i = sel.get_selected()

        self.__changing_model = True
        if i: m.remove(i)
        self.__changing_model = False
        return

    def on_selection_changed(self, sel):
        """The user changed selection"""
        m, self.editing_iter = sel.get_selected()

        if self.editing_iter:
            self.editing_model = m[self.editing_iter][0]
            self.show_curr_model_view(self.editing_model, False)
            
        else: self.view.remove_currency_view()
            
        return

    def on_dialog_currencies_response(self, dlg, id):
        if id == gtk.RESPONSE_APPLY:
            self.apply_modification()
            return

        self.unregister_model() # self unregisters itself
        if id == gtk.RESPONSE_CLOSE: self.view.destroy()
        return
        
    pass # end of class

