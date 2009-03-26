#  Author: Roberto Cavada <cavada@fbk.eu>
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
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110, USA.
#
#  For more information on pygtkmvc see <http://pygtkmvc.sourceforge.net>
#  or email to the author Roberto Cavada <cavada@fbk.eu>.
#  Please report bugs to <cavada@fbk.eu>.

import new
import re
import types
import warnings

import gtkmvc.support.wrappers as wrappers
from gtkmvc.support.utils import get_function_from_source
from gtkmvc.support.log import logger


# ----------------------------------------------------------------------

OBS_TUPLE_NAME = "__observables__"

# old name, supported only for backward compatilibity, do not use it
# anymore in new code
PROPS_MAP_NAME = "__properties__" 

# This keeps the names of all observable properties (old and new)
ALL_OBS_SET = "__all_observables__"

# name of the variable that hold a property value
PROP_NAME = "_prop_%(prop_name)s"

# These are the names for property getter/setter methods that depend on property name
GET_PROP_NAME = "get_%(prop_name)s_value"
SET_PROP_NAME = "set_%(prop_name)s_value"

# There are the names for generic property getter/setter methods
GET_GENERIC_NAME = "get__value"
SET_GENERIC_NAME = "set__value"


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
    variable associated to the property. The setter simply sets its value.
    Programmers can override basic behaviour for getters or setters simply by
    defining their getters and setters (see at the names convention above).
    The customized function can lie everywhere in the user classes hierarchy.
    Every overridden function will not be generated by the metaclass.

    To supply your own methods is good for few methods, but can result in a
    very unconfortable way for many methods. In this case you can extend
    the meta-class, and override methods get_[gs]etter_source with your
    implementation (this can be probably made better).
    An example is provided in meta-class PropertyMetaVerbose below.
    """
    
    def __init__(cls, name, bases, _dict):
        """class constructor"""
        properties = {}
        type.__init__(cls, name, bases, _dict)
       
        # the set of all obs (it is calculated and stored below)
        obs = set()

        # processes now all names in __observables__ 
        for prop in type(cls).__get_observables_array__(cls):
            val = _dict.get(prop, None)
            if val is not None: type(cls).__create_prop_accessors__(cls, prop, val)
            elif type(getattr(cls, prop)) != property: type(cls).__create_prop_accessors__(cls, prop, val)
            obs.add(prop)
            pass

        # Generates code for all properties (but not for derived props):
        props = getattr(cls, PROPS_MAP_NAME, {})            
        if len(props) > 0: warnings.warn("In class %s.%s the use of attribute '%s' in models is deprecated. Use the tuple '%s' instead (see the manual)" %
                                         (cls.__module__, cls.__name__,  PROPS_MAP_NAME, OBS_TUPLE_NAME), 
                                         DeprecationWarning)

        # processes all names in __properties__ (deprecated, overloaded by __observables__)
        for prop in (x for x in props.iterkeys() if x not in obs):
            type(cls).__create_prop_accessors__(cls, prop, props[prop])
            obs.add(prop)
            pass
        
        # generates the list of _all_ properties available for this
        # class (also from bases)
        for base in bases: obs |= getattr(base, ALL_OBS_SET, set())
        setattr(cls, ALL_OBS_SET, obs)
        logger.debug("class %s.%s has observables: %s", cls.__module__, cls.__name__, obs)
        return


    def __get_observables_array__(cls):
        """Returns a set of strings by expanding wilcards found
        in class field __observables__. Expansion works only with
        names not prefixed with __"""
        import fnmatch
        res_set = set()

        not_found = []
        names = getattr(cls, OBS_TUPLE_NAME, tuple())
        if not isinstance(names, types.ListType) and not isinstance(names, types.TupleType):
            raise TypeError("In class %s.%s attribute '%s' must be a list or tuple" % (cls.__module__, cls.__name__, OBS_TUPLE_NAME))

        for name in names:
            if type(name) != types.StringType: raise TypeError("In class %s.%s attribute '%s' must contain only strings (found %s)" % 
                                                               (cls.__module__, cls.__name__, OBS_TUPLE_NAME, type(name)))
            if hasattr(cls, name):
                if getattr(cls, name) != types.MethodType: res_set.add(name)
                pass
            else: not_found.append(name)
            pass

        # now searches all possible matches for those that have not been found:
        for name in (x for x,v in cls.__dict__.iteritems()
                     if not x.startswith("__") 
                     and type(v) != types.MethodType
                     and x not in res_set):
            for pat, i in zip(not_found, range(len(not_found))):
                if fnmatch.fnmatch(name, pat): res_set.add(name)
                pass
            pass
        
        # finally, there might entries that have no corresponding
        # value, but there exist getter and setter methods. These
        # entries are valid only if they do not contain wilcards
        wilcards = frozenset("[]!*?")
        for name, nameset in zip(not_found, (frozenset(x) for x in not_found)):
            if (len(nameset & wilcards) == 0 and # no wilcards in the name
                ((hasattr(cls, GET_PROP_NAME % {'prop_name' : name}) and # has property getter and setter 
                  hasattr(cls, SET_PROP_NAME % {'prop_name' : name})) or
                 (hasattr(cls, GET_GENERIC_NAME) and # has generic getter and setter 
                  hasattr(cls, SET_GENERIC_NAME)))): res_set.add(name)
            else: # the observable was not found!
                logger.warning("In class %s.%s ignoring observable '%s' which has no corresponding attribute or custom getter/setter pair" % (cls.__module__, cls.__name__, name))
                pass
                               
            pass

        return res_set

        
    def __create_prop_accessors__(cls, prop_name, default_val):
        """Private method that creates getter and setter, and the
        corresponding property"""
        getter_name = "get_prop_%s" % prop_name
        setter_name = "set_prop_%s" % prop_name

        members_names = cls.__dict__.keys()

        # checks if accessors are already defined:
        if getter_name not in members_names:
            src = type(cls).get_getter_source(cls, getter_name, prop_name)
            func = get_function_from_source(src)
            setattr(cls, getter_name, func)
        else:
            logger.debug("Custom member '%s' overloads generated getter of property '%s'", 
                         getter_name, prop_name)
            pass

        if setter_name not in members_names:
            src = type(cls).get_setter_source(cls, setter_name, prop_name)
            func = get_function_from_source(src)
            setattr(cls, setter_name, func)
        else:
            logger.warning("Custom member '%s' overloads generated setter of property '%s'",
                           setter_name, prop_name)
            pass

        prop = property(getattr(cls, getter_name), getattr(cls, setter_name))
        setattr(cls, prop_name, prop)

        has_prop_variable = hasattr(cls, prop_name) or props.has_key(prop_name)
        if has_prop_variable:
            varname = PROP_NAME % {'prop_name' : prop_name}
            if not varname in members_names: cls.__create_property(varname, default_val)
            else: logger.warning("In class %s.%s automatic property builder found a possible clashing with attribute '%s'",
                                 cls.__module__, cls.__name__, varname)
            pass
        
        return

    def __create_property(cls, name, default_val):
        setattr(cls, name, cls.create_value(name, default_val))
        return

    def has_prop_attribute(cls, prop_name):
        """This methods returns True if there exists a class attribute
        for the given property. The attribute is searched locally
        only"""
        props = getattr(cls, PROPS_MAP_NAME, {})
        return cls.__dict__.has_key(prop_name) or props.has_key(prop_name)
    
    def check_value_change(cls, old, new):
        """Checks whether the value of the property changed in type
        or if the instance has been changed to a different instance.
        If true, a call to model._reset_property_notification should
        be called in order to re-register the new property instance
        or type"""
        return  type(old) != type(new) or \
               isinstance(old, wrappers.ObsWrapperBase) and (old != new)
    
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


    # ------------------------------------------------------------
    #               Services    
    # ------------------------------------------------------------

    # Override these:
    def get_getter_source(cls, getter_name, prop_name):
        """This must be overridden if you need a different
        implementation.  Simply the generated implementation returns
        the variable name given by PROP_NAME"""
        return "def %(getter_name)s(self): return " + PROP_NAME % \
          {'getter_name' : getter_name, 'prop_name' : prop_name}

    def get_setter_source(cls, setter_name, prop_name):
        """This must be overridden if you need a different implementation.
        Simply the generated implementation sets the variable _prop_name"""
        return "def %(setter_name)s(self, val):  self." + PROP_NAME + " = val" % \
          {'setter_name' : setter_name, 'prop_name' : prop_name}
       
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



class ObservablePropertyMeta (PropertyMeta):
  """Classes instantiated by this meta-class must provide a method named
  notify_property_change(self, prop_name, old, new)"""
  def __init__(cls, name, bases, dict):
    PropertyMeta.__init__(cls, name, bases, dict)
    return    

  def get_getter_source(cls, getter_name, prop_name):
      """This implementation returns the PROP_NAME value if there
      exists such property. If there exist a pair of methods
      __get_<prop_name>_value__ and __set_<prop_name>_value__ the
      value is taken from the getter. Otherwise if there exists the
      generic pair __get_value__ and __set_value__ the gettter is
      called. The getter method (specific or general) is called _only_
      if there exists no variable called PROP_NAME (see the user
      manual)"""

      has_prop_variable = cls.has_prop_attribute(prop_name)

      has_specific_getter = (
          hasattr(cls, GET_PROP_NAME % {'prop_name' : prop_name}) and # has property getter and setter 
          hasattr(cls, SET_PROP_NAME % {'prop_name' : prop_name}))

      has_general_getter = (
          hasattr(cls, GET_GENERIC_NAME) and # has generic getter and setter 
          hasattr(cls, SET_GENERIC_NAME))

      assert has_prop_variable or has_specific_getter or has_general_getter, "no var/methods for '%s'" % prop_name
      
      # when property variable is given, it overrides all getters
      if has_prop_variable:
          getter = "self." + PROP_NAME
          if has_specific_getter: logger.warning("In class %s.%s ignoring custom getter/setter pair for property '%s' as a corresponding attribute exists" % (cls.__module__, cls.__name__, prop_name))

      # specific getter ovverides the general one
      elif has_specific_getter: getter = "self." + GET_PROP_NAME + "()" 

      # generic getter
      else: getter = "self." + GET_GENERIC_NAME + "('%(prop_name)s')"

      # general getter ovverides the general one
      return ("def %(getter_name)s(self): return " + getter) % \
        {'getter_name' : getter_name, 'prop_name' : prop_name}
          
  
  def get_setter_source(cls, setter_name, prop_name):
      """The setter follows the rules of the getter. First search for
      property variable, then specific getter/seter pair methods, and
      finally the generic getter/setter pair (see the user manual)"""

      has_prop_variable = cls.has_prop_attribute(prop_name)

      has_specific_setter = (
          hasattr(cls, GET_PROP_NAME % {'prop_name' : prop_name}) and # has property getter and setter 
          hasattr(cls, SET_PROP_NAME % {'prop_name' : prop_name}))

      has_general_setter = (
          hasattr(cls, GET_GENERIC_NAME) and # has generic getter and setter 
          hasattr(cls, SET_GENERIC_NAME))

      assert has_prop_variable or has_specific_setter or has_general_setter

      if has_prop_variable:
          getter = "self._prop_%(prop_name)s"
          setter = "self._prop_%(prop_name)s = new"

      elif has_specific_setter:
          getter = "self." + GET_PROP_NAME + "()"
          setter = "self." + SET_PROP_NAME + "(new)"
          
      else:
          getter = "self." + GET_GENERIC_NAME + "('%(prop_name)s')"
          setter = "self." + SET_GENERIC_NAME + "('%(prop_name)s', new)"
          pass          
      
      return ("""def %(setter_name)s(self, val):
 old = """ + getter + """
 new = type(self).create_value('%(prop_name)s', val, self)
 """ + setter + """
 if type(self).check_value_change(old, new): self._reset_property_notification('%(prop_name)s')
 self.notify_property_value_change('%(prop_name)s', old, val)
 return
""") % {'setter_name':setter_name, 'prop_name':prop_name}


  pass #end of class
# ----------------------------------------------------------------------


class ObservablePropertyMetaMT (ObservablePropertyMeta):
  """This class provides multithreading support for accesing
  properties, through a locking mechanism. It is assumed a lock is
  owned by the class that uses it. A Lock object called _prop_lock
  is assumed to be a member of the using class. see for example class
  ModelMT"""
  def __init__(cls, name, bases, dict):
    ObservablePropertyMeta.__init__(cls, name, bases, dict)
    return 
    
  def get_setter_source(cls, setter_name, prop_name):
      """Setter for MT.""" 
      has_prop_variable = cls.has_prop_attribute(prop_name)

      has_specific_setter = (
          hasattr(cls, GET_PROP_NAME % {'prop_name' : name}) and # has property getter and setter 
          hasattr(cls, SET_PROP_NAME % {'prop_name' : name}))

      has_general_setter = (
          hasattr(cls, GET_GENERIC_NAME) and # has generic getter and setter 
          hasattr(cls, SET_GENERIC_NAME))

      assert has_prop_variable or has_specific_setter or has_general_setter

      if has_prop_variable:
          getter = "self._prop_%(prop_name)s"
          setter = "self._prop_%(prop_name)s = new"

      elif has_specific_setter:
          getter = "self." + GET_PROP_NAME + "()"
          setter = "self." + SET_PROP_NAME + "(new)"
          
      else:
          getter = "self." + GET_GENERIC_NAME + "('%(prop_name)s')"
          setter = "self." + SET_GENERIC_NAME + "('%(prop_name)s', new)"
          pass          
      
      return """def %(setter_name)s(self, val): 
 old = """ + getter + """
 new = type(self).create_value('%(prop_name)s', val, self)
 self._prop_lock.acquire()
 """ + setter + """
 self._prop_lock.release()
 if type(self).check_value_change(old, new): self._reset_property_notification('%(prop_name)s')
 self.notify_property_value_change('%(prop_name)s', old, val)
 return
""" % {'setter_name':setter_name, 'prop_name':prop_name}

  pass #end of class


try:
  from sqlobject import Col
  from sqlobject.inheritance import InheritableSQLObject
  from sqlobject.events import listen, RowUpdateSignal
  
  class ObservablePropertyMetaSQL (ObservablePropertyMeta, InheritableSQLObject.__metaclass__):
    """Classes instantiated by this meta-class must provide a method
    named notify_property_change(self, prop_name, old, new)"""

    def __init__(cls, name, bases, dict):
      InheritableSQLObject.__metaclass__.__init__(cls, name, bases, dict)
      ObservablePropertyMeta.__init__(cls, name, bases, dict)

      listen(cls.update_listener, cls, RowUpdateSignal)
      return    

    def __create_prop_accessors__(cls, prop_name, default_val):
      if not isinstance(default_val, Col):
        # this is not a SQLObject column (likely a normal
        # observable property)
        ObservablePropertyMeta.__create_prop_accessors__(cls, prop_name, default_val)
        pass
      return
    
    def update_listener(cls, instance, kwargs):
      pnames = type(cls).__get_observables_array__(cls)
      for k in kwargs:
        if k in pnames:
          _old = getattr(instance, k)
          _new = kwargs[k]
          instance.notify_property_value_change(k, _old, _new)
          pass
        pass
      return
    
    pass #end of class
except: pass
  
try:
  from gobject import GObjectMeta
  class ObservablePropertyGObjectMeta (ObservablePropertyMeta, GObjectMeta): pass
  class ObservablePropertyGObjectMetaMT (ObservablePropertyMetaMT, GObjectMeta): pass    
except:
  class ObservablePropertyGObjectMeta (ObservablePropertyMeta): pass
  class ObservablePropertyGObjectMetaMT (ObservablePropertyMetaMT): pass
  pass


