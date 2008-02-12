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


class Engine(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Engine, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Engine, name)
    __repr__ = _swig_repr
    def write(*args): return _annchienta.Engine_write(*args)
    def __init__(self, *args): 
        this = _annchienta.new_Engine(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Engine
    __del__ = lambda self : None;
Engine_swigregister = _annchienta.Engine_swigregister
Engine_swigregister(Engine)

getEngine = _annchienta.getEngine
class VideoManager(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, VideoManager, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, VideoManager, name)
    __repr__ = _swig_repr
    def setVideoMode(*args): return _annchienta.VideoManager_setVideoMode(*args)
    def getScreenWidth(*args): return _annchienta.VideoManager_getScreenWidth(*args)
    def getScreenHeight(*args): return _annchienta.VideoManager_getScreenHeight(*args)
    def reset(*args): return _annchienta.VideoManager_reset(*args)
    def translate(*args): return _annchienta.VideoManager_translate(*args)
    def rotate(*args): return _annchienta.VideoManager_rotate(*args)
    def scale(*args): return _annchienta.VideoManager_scale(*args)
    def pushMatrix(*args): return _annchienta.VideoManager_pushMatrix(*args)
    def popMatrix(*args): return _annchienta.VideoManager_popMatrix(*args)
    def flip(*args): return _annchienta.VideoManager_flip(*args)
    def setColor(*args): return _annchienta.VideoManager_setColor(*args)
    def setAlpha(*args): return _annchienta.VideoManager_setAlpha(*args)
    def drawLine(*args): return _annchienta.VideoManager_drawLine(*args)
    def drawTriangle(*args): return _annchienta.VideoManager_drawTriangle(*args)
    def drawRectangle(*args): return _annchienta.VideoManager_drawRectangle(*args)
    def drawQuad(*args): return _annchienta.VideoManager_drawQuad(*args)
    def drawSurface(*args): return _annchienta.VideoManager_drawSurface(*args)
    def drawPattern(*args): return _annchienta.VideoManager_drawPattern(*args)
    def drawString(*args): return _annchienta.VideoManager_drawString(*args)
    def drawStringCentered(*args): return _annchienta.VideoManager_drawStringCentered(*args)
    def drawStringRight(*args): return _annchienta.VideoManager_drawStringRight(*args)
    def grabBuffer(*args): return _annchienta.VideoManager_grabBuffer(*args)
    def storeBuffer(*args): return _annchienta.VideoManager_storeBuffer(*args)
    def restoreBuffer(*args): return _annchienta.VideoManager_restoreBuffer(*args)
    def __init__(self, *args): 
        this = _annchienta.new_VideoManager(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_VideoManager
    __del__ = lambda self : None;
VideoManager_swigregister = _annchienta.VideoManager_swigregister
VideoManager_swigregister(VideoManager)

getVideoManager = _annchienta.getVideoManager
class InputManager(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, InputManager, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, InputManager, name)
    __repr__ = _swig_repr
    def update(*args): return _annchienta.InputManager_update(*args)
    def running(*args): return _annchienta.InputManager_running(*args)
    def stop(*args): return _annchienta.InputManager_stop(*args)
    def keyDown(*args): return _annchienta.InputManager_keyDown(*args)
    def keyTicked(*args): return _annchienta.InputManager_keyTicked(*args)
    def getMouseX(*args): return _annchienta.InputManager_getMouseX(*args)
    def getMouseY(*args): return _annchienta.InputManager_getMouseY(*args)
    def buttonDown(*args): return _annchienta.InputManager_buttonDown(*args)
    def buttonTicked(*args): return _annchienta.InputManager_buttonTicked(*args)
    def __init__(self, *args): 
        this = _annchienta.new_InputManager(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_InputManager
    __del__ = lambda self : None;
InputManager_swigregister = _annchienta.InputManager_swigregister
InputManager_swigregister(InputManager)

getInputManager = _annchienta.getInputManager
class MapManager(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, MapManager, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, MapManager, name)
    __repr__ = _swig_repr
    def setTileWidth(*args): return _annchienta.MapManager_setTileWidth(*args)
    def getTileWidth(*args): return _annchienta.MapManager_getTileWidth(*args)
    def setTileHeight(*args): return _annchienta.MapManager_setTileHeight(*args)
    def getTileHeight(*args): return _annchienta.MapManager_getTileHeight(*args)
    def setCameraX(*args): return _annchienta.MapManager_setCameraX(*args)
    def getCameraX(*args): return _annchienta.MapManager_getCameraX(*args)
    def setCameraY(*args): return _annchienta.MapManager_setCameraY(*args)
    def getCameraY(*args): return _annchienta.MapManager_getCameraY(*args)
    def cameraFollow(*args): return _annchienta.MapManager_cameraFollow(*args)
    def setUpdatesPerSecond(*args): return _annchienta.MapManager_setUpdatesPerSecond(*args)
    def setCurrentMap(*args): return _annchienta.MapManager_setCurrentMap(*args)
    def getCurrentMap(*args): return _annchienta.MapManager_getCurrentMap(*args)
    def setMaxAscentHeight(*args): return _annchienta.MapManager_setMaxAscentHeight(*args)
    def getMaxAscentHeight(*args): return _annchienta.MapManager_getMaxAscentHeight(*args)
    def setMaxDescentHeight(*args): return _annchienta.MapManager_setMaxDescentHeight(*args)
    def getMaxDescentHeight(*args): return _annchienta.MapManager_getMaxDescentHeight(*args)
    def run(*args): return _annchienta.MapManager_run(*args)
    def update(*args): return _annchienta.MapManager_update(*args)
    def renderFrame(*args): return _annchienta.MapManager_renderFrame(*args)
    def __init__(self, *args): 
        this = _annchienta.new_MapManager(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_MapManager
    __del__ = lambda self : None;
MapManager_swigregister = _annchienta.MapManager_swigregister
MapManager_swigregister(MapManager)

getMapManager = _annchienta.getMapManager
class AudioManager(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, AudioManager, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, AudioManager, name)
    __repr__ = _swig_repr
    def playSound(*args): return _annchienta.AudioManager_playSound(*args)
    def playMusic(*args): return _annchienta.AudioManager_playMusic(*args)
    def __init__(self, *args): 
        this = _annchienta.new_AudioManager(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_AudioManager
    __del__ = lambda self : None;
AudioManager_swigregister = _annchienta.AudioManager_swigregister
AudioManager_swigregister(AudioManager)

getAudioManager = _annchienta.getAudioManager
class CacheManager(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, CacheManager, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, CacheManager, name)
    __repr__ = _swig_repr
    def getSurface(*args): return _annchienta.CacheManager_getSurface(*args)
    def deleteSurface(*args): return _annchienta.CacheManager_deleteSurface(*args)
    def getMask(*args): return _annchienta.CacheManager_getMask(*args)
    def deleteMask(*args): return _annchienta.CacheManager_deleteMask(*args)
    def clear(*args): return _annchienta.CacheManager_clear(*args)
    def __init__(self, *args): 
        this = _annchienta.new_CacheManager(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_CacheManager
    __del__ = lambda self : None;
CacheManager_swigregister = _annchienta.CacheManager_swigregister
CacheManager_swigregister(CacheManager)

getCacheManager = _annchienta.getCacheManager
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
    def getWidth(*args): return _annchienta.Surface_getWidth(*args)
    def getHeight(*args): return _annchienta.Surface_getHeight(*args)
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
    def getHeight(*args): return _annchienta.Font_getHeight(*args)
    def getLineHeight(*args): return _annchienta.Font_getLineHeight(*args)
    def getStringWidth(*args): return _annchienta.Font_getStringWidth(*args)
Font_swigregister = _annchienta.Font_swigregister
Font_swigregister(Font)

class Sound(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Sound, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Sound, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_Sound(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Sound
    __del__ = lambda self : None;
Sound_swigregister = _annchienta.Sound_swigregister
Sound_swigregister(Sound)

class Layer(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Layer, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Layer, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_Layer(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Layer
    __del__ = lambda self : None;
    def setOpacity(*args): return _annchienta.Layer_setOpacity(*args)
    def getOpacity(*args): return _annchienta.Layer_getOpacity(*args)
    def update(*args): return _annchienta.Layer_update(*args)
    def draw(*args): return _annchienta.Layer_draw(*args)
    def depthSort(*args): return _annchienta.Layer_depthSort(*args)
    def addEntity(*args): return _annchienta.Layer_addEntity(*args)
Layer_swigregister = _annchienta.Layer_swigregister
Layer_swigregister(Layer)

class Map(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Map, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Map, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_Map(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Map
    __del__ = lambda self : None;
    def getCurrentLayer(*args): return _annchienta.Map_getCurrentLayer(*args)
    def setCurrentLayer(*args): return _annchienta.Map_setCurrentLayer(*args)
    def update(*args): return _annchienta.Map_update(*args)
    def draw(*args): return _annchienta.Map_draw(*args)
    def depthSort(*args): return _annchienta.Map_depthSort(*args)
Map_swigregister = _annchienta.Map_swigregister
Map_swigregister(Map)

TilePoint = _annchienta.TilePoint
IsometricPoint = _annchienta.IsometricPoint
MapPoint = _annchienta.MapPoint
ScreenPoint = _annchienta.ScreenPoint
class Point(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Point, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Point, name)
    __repr__ = _swig_repr
    __swig_setmethods__["x"] = _annchienta.Point_x_set
    __swig_getmethods__["x"] = _annchienta.Point_x_get
    if _newclass:x = _swig_property(_annchienta.Point_x_get, _annchienta.Point_x_set)
    __swig_setmethods__["y"] = _annchienta.Point_y_set
    __swig_getmethods__["y"] = _annchienta.Point_y_get
    if _newclass:y = _swig_property(_annchienta.Point_y_get, _annchienta.Point_y_set)
    __swig_setmethods__["z"] = _annchienta.Point_z_set
    __swig_getmethods__["z"] = _annchienta.Point_z_get
    if _newclass:z = _swig_property(_annchienta.Point_z_get, _annchienta.Point_z_set)
    def __init__(self, *args): 
        this = _annchienta.new_Point(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Point
    __del__ = lambda self : None;
    def getType(*args): return _annchienta.Point_getType(*args)
    def convert(*args): return _annchienta.Point_convert(*args)
    def to(*args): return _annchienta.Point_to(*args)
Point_swigregister = _annchienta.Point_swigregister
Point_swigregister(Point)

class Tile(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Tile, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Tile, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_Tile(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Tile
    __del__ = lambda self : None;
    def update(*args): return _annchienta.Tile_update(*args)
    def draw(*args): return _annchienta.Tile_draw(*args)
    def getDepthSortY(*args): return _annchienta.Tile_getDepthSortY(*args)
    def hasPoint(*args): return _annchienta.Tile_hasPoint(*args)
Tile_swigregister = _annchienta.Tile_swigregister
Tile_swigregister(Tile)

class TileSet(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, TileSet, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, TileSet, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_TileSet(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_TileSet
    __del__ = lambda self : None;
    def getSurface(*args): return _annchienta.TileSet_getSurface(*args)
    def getSideSurface(*args): return _annchienta.TileSet_getSideSurface(*args)
    def getMask(*args): return _annchienta.TileSet_getMask(*args)
TileSet_swigregister = _annchienta.TileSet_swigregister
TileSet_swigregister(TileSet)

class Mask(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Mask, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Mask, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _annchienta.new_Mask(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _annchienta.delete_Mask
    __del__ = lambda self : None;
    def getWidth(*args): return _annchienta.Mask_getWidth(*args)
    def getHeight(*args): return _annchienta.Mask_getHeight(*args)
    def collision(*args): return _annchienta.Mask_collision(*args)
Mask_swigregister = _annchienta.Mask_swigregister
Mask_swigregister(Mask)

SDLK_UNKNOWN = _annchienta.SDLK_UNKNOWN
SDLK_FIRST = _annchienta.SDLK_FIRST
SDLK_BACKSPACE = _annchienta.SDLK_BACKSPACE
SDLK_TAB = _annchienta.SDLK_TAB
SDLK_CLEAR = _annchienta.SDLK_CLEAR
SDLK_RETURN = _annchienta.SDLK_RETURN
SDLK_PAUSE = _annchienta.SDLK_PAUSE
SDLK_ESCAPE = _annchienta.SDLK_ESCAPE
SDLK_SPACE = _annchienta.SDLK_SPACE
SDLK_EXCLAIM = _annchienta.SDLK_EXCLAIM
SDLK_QUOTEDBL = _annchienta.SDLK_QUOTEDBL
SDLK_HASH = _annchienta.SDLK_HASH
SDLK_DOLLAR = _annchienta.SDLK_DOLLAR
SDLK_AMPERSAND = _annchienta.SDLK_AMPERSAND
SDLK_QUOTE = _annchienta.SDLK_QUOTE
SDLK_LEFTPAREN = _annchienta.SDLK_LEFTPAREN
SDLK_RIGHTPAREN = _annchienta.SDLK_RIGHTPAREN
SDLK_ASTERISK = _annchienta.SDLK_ASTERISK
SDLK_PLUS = _annchienta.SDLK_PLUS
SDLK_COMMA = _annchienta.SDLK_COMMA
SDLK_MINUS = _annchienta.SDLK_MINUS
SDLK_PERIOD = _annchienta.SDLK_PERIOD
SDLK_SLASH = _annchienta.SDLK_SLASH
SDLK_0 = _annchienta.SDLK_0
SDLK_1 = _annchienta.SDLK_1
SDLK_2 = _annchienta.SDLK_2
SDLK_3 = _annchienta.SDLK_3
SDLK_4 = _annchienta.SDLK_4
SDLK_5 = _annchienta.SDLK_5
SDLK_6 = _annchienta.SDLK_6
SDLK_7 = _annchienta.SDLK_7
SDLK_8 = _annchienta.SDLK_8
SDLK_9 = _annchienta.SDLK_9
SDLK_COLON = _annchienta.SDLK_COLON
SDLK_SEMICOLON = _annchienta.SDLK_SEMICOLON
SDLK_LESS = _annchienta.SDLK_LESS
SDLK_EQUALS = _annchienta.SDLK_EQUALS
SDLK_GREATER = _annchienta.SDLK_GREATER
SDLK_QUESTION = _annchienta.SDLK_QUESTION
SDLK_AT = _annchienta.SDLK_AT
SDLK_LEFTBRACKET = _annchienta.SDLK_LEFTBRACKET
SDLK_BACKSLASH = _annchienta.SDLK_BACKSLASH
SDLK_RIGHTBRACKET = _annchienta.SDLK_RIGHTBRACKET
SDLK_CARET = _annchienta.SDLK_CARET
SDLK_UNDERSCORE = _annchienta.SDLK_UNDERSCORE
SDLK_BACKQUOTE = _annchienta.SDLK_BACKQUOTE
SDLK_a = _annchienta.SDLK_a
SDLK_b = _annchienta.SDLK_b
SDLK_c = _annchienta.SDLK_c
SDLK_d = _annchienta.SDLK_d
SDLK_e = _annchienta.SDLK_e
SDLK_f = _annchienta.SDLK_f
SDLK_g = _annchienta.SDLK_g
SDLK_h = _annchienta.SDLK_h
SDLK_i = _annchienta.SDLK_i
SDLK_j = _annchienta.SDLK_j
SDLK_k = _annchienta.SDLK_k
SDLK_l = _annchienta.SDLK_l
SDLK_m = _annchienta.SDLK_m
SDLK_n = _annchienta.SDLK_n
SDLK_o = _annchienta.SDLK_o
SDLK_p = _annchienta.SDLK_p
SDLK_q = _annchienta.SDLK_q
SDLK_r = _annchienta.SDLK_r
SDLK_s = _annchienta.SDLK_s
SDLK_t = _annchienta.SDLK_t
SDLK_u = _annchienta.SDLK_u
SDLK_v = _annchienta.SDLK_v
SDLK_w = _annchienta.SDLK_w
SDLK_x = _annchienta.SDLK_x
SDLK_y = _annchienta.SDLK_y
SDLK_z = _annchienta.SDLK_z
SDLK_DELETE = _annchienta.SDLK_DELETE
SDLK_WORLD_0 = _annchienta.SDLK_WORLD_0
SDLK_WORLD_1 = _annchienta.SDLK_WORLD_1
SDLK_WORLD_2 = _annchienta.SDLK_WORLD_2
SDLK_WORLD_3 = _annchienta.SDLK_WORLD_3
SDLK_WORLD_4 = _annchienta.SDLK_WORLD_4
SDLK_WORLD_5 = _annchienta.SDLK_WORLD_5
SDLK_WORLD_6 = _annchienta.SDLK_WORLD_6
SDLK_WORLD_7 = _annchienta.SDLK_WORLD_7
SDLK_WORLD_8 = _annchienta.SDLK_WORLD_8
SDLK_WORLD_9 = _annchienta.SDLK_WORLD_9
SDLK_WORLD_10 = _annchienta.SDLK_WORLD_10
SDLK_WORLD_11 = _annchienta.SDLK_WORLD_11
SDLK_WORLD_12 = _annchienta.SDLK_WORLD_12
SDLK_WORLD_13 = _annchienta.SDLK_WORLD_13
SDLK_WORLD_14 = _annchienta.SDLK_WORLD_14
SDLK_WORLD_15 = _annchienta.SDLK_WORLD_15
SDLK_WORLD_16 = _annchienta.SDLK_WORLD_16
SDLK_WORLD_17 = _annchienta.SDLK_WORLD_17
SDLK_WORLD_18 = _annchienta.SDLK_WORLD_18
SDLK_WORLD_19 = _annchienta.SDLK_WORLD_19
SDLK_WORLD_20 = _annchienta.SDLK_WORLD_20
SDLK_WORLD_21 = _annchienta.SDLK_WORLD_21
SDLK_WORLD_22 = _annchienta.SDLK_WORLD_22
SDLK_WORLD_23 = _annchienta.SDLK_WORLD_23
SDLK_WORLD_24 = _annchienta.SDLK_WORLD_24
SDLK_WORLD_25 = _annchienta.SDLK_WORLD_25
SDLK_WORLD_26 = _annchienta.SDLK_WORLD_26
SDLK_WORLD_27 = _annchienta.SDLK_WORLD_27
SDLK_WORLD_28 = _annchienta.SDLK_WORLD_28
SDLK_WORLD_29 = _annchienta.SDLK_WORLD_29
SDLK_WORLD_30 = _annchienta.SDLK_WORLD_30
SDLK_WORLD_31 = _annchienta.SDLK_WORLD_31
SDLK_WORLD_32 = _annchienta.SDLK_WORLD_32
SDLK_WORLD_33 = _annchienta.SDLK_WORLD_33
SDLK_WORLD_34 = _annchienta.SDLK_WORLD_34
SDLK_WORLD_35 = _annchienta.SDLK_WORLD_35
SDLK_WORLD_36 = _annchienta.SDLK_WORLD_36
SDLK_WORLD_37 = _annchienta.SDLK_WORLD_37
SDLK_WORLD_38 = _annchienta.SDLK_WORLD_38
SDLK_WORLD_39 = _annchienta.SDLK_WORLD_39
SDLK_WORLD_40 = _annchienta.SDLK_WORLD_40
SDLK_WORLD_41 = _annchienta.SDLK_WORLD_41
SDLK_WORLD_42 = _annchienta.SDLK_WORLD_42
SDLK_WORLD_43 = _annchienta.SDLK_WORLD_43
SDLK_WORLD_44 = _annchienta.SDLK_WORLD_44
SDLK_WORLD_45 = _annchienta.SDLK_WORLD_45
SDLK_WORLD_46 = _annchienta.SDLK_WORLD_46
SDLK_WORLD_47 = _annchienta.SDLK_WORLD_47
SDLK_WORLD_48 = _annchienta.SDLK_WORLD_48
SDLK_WORLD_49 = _annchienta.SDLK_WORLD_49
SDLK_WORLD_50 = _annchienta.SDLK_WORLD_50
SDLK_WORLD_51 = _annchienta.SDLK_WORLD_51
SDLK_WORLD_52 = _annchienta.SDLK_WORLD_52
SDLK_WORLD_53 = _annchienta.SDLK_WORLD_53
SDLK_WORLD_54 = _annchienta.SDLK_WORLD_54
SDLK_WORLD_55 = _annchienta.SDLK_WORLD_55
SDLK_WORLD_56 = _annchienta.SDLK_WORLD_56
SDLK_WORLD_57 = _annchienta.SDLK_WORLD_57
SDLK_WORLD_58 = _annchienta.SDLK_WORLD_58
SDLK_WORLD_59 = _annchienta.SDLK_WORLD_59
SDLK_WORLD_60 = _annchienta.SDLK_WORLD_60
SDLK_WORLD_61 = _annchienta.SDLK_WORLD_61
SDLK_WORLD_62 = _annchienta.SDLK_WORLD_62
SDLK_WORLD_63 = _annchienta.SDLK_WORLD_63
SDLK_WORLD_64 = _annchienta.SDLK_WORLD_64
SDLK_WORLD_65 = _annchienta.SDLK_WORLD_65
SDLK_WORLD_66 = _annchienta.SDLK_WORLD_66
SDLK_WORLD_67 = _annchienta.SDLK_WORLD_67
SDLK_WORLD_68 = _annchienta.SDLK_WORLD_68
SDLK_WORLD_69 = _annchienta.SDLK_WORLD_69
SDLK_WORLD_70 = _annchienta.SDLK_WORLD_70
SDLK_WORLD_71 = _annchienta.SDLK_WORLD_71
SDLK_WORLD_72 = _annchienta.SDLK_WORLD_72
SDLK_WORLD_73 = _annchienta.SDLK_WORLD_73
SDLK_WORLD_74 = _annchienta.SDLK_WORLD_74
SDLK_WORLD_75 = _annchienta.SDLK_WORLD_75
SDLK_WORLD_76 = _annchienta.SDLK_WORLD_76
SDLK_WORLD_77 = _annchienta.SDLK_WORLD_77
SDLK_WORLD_78 = _annchienta.SDLK_WORLD_78
SDLK_WORLD_79 = _annchienta.SDLK_WORLD_79
SDLK_WORLD_80 = _annchienta.SDLK_WORLD_80
SDLK_WORLD_81 = _annchienta.SDLK_WORLD_81
SDLK_WORLD_82 = _annchienta.SDLK_WORLD_82
SDLK_WORLD_83 = _annchienta.SDLK_WORLD_83
SDLK_WORLD_84 = _annchienta.SDLK_WORLD_84
SDLK_WORLD_85 = _annchienta.SDLK_WORLD_85
SDLK_WORLD_86 = _annchienta.SDLK_WORLD_86
SDLK_WORLD_87 = _annchienta.SDLK_WORLD_87
SDLK_WORLD_88 = _annchienta.SDLK_WORLD_88
SDLK_WORLD_89 = _annchienta.SDLK_WORLD_89
SDLK_WORLD_90 = _annchienta.SDLK_WORLD_90
SDLK_WORLD_91 = _annchienta.SDLK_WORLD_91
SDLK_WORLD_92 = _annchienta.SDLK_WORLD_92
SDLK_WORLD_93 = _annchienta.SDLK_WORLD_93
SDLK_WORLD_94 = _annchienta.SDLK_WORLD_94
SDLK_WORLD_95 = _annchienta.SDLK_WORLD_95
SDLK_KP0 = _annchienta.SDLK_KP0
SDLK_KP1 = _annchienta.SDLK_KP1
SDLK_KP2 = _annchienta.SDLK_KP2
SDLK_KP3 = _annchienta.SDLK_KP3
SDLK_KP4 = _annchienta.SDLK_KP4
SDLK_KP5 = _annchienta.SDLK_KP5
SDLK_KP6 = _annchienta.SDLK_KP6
SDLK_KP7 = _annchienta.SDLK_KP7
SDLK_KP8 = _annchienta.SDLK_KP8
SDLK_KP9 = _annchienta.SDLK_KP9
SDLK_KP_PERIOD = _annchienta.SDLK_KP_PERIOD
SDLK_KP_DIVIDE = _annchienta.SDLK_KP_DIVIDE
SDLK_KP_MULTIPLY = _annchienta.SDLK_KP_MULTIPLY
SDLK_KP_MINUS = _annchienta.SDLK_KP_MINUS
SDLK_KP_PLUS = _annchienta.SDLK_KP_PLUS
SDLK_KP_ENTER = _annchienta.SDLK_KP_ENTER
SDLK_KP_EQUALS = _annchienta.SDLK_KP_EQUALS
SDLK_UP = _annchienta.SDLK_UP
SDLK_DOWN = _annchienta.SDLK_DOWN
SDLK_RIGHT = _annchienta.SDLK_RIGHT
SDLK_LEFT = _annchienta.SDLK_LEFT
SDLK_INSERT = _annchienta.SDLK_INSERT
SDLK_HOME = _annchienta.SDLK_HOME
SDLK_END = _annchienta.SDLK_END
SDLK_PAGEUP = _annchienta.SDLK_PAGEUP
SDLK_PAGEDOWN = _annchienta.SDLK_PAGEDOWN
SDLK_F1 = _annchienta.SDLK_F1
SDLK_F2 = _annchienta.SDLK_F2
SDLK_F3 = _annchienta.SDLK_F3
SDLK_F4 = _annchienta.SDLK_F4
SDLK_F5 = _annchienta.SDLK_F5
SDLK_F6 = _annchienta.SDLK_F6
SDLK_F7 = _annchienta.SDLK_F7
SDLK_F8 = _annchienta.SDLK_F8
SDLK_F9 = _annchienta.SDLK_F9
SDLK_F10 = _annchienta.SDLK_F10
SDLK_F11 = _annchienta.SDLK_F11
SDLK_F12 = _annchienta.SDLK_F12
SDLK_F13 = _annchienta.SDLK_F13
SDLK_F14 = _annchienta.SDLK_F14
SDLK_F15 = _annchienta.SDLK_F15
SDLK_NUMLOCK = _annchienta.SDLK_NUMLOCK
SDLK_CAPSLOCK = _annchienta.SDLK_CAPSLOCK
SDLK_SCROLLOCK = _annchienta.SDLK_SCROLLOCK
SDLK_RSHIFT = _annchienta.SDLK_RSHIFT
SDLK_LSHIFT = _annchienta.SDLK_LSHIFT
SDLK_RCTRL = _annchienta.SDLK_RCTRL
SDLK_LCTRL = _annchienta.SDLK_LCTRL
SDLK_RALT = _annchienta.SDLK_RALT
SDLK_LALT = _annchienta.SDLK_LALT
SDLK_RMETA = _annchienta.SDLK_RMETA
SDLK_LMETA = _annchienta.SDLK_LMETA
SDLK_LSUPER = _annchienta.SDLK_LSUPER
SDLK_RSUPER = _annchienta.SDLK_RSUPER
SDLK_MODE = _annchienta.SDLK_MODE
SDLK_COMPOSE = _annchienta.SDLK_COMPOSE
SDLK_HELP = _annchienta.SDLK_HELP
SDLK_PRINT = _annchienta.SDLK_PRINT
SDLK_SYSREQ = _annchienta.SDLK_SYSREQ
SDLK_BREAK = _annchienta.SDLK_BREAK
SDLK_MENU = _annchienta.SDLK_MENU
SDLK_POWER = _annchienta.SDLK_POWER
SDLK_EURO = _annchienta.SDLK_EURO
SDLK_UNDO = _annchienta.SDLK_UNDO
SDLK_LAST = _annchienta.SDLK_LAST
KMOD_NONE = _annchienta.KMOD_NONE
KMOD_LSHIFT = _annchienta.KMOD_LSHIFT
KMOD_RSHIFT = _annchienta.KMOD_RSHIFT
KMOD_LCTRL = _annchienta.KMOD_LCTRL
KMOD_RCTRL = _annchienta.KMOD_RCTRL
KMOD_LALT = _annchienta.KMOD_LALT
KMOD_RALT = _annchienta.KMOD_RALT
KMOD_LMETA = _annchienta.KMOD_LMETA
KMOD_RMETA = _annchienta.KMOD_RMETA
KMOD_NUM = _annchienta.KMOD_NUM
KMOD_CAPS = _annchienta.KMOD_CAPS
KMOD_MODE = _annchienta.KMOD_MODE
KMOD_RESERVED = _annchienta.KMOD_RESERVED


