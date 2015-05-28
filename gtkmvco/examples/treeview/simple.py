# PYGTKMVC TreeView contribution UI
# Copyright (C) 2011  Tobias Weber
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301, USA.

import gtk

import _importer
import gtkmvc3

class Person(gtkmvc3.Model):
    name = ''
    age = 0
    license = False
    __observables__ = ('name', 'age')

class Controller(gtkmvc3.Controller):
    handlers='class'

    def register_view(self, view):
        m = view['liststore1']

        p = Person()
        p.name = 'Joe'
        p.age = 15
        m.append([p])

        p = Person()
        p.name = 'Mary'
        p.age = 60
        p.license = True
        m.append([p])

    def register_adapters(self):
        self.setup_columns()

    def on_window1__delete_event(self, widget, event):
        gtk.main_quit()

m = gtkmvc3.Model()
v = gtkmvc3.View(builder='simple.ui')
c = Controller(m, v)

gtk.main()
