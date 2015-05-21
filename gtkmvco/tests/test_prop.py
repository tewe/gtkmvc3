"""
Test should print:
<class '__main__.AA'>
<unbound method AA.foo>
foo
"""

import _importer
from gtkmvc3.support.porting import add_metaclass

class Meta (type):

  def __new__(cls, name, bases, cls_dict):

    
    clsi = type.__new__(cls, name, bases, cls_dict)
    print(clsi)

    def foo(self): print("foo")
    setattr(clsi, "foo", foo)
    
    return clsi

  
  pass


@add_metaclass(Meta)
class AA (object):

  pass

print(AA.foo)
a = AA()
a.foo()
