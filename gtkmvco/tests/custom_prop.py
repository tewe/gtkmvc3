## custom_prop.py
## Started on  Fri Dec  4 12:31:29 2009 Roberto Cavada
## Copyright (C) 2009 Roberto Cavada

# This file tests custom properties used in combination with adapters
# This was used to check bug fix made in rev.150

import _importer
from gtkmvc import Model, Controller, View

# ------------------------------------------------
class MyModel (Model):
    data_source = 10
    
    __observables__ = ("external",)

    def get_external_value(self):
        # gets the data from the external source
        return self.data_source
    
    def set_external_value(self, value):
        # sends the data to the external source
        self.data_source = value        
        return

    def change_data_source_value(self):
        """This simulates a change in the external data source. For
        the sake of simplicity, this is called from the controller
        when a button is pressed, but in a real example this got
        called by the external data source"""
        self.data_source += 1 # this changes the data (unfair, but simple!)
        self.external = self.data_source # here the property got in sync
        return
    
    pass # end of class

import gtk
# ------------------------------------------------
class MyView (View):    
    def __init__(self):
        View.__init__(self)
        self['win_top'] = gtk.Window()
        self['entry_external'] = gtk.Entry()
        self['button'] = gtk.Button("Click me to change the data source")
        box = gtk.VBox()
        for n in ('entry_external', 'button'): box.add(self[n])
        
        self['win_top'].add(box)
        self['win_top'].show_all()
    pass # end of class


# ------------------------------------------------
class MyCtrl (Controller):

    def register_view(self, view):
        view['button'].connect('clicked', self.on_button_clicked)
        view['win_top'].connect('delete-event', gtk.main_quit)
        return
    
    def register_adapters(self):
        self.adapt("external")
        return

    # properties
    def property_external_value_change(self, model, old, new):
        print "Changed from ", old, "to", new
        return
    
    # signals
    def on_button_clicked(self, button): self.model.change_data_source_value()
    pass # end of class



# ----------------------------------------------------------------------
# Test code
m = MyModel()
v = MyView()
c = MyCtrl(m, v, spurious=True)

gtk.main()