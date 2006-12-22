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



# ----------------------------------------------------------------------
# In this example the use of observable properties is shown.  Here the
# property we want to observe is an already existing instance of a
# class that we do _not_ want to change to add support for the
# observer pattern.  Given that instance, we want the obsevers to be
# notified when one or more instance methods are executed, but without
# modifying the class instance itself. To reach our goal, as soon as the
# instance is stored into the model as an observable class, we 'wrap' it
# into a tuple of 3 elements, as shown in this simple example
# ----------------------------------------------------------------------

import _importer

from gtkmvc.model import Model
from gtkmvc.observer import Observer


# ----------------------------------------------------------------------
class ExistingClass (object):
    """This is an already existing class whose code is not intended to
    be changed. Instead, when instantiated into the model, it is
    declared in a particular manner, so that the model can recognise
    it and wrap it in order to monitor it"""
    
    def __init__(self): self.val = 0 

    def change(self): self.val += 1

    pass #end of class


# ----------------------------------------------------------------------
class MyModel (Model):

    __properties__ = {
        # the tuple contains: class name, instance and the list of
        # method names that we want to have observed:
        'obj' : (ExistingClass, ExistingClass(), ('change',)),
        }

    def __init__(self):
        Model.__init__(self)
        return    

    pass # end of class


# ----------------------------------------------------------------------
class MyObserver (Observer):
    def __init__(self, model):
        Observer.__init__(self, model)
        return

    # notification
    def property_obj_value_change(self, model, old, new):
        print "obj changed!"
        return

    def property_obj_before_change(self, model, instance, name, args, kwargs):
        print "obj before change!", instance, name, args, kwargs
        return

    def property_obj_after_change(self, model, instance, name, res,
                                  args, kwargs):
        print "obj after change!", instance, name, res, args, kwargs
        return

    pass # end of class


# Look at what happens to the observer
if __name__ == "__main__":
    m = MyModel()
    c = MyObserver(m)
    m.obj.change()
    pass

# ----------------------------------------------------------------------

