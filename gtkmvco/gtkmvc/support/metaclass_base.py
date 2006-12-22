#  Author: Roberto Cavada <cavada@irst.itc.it>
#
#  Copyright (c) 2005 by Roberto Cavada
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


import new
import re
import types

import gtkmvc.support.wrappers as wrappers


# ----------------------------------------------------------------------

VERBOSE_LEVEL = 5

class PropertyMeta (type):
    """This is a meta-class that provides auto-property support.
    The idea is to allow programmers to define some properties which
    will be automatically connected to auto-generated code which handles
    access to those properties.
    How can you use this meta-class?
    First, '__metaclass__ = PropertyMeta' must be class member of the class
    you want to make the automatic properties handling.
    Second, '__properties__' must be a map containing the properties names
    as keys, values will be initial values for properties.
    That's all: after the instantiation, your class will contain all properties
    you named inside '__properties__'. Each of them will be also associated
    to a couple of automatically-generated functions which get and set the
    property value inside a generated member variable.
    About names: suppose the property is called 'x'.  The generated variable
    (which keeps the real value of the property x) is called _prop_x.
    The getter is called get_prop_x(self), and the setter is called
    'set_prop_x(self, value)'.

    Customization:
    The base implementation of getter is to return the value stored in the
    variable associate to the property. The setter simply sets its value.
    Programmers can override basic behaviour for getters or setters simply by
    defining their getters and setters (see at the names convention above).
    The customized function can lie everywhere in the user classes hierarchy.
    Every overrided function will not be generated by the metaclass.

    To supply your own methods is good for few methods, but can result in a
    very unconfortable way for many methods. In this case you can extend
    the meta-class, and override methods get_[gs]etter_source with your
    implementation (this can be probably made better).
    An example is provided in meta-class PropertyMetaVerbose below.
    """
    
    def __init__(cls, name, bases, dict):
        """class constructor"""
        properties = {}
        type.__init__(cls, name, bases, dict)

        props = getattr(cls, '__properties__', {})
        setattr(cls, '__derived_properties__', {})
        der_props = getattr(cls, '__derived_properties__')
        
        # Calculates derived properties:
        for base in bases:
            maps = ( getattr(base, '__properties__', {}),
                     getattr(base, '__derived_properties__', {}) )
            for map in maps:
                for p in map.keys():
                    if not props.has_key(p) and not der_props.has_key(p):
                        der_props[p] = map[p]
                        pass
                    pass
                pass
            pass

        # Generates code for all properties (but not for derived props):
        props = getattr(cls, '__properties__', {})            
        for prop in props.keys():
            type(cls).__create_prop_accessors__(cls, prop, props[prop])
            pass

        return


    def __msg__(cls, msg, level):
        """if level is less or equal to VERBOSE_LEVEL, ths message will
        be printed"""
        if level <= VERBOSE_LEVEL: print msg
        return

    def __create_prop_accessors__(cls, prop_name, default_val):
        """Private method that creates getter and setter, and the
        corresponding property"""
        getter_name = "get_prop_%s" % prop_name
        setter_name = "set_prop_%s" % prop_name

        members_names = cls.__dict__.keys()

        # checks if accessors are already defined:
        if getter_name not in members_names:
            src = type(cls).get_getter_source(cls, getter_name, prop_name)
            code = type(cls).get_func_code_from_func_src(cls, src)
            type(cls).add_method_from_func_code(cls, getter_name, code)
        else:
            cls.__msg__("Warning: Custom member '%s' overloads generated accessor of property '%s'" \
                        % (getter_name, prop_name), 2)
            pass

        if setter_name not in members_names:
            src = type(cls).get_setter_source(cls, setter_name, prop_name)
            code = type(cls).get_func_code_from_func_src(cls, src)
            type(cls).add_method_from_func_code(cls, setter_name, code)
        else:
            cls.__msg__("Warning: Custom member '%s' overloads generated accessor of property '%s'" \
                        % (setter_name, prop_name), 2)
            pass

        prop = property(getattr(cls, getter_name), getattr(cls, setter_name))

        if prop_name in members_names:
            cls.__msg__("Warning: automatic property builder is overriding property %s in class %s" \
                        % (prop_name, cls.__name__), 2)
            pass
        setattr(cls, prop_name, prop)

        varname = "_prop_%s" % prop_name
        if not varname in members_names: cls.__create_property(varname, default_val)
        else: cls.__msg__("Warning: automatic property builder found a possible clashing for variable %s inside class %s" \
                          % (varname, cls.__name__), 2)
        return

    def __create_property(cls, name, default_val):
        setattr(cls, name, cls.create_value(name, default_val))
        return

    def create_value(cls, prop_name, val, model=None):
        """This is used to create a value to be assigned to a
        property. Depending on the type of the value, different values
        are created and returned. For example, for a list, a
        ListWrapper is created to wrap it, and returned for the
        assignment. model is different from model when the value is
        changed (a model exists). Otherwise, during property creation
        model is None"""

        if isinstance(val, tuple):
            # this might be a class instance to be wrapped
            if len(val) == 3 and \
               isinstance(val[1], val[0]) and \
               (isinstance(val[2], tuple) or isinstance(val[2], list)):
                res = wrappers.ObsUserClassWrapper(val[1], val[2])
                if model: res.__set_model__(model, prop_name)
                return res
            pass
        
        elif isinstance(val, list):
            res = wrappers.ObsListWrapper(val)
            if model: res.__set_model__(model, prop_name)
            return res

        elif isinstance(val, dict):            
            res = wrappers.ObsMapWrapper(val)
            if model: res.__set_model__(model, prop_name)
            return res

        return val
    
    # Services:
    def add_method_from_func_code(cls, meth_name, code):
        """Use this to add a code that is a new method for the class"""

        func = new.function(code, globals(), meth_name)
        meth = new.instancemethod(func, cls, cls.__name__)
        setattr(cls, meth_name, func)
        return
    
    def get_func_code_from_func_src(cls, source):
        """Public service that provided code object from function source"""
        m = re.compile("def\s+(\w+)\s*\(.*\):").match(source)
        if m is None: raise BadFuncSource(source)
        
        func_name = m.group(1)
        exec source
        code = eval("%s.func_code" % func_name)
        return code


    # Override these:
    def get_getter_source(cls, getter_name, prop_name):
        """This must be overrided if you need a different implementation.
        Simply the generated implementation returns the variable name
        _prop_name"""

        return "def %s(self): return self._prop_%s" % (getter_name, prop_name)
    
    def get_setter_source(cls, setter_name, prop_name):
        """This must be overrided if you need a different implementation.
        Simply the generated implementation sets the variable _prop_name"""
        return "def %s(self, val):  self._prop_%s = val" \
               % (setter_name, prop_name)
       
    pass # end of class
# ----------------------------------------------------------------------


# What follows underneath is a set of examples of usage

## class PropertyMetaVerbose (PropertyMeta):
##     """An example of customization"""
##     def get_getter_source(cls, getter_name, prop_name):
##         return "def %s(self): print 'Calling %s!'; return self._prop_%s" \
##                % (getter_name, getter_name, prop_name)

##     def get_setter_source(cls, setter_name, prop_name):
##         return "def %s(self, val):  print 'Calling %s!'; self._prop_%s = val;" \
##                % (setter_name, setter_name, prop_name)
##     pass #end of class
# ----------------------------------------------------------------------
    
## class User:
##     """An example of usage"""
##     __metaclass__ = PropertyMetaVerbose
##     __properties__ = {'x':10, 'y':20}

##     def __init__(self):
##         print self.x         # x is 10
##         self.x = self.y + 10 # x is now 30
##         return
##     pass
# ----------------------------------------------------------------------
