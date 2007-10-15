import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters.basic import Adapter

import gtk



class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window1")
        return
    pass


class MyModel (Model):
    __properties__ = {
        'en1' : 10.0,
        }

    def __init__(self):
        Model.__init__(self)
        return
    pass


def myerr(adapt, name, val):
    print "Error from", adapt, ":", name, ",", val
    adapt.update_widget()

class MyCtrl (Controller):
    def __init__(self, m):
        Controller.__init__(self, m)
        return

    def register_adapters(self):
        a1 = Adapter(self.model, "en1",
                     prop_read=lambda v: v/2.0, prop_write=lambda v: v*2,
                     value_error=myerr)
        a1.connect_widget(self.view["entry1"])
        self.adapt(a1)

        a2 = Adapter(self.model, "en1")
        a2.connect_widget(self.view["label1"],
                          setter=lambda w,v: w.set_markup("<big><b>%.2f</b></big>" % v))
        self.adapt(a2)
        
        return
    
    def on_button1_clicked(self, button):
        self.model.en1 += 1
        return
    
    pass

# ----------------------------------------------------------------------

    
m = MyModel()
c = MyCtrl(m)
v = MyView(c)

gtk.main()


