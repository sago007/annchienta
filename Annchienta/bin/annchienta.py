# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.31
#
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _annchienta
import new
new_instancemethod = new.instancemethod
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class Device(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Device, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Device, name)
    __repr__ = _swig_repr
    def setVideoMode(*args): return _annchienta.Device_setVideoMode(*args)
    def runPythonScript(*args): return _annchienta.Device_runPythonScript(*args)
    def _print(*args): return _annchienta.Device__print(*args)
    def __init__(self, *args): 
        this = _annchienta.new_Device(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Device
    __del__ = lambda self : None;
Device_swigregister = _annchienta.Device_swigregister
Device_swigregister(Device)

getDevice = _annchienta.getDevice
class Painter(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Painter, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Painter, name)
    __repr__ = _swig_repr
    def reset(*args): return _annchienta.Painter_reset(*args)
    def translate(*args): return _annchienta.Painter_translate(*args)
    def rotate(*args): return _annchienta.Painter_rotate(*args)
    def scale(*args): return _annchienta.Painter_scale(*args)
    def pushMatrix(*args): return _annchienta.Painter_pushMatrix(*args)
    def popMatrix(*args): return _annchienta.Painter_popMatrix(*args)
    def flip(*args): return _annchienta.Painter_flip(*args)
    def setColor(*args): return _annchienta.Painter_setColor(*args)
    def drawLine(*args): return _annchienta.Painter_drawLine(*args)
    def drawTriangle(*args): return _annchienta.Painter_drawTriangle(*args)
    def __init__(self, *args): 
        this = _annchienta.new_Painter(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Painter
    __del__ = lambda self : None;
Painter_swigregister = _annchienta.Painter_swigregister
Painter_swigregister(Painter)

getPainter = _annchienta.getPainter
class InputManager(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, InputManager, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, InputManager, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_InputManager(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_InputManager
    __del__ = lambda self : None;
InputManager_swigregister = _annchienta.InputManager_swigregister
InputManager_swigregister(InputManager)

getInputManager = _annchienta.getInputManager
class Surface(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Surface, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Surface, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_Surface(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Surface
    __del__ = lambda self : None;
    def draw(*args): return _annchienta.Surface_draw(*args)
Surface_swigregister = _annchienta.Surface_swigregister
Surface_swigregister(Surface)

class Font(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Font, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Font, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_Font(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Font
    __del__ = lambda self : None;
    def draw(*args): return _annchienta.Font_draw(*args)
Font_swigregister = _annchienta.Font_swigregister
Font_swigregister(Font)



