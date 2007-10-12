import _importer
from gtkmvc import Model, Controller, View
from gtkmvc.adapters import StaticContainerAdapter

import gtk


class MyView (View):
    def __init__(self, ctrl):
        View.__init__(self, ctrl, "adapters.glade", "window4")
        return
    pass


class MyModel (Model):
    __properties__ = {
        'box' : { 'en4' : 0,
                  'lbl4' : 1,
                  'sb4' : 2 }
        }

    def __init__(self):
        Model.__init__(self)
        return
    pass

import random
class MyCtrl (Controller):
    def __init__(self, m):
        Controller.__init__(self, m)
        return

    def on_button4_clicked(self, button):
        k = random.choice(self.model.box.keys())
        self.model.box[k] += 1
        return
    
    pass

# ----------------------------------------------------------------------

m = MyModel()
c = MyCtrl(m)
v = MyView(c)

a1 = StaticContainerAdapter(m, "box")
a1.connect_widget(map(lambda x: v[x], "en4 lbl4 sb4".split()), 
                  setters = {'lbl4': lambda w, v: w.set_markup("<big>Val: <b>%d</b></big>" % v),})


gtk.main()



