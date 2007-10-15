##  ===========================================================================
##  This file is part of Yoman, a notebook program.
##
##  Author: Baruch Even <baruch@ev-en.org>
##
##  Copyright (c) 2006 by Baruch Even
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 2 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program; if not, write to the Free Software Foundation, Inc.,
##  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
##  The author may be contact at his email <baruch@ev-en.org>.
##
##  ===========================================================================


from yomanlib.utils import _importer
from yomanlib.utils import globals

from gtkmvc import View
import gtk, gobject
import os

class BaseView(View):
	GLADE_FILE = 'glade/yoman.glade'

	def __init__(self, ctrl, parent_view=None, auto_register=True):
		View.__init__(self, ctrl, self.GLADE_FILE, self.TOP_WIDGET, parent_view, auto_register)

class AppView(BaseView):
	TOP_WIDGET = 'window_main'

	def __init__(self, ctrl):
		BaseView.__init__(self, ctrl, auto_register=False)

		self.main = MainView(ctrl.main)
		self['scrolledwindow_main'].add(self.main['treeview_main'])

		self.note = NoteView(ctrl.note)
		self['scrolledwindow_note'].add(self.note['viewport_note'])

		ctrl.register_view(self)
		pass

class BaseTreeView(BaseView):
	def __init__(self, ctrl):
		BaseView.__init__(self, ctrl, auto_register=False)
		treeview = self[self.TOP_WIDGET[0]]
		treeview.set_reorderable(True)

		cell = gtk.CellRendererText()
		tvcolumn = gtk.TreeViewColumn('Title', cell, text=0)
		treeview.append_column(tvcolumn)

		ctrl.register_view(self)
	
class MainView(BaseTreeView):
	TOP_WIDGET = ('treeview_main', 'main_popup')

class NoteView(BaseView):
	TOP_WIDGET = ('viewport_note', 'textview_note', 'entry_title')

	def __init__(self, ctrl):
		BaseView.__init__(self, ctrl)
		self['textview_note'].set_wrap_mode(gtk.WRAP_WORD)

class AppAboutView(BaseView):
	TOP_WIDGET = 'aboutdialog'

	def run(self):
		f = open(os.path.join(globals.TOPDIR, "LICENSE"), "r")
		self['aboutdialog'].set_license(f.read())
		f.close()

		w = self.get_top_widget()
		res = w.run()
		w.destroy()
		return res