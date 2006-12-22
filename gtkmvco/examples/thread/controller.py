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


from gtkmvc import Controller
class MyController (Controller):
    """"""

    
    def __init__(self, m):
        Controller.__init__(self, m)
        return

    def register_view(self, view):
        Controller.register_view(self, view)

        readme = open("README","r").read()
        view.set_info(readme)
        view.set_label("Hello")
        return

    # gtk signals
    def on_button_clicked(self, button): self.model.run_test()

    def on_window_delete_event(self, window, event):
        import gtk
        gtk.main_quit()
        return True
    
    # observd properties
    def property_counter_value_change(self, model, old, new):
        self.view.set_label("%d" % new)
        return

    def property_busy_value_change(self, model, old, new):
        if new != old:
            self.view['button'].set_sensitive(not new)
            if not new: self.view['button'].grab_focus()
        return

    pass # end of class

