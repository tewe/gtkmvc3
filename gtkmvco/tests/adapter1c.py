"""
Like adapter1.py but using old prop_write semantics.
"""
import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.basic import Adapter
from gtkmvc import observable

import gtk



class MyView (View):
    glade = "adapters.glade"
    top = "window1"


class MyModel (Model):
    en1 = 10.0
    __observables__ = ("en1",)


class MyCtrl (Controller):

    def on_button1_clicked(self, button):
        self.model.en1 += 1
        return
    
    pass

# ----------------------------------------------------------------------

def myerr(adapt, name, val):
    print "Error from", adapt, ":", name, ",", val
    adapt.update_widget()
    
m = MyModel()
v = MyView()
c = MyCtrl(m, v)

a1 = Adapter(m, "en1",
    prop_read=lambda v: v/2.0, prop_write=lambda v: v*2,
    value_error=myerr)
a1.connect_widget(v["entry1"])

a2 = Adapter(m, "en1")
a2.connect_widget(v["label1"], setter=lambda w,v: w.set_markup("<big><b>%.2f</b></big>" % v))

gtk.main()


