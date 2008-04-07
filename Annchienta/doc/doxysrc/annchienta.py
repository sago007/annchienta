
## \brief Obtain the AudioManager instance.
#
#  Use this function to get access to the AudioManager
#  instance anywhere.
#
#  \return The global AudioManager instance.
def getAudioManager():
    pass


## \brief Handles audio tasks.
#
#  You use this class to perform audio tasks: play music, sounds, etc.
class AudioManager:

    ## \brief Plays a sound.
    #
    #  \param sound Sound to be played.
    def playSound( sound ):
        pass

    ## \brief Plays background some music.
    #
    #  When the given music is already playing, nothing happens. When
    #  other music is already playing, the other music is stopped.
    #
    #  \param filename Filename of the music file to be played.
    def playMusic( filename ):
        pass


## \brief Obtain the Engine instance.
#
#  Whenever you need access to the global Device instance, call this.
#  \return The global Device instance.
def getEngine():
    pass

## \brief Holds the Annchienta Engine.
#
#  This is the class that holds most other classes. To obtain it, call
#  annchienta.getDevice().
class Engine:

    ## \brief Writes a string to stdout.
    #
    #  When running under certain operating systems, the default
    #  Python 'print' function might be unsafe. That's why I
    #  recommend using this function in your scripts.
    #
    #  \param string The string to write.
    def write( string ):
        pass

    ## \brief Sets the window caption.
    #
    #  \param title The new title string.
    def setWindowTitle( title ):
        pass

    ## \brief Get time since initting.
    #
    #  \return The number of milliseconds that passed since the engine was initted.
    def getTicks():
        pass

    ## \brief Waits a specified time.
    #
    #  \param ms Milliseconds to wait.
    def delay( ms ):
        pass



## \brief Holds an Entity.
#
#  This class is an abstract superclass for Tiles,
#  StaticObjects and Persons.
class Entity:

    ## \brief Creates a new Entity.
    #
    #  \param name The name for this Entity.
    #  \return A newly created Entity.
    def __init__( name ):
        pass

    ## \brief Returns the Entity Type.
    #
    #  \return TileEntity, StaticObjectEntity or PersonEntity.
    def getEntityType():
        pass

    ## \brief Renders this Entity.
    #
    def draw():
        pass

    ## \brief Updates this Entity.
    #
    def update():
        pass

    ## \brief Gets the depth from the origin.
    #
    #  This is used to draw all entities in the correct
    #  order. Lower depth = farther from the screen
    #  \return The depth of this Entity.
    def getDepth():
        pass

    ## \brief The poition of the Entity Mask.
    #
    #  \return A Point referring to where the Mask of this entity should be drawn.
    def getMaskPosition():
        pass

    ## \brief Sets this Entity as drawn.
    #
    #  \param value When set to True, the Entity will not be drawn this render because the engine assumes it has been drawn already.
    def setDrawn( value ):
        pass

    ## \brief Checks if this Entity has been drawn.
    #
    #  \return True if this Entity was already drawn in the current render.
    def isDrawn():
        pass

    ## \brief Sets the name of this Entity.
    #
    #  \param name The new name for this Entity.
    def setName( name ):
        pass

    ## \brief Gets the name of this Entity.
    #
    #  \return The name of this Entity.
    def getName():
        pass

    ## \brief Sets the Layer of this Entity.
    #
    #  This happens automatically when using
    #  Layer.addEntity()
    #
    #  \param layer The new Layer to which this Entity should belong.
    def setLayer( layer ):
        pass

    ## \brief Gets a reference to the Layer of this Entity.
    #
    #  \return The Layer to which this Entity belongs.
    def getLayer():
        pass

## \brief Holds a font.
#
#  This class is used for holding text fonts.
#
#  \section font_example1 Example:
#  \code
# font = annchienta.Font( "font.ttf", 16 )
# videoManager.drawString( font, "Hello world!", 0, 0 )
#  \endcode
#
class Font:

    ## \brief Loads a new Font.
    #
    #  This function loads the font specified by filename,
    #  preferably a valid TrueType font.
    #
    #  \param filename The font to load.
    #  \param height The font height in pixels.
    #
    #  \return A new Font.
    #
    def __init__( filename, height ):
        pass

    ## \brief Gets the Font height.
    #
    #  \return The Font height.
    def getHeight():
        pass

    ## \brief Gets the Font line height.
    #
    #  The line height is basically the font height including
    #  a little extra space, so that you know where to start
    #  a new line.
    #
    #  \code
    # videoManager.drawString( font, "This is a line!", x, y )
    # y += font.getLineHeight()
    # videoManager.drawString( font, "This is another line.", x, y )
    #  \endcode
    #
    #  \return The Font line height.
    def getLineHeight():
        pass

    ## \brief Gets the width of a string.
    #
    #  This function calculates how wide the string will be in
    #  pixels, when it would be drawn. This is useful for aliging
    #  purposes:
    #
    #  \code
    # videoManager.drawString( font, "Boo!", 25, 400 - font.getStringWidth(boo) )
    #  \endcode
    #
    #  \return The string width.
    def getStringWidth( string ):
        pass


## \brief Obtain the InputManager instance.
#
#  Use this function to get access to the InputManager
#  instance anywhere.
#
#  \return The global InputManager instance.
def getInputManager():
    pass


## \brief Handles input tasks.
#
#  You use this class to get input information: Which keys
#  are pressed, if the exit button is pressed...
class InputManager:

    ## \brief Updates the input.
    #
    #  This function updates the input, eg. processes all
    #  pending events etc.
    def update():
        pass

    ## \brief Is the game still running?
    #
    #  This function should be called to ask whether the game
    #  is still running or not. This function will return false
    #  if, for example, the user closed the window.
    #
    #  \return A boolean value, True if the game is still running.
    def running():
        pass

    ## \brief Stops the game.
    #
    #  This function ensures running() will return False from now on.
    def stop():
        pass

    ## \brief Inspects a key.
    #
    #  \param keyCode The key keyCode. See \ref keycodes
    #  \return True is pressed, False if not.
    def keyDown( keyCode ):
        pass

    ## \brief Inspects a key.
    #
    #  This is a function like keyDown(), but slightly different:
    #  this function only returns true if the key was ticked since
    #  the last update. That means that, even when the user keeps
    #  pressing the key, this function will only return True the
    #  first time.
    #
    #  \param keyCode The key keyCode. See \ref keycodes
    #  \return True is ticked, False if not.
    def keyTicked( keyCode ):
        pass

    ## \brief Get mouse X.
    #
    #  \return The X coordinate of the mouse.
    def getMouseX():
        pass

    ## \brief Get mouse Y.
    #
    #  \return The Y coordinate of the mouse.
    def getMouseY():
        pass

    ## \brief Inspects a mouse button.
    #
    #  \param button The button code. 0 stands for left mouse button, 1 for right.
    #  \return True if that button is pressed, False is not.
    def buttonDown( button ):
        pass

    ## \brief Inspects a mouse button.
    #
    #  This is a function like buttonDown(), but slightly different:
    #  this function only returns true if the button was ticked since
    #  the last update. That means that, even when the user keeps
    #  pressing the button, this function will only return True the
    #  first time.
    #
    #  \param button The button code. 0 stands for left mouse button, 1 for right.
    #  \return True if that button is ticked, False is not.
    def buttonTicked( button ):
        pass

    ## \brief Sets the Person controlled by input.
    #
    #  If there already is a Person controlled by user input, the previous Person
    #  will be forgotten and this one will be used.
    #
    #  \param person The Person who will be controlled by user input from now onwards.
    def setInputControlledPerson( person ):
        pass

    ## \brief Gets the Person controlled by input.
    #
    #  \return A reference to the Person currently controlled by user input.
    def getInputControlledPerson():
        pass

    ## \brief Checks whether input is enabled for the Person or not.
    #
    #  \return True if the input for the Person is enabled, False if not.
    def personInputIsEnabled():
        pass

    ## \brief Sets whether input is enabled for the Person or not.
    #
    #  On certain moments, you will want to disable the input for the Person
    #  controlled by the user. As an example; you do not want the player to
    #  be able to just walk normally during a battle.
    #
    #  \param enabled True if you want input enabled, False if not.
    def setPersonInputEnabled( enabled ):
        pass

    ## \brief Sets the interact key.
    #
    #  \param keyCode The new interact key. See \ref keycodes
    def setInteractKey( keyCode ):
        pass

    ## \brief Gets the interact key.
    #
    #  \return The key code of the current interact key.
    def getInteractKey():
        pass


## \page keycodes Annchienta keyCodes.
#
#
#  \li annchienta.SDLK_UNKNOWN
#  \li annchienta.SDLK_FIRST
#  \li annchienta.SDLK_BACKSPACE
#  \li annchienta.SDLK_TAB
#  \li annchienta.SDLK_CLEAR
#  \li annchienta.SDLK_RETURN
#  \li annchienta.SDLK_PAUSE
#  \li annchienta.SDLK_ESCAPE
#  \li annchienta.SDLK_SPACE
#  \li annchienta.SDLK_EXCLAIM
#  \li annchienta.SDLK_QUOTEDBL
#  \li annchienta.SDLK_HASH
#  \li annchienta.SDLK_DOLLAR
#  \li annchienta.SDLK_AMPERSAND
#  \li annchienta.SDLK_QUOTE
#  \li annchienta.SDLK_LEFTPAREN
#  \li annchienta.SDLK_RIGHTPAREN
#  \li annchienta.SDLK_ASTERISK
#  \li annchienta.SDLK_PLUS
#  \li annchienta.SDLK_COMMA
#  \li annchienta.SDLK_MINUS
#  \li annchienta.SDLK_PERIOD
#  \li annchienta.SDLK_SLASH
#  \li annchienta.SDLK_0
#  \li annchienta.SDLK_1
#  \li annchienta.SDLK_2
#  \li annchienta.SDLK_3
#  \li annchienta.SDLK_4
#  \li annchienta.SDLK_5
#  \li annchienta.SDLK_6
#  \li annchienta.SDLK_7
#  \li annchienta.SDLK_8
#  \li annchienta.SDLK_9
#  \li annchienta.SDLK_COLON
#  \li annchienta.SDLK_SEMICOLON
#  \li annchienta.SDLK_LESS
#  \li annchienta.SDLK_EQUALS
#  \li annchienta.SDLK_GREATER
#  \li annchienta.SDLK_QUESTION
#  \li annchienta.SDLK_AT
#  \li annchienta.SDLK_LEFTBRACKET
#  \li annchienta.SDLK_BACKSLASH
#  \li annchienta.SDLK_RIGHTBRACKET
#  \li annchienta.SDLK_CARET
#  \li annchienta.SDLK_UNDERSCORE
#  \li annchienta.SDLK_BACKQUOTE
#  \li annchienta.SDLK_a
#  \li annchienta.SDLK_b
#  \li annchienta.SDLK_c
#  \li annchienta.SDLK_d
#  \li annchienta.SDLK_e
#  \li annchienta.SDLK_f
#  \li annchienta.SDLK_g
#  \li annchienta.SDLK_h
#  \li annchienta.SDLK_i
#  \li annchienta.SDLK_j
#  \li annchienta.SDLK_k
#  \li annchienta.SDLK_l
#  \li annchienta.SDLK_m
#  \li annchienta.SDLK_n
#  \li annchienta.SDLK_o
#  \li annchienta.SDLK_p
#  \li annchienta.SDLK_q
#  \li annchienta.SDLK_r
#  \li annchienta.SDLK_s
#  \li annchienta.SDLK_t
#  \li annchienta.SDLK_u
#  \li annchienta.SDLK_v
#  \li annchienta.SDLK_w
#  \li annchienta.SDLK_x
#  \li annchienta.SDLK_y
#  \li annchienta.SDLK_z
#  \li annchienta.SDLK_DELETE
#  \li annchienta.SDLK_WORLD_0
#  \li annchienta.SDLK_WORLD_1
#  \li annchienta.SDLK_WORLD_2
#  \li annchienta.SDLK_WORLD_3
#  \li annchienta.SDLK_WORLD_4
#  \li annchienta.SDLK_WORLD_5
#  \li annchienta.SDLK_WORLD_6
#  \li annchienta.SDLK_WORLD_7
#  \li annchienta.SDLK_WORLD_8
#  \li annchienta.SDLK_WORLD_9
#  \li annchienta.SDLK_WORLD_10
#  \li annchienta.SDLK_WORLD_11
#  \li annchienta.SDLK_WORLD_12
#  \li annchienta.SDLK_WORLD_13
#  \li annchienta.SDLK_WORLD_14
#  \li annchienta.SDLK_WORLD_15
#  \li annchienta.SDLK_WORLD_16
#  \li annchienta.SDLK_WORLD_17
#  \li annchienta.SDLK_WORLD_18
#  \li annchienta.SDLK_WORLD_19
#  \li annchienta.SDLK_WORLD_20
#  \li annchienta.SDLK_WORLD_21
#  \li annchienta.SDLK_WORLD_22
#  \li annchienta.SDLK_WORLD_23
#  \li annchienta.SDLK_WORLD_24
#  \li annchienta.SDLK_WORLD_25
#  \li annchienta.SDLK_WORLD_26
#  \li annchienta.SDLK_WORLD_27
#  \li annchienta.SDLK_WORLD_28
#  \li annchienta.SDLK_WORLD_29
#  \li annchienta.SDLK_WORLD_30
#  \li annchienta.SDLK_WORLD_31
#  \li annchienta.SDLK_WORLD_32
#  \li annchienta.SDLK_WORLD_33
#  \li annchienta.SDLK_WORLD_34
#  \li annchienta.SDLK_WORLD_35
#  \li annchienta.SDLK_WORLD_36
#  \li annchienta.SDLK_WORLD_37
#  \li annchienta.SDLK_WORLD_38
#  \li annchienta.SDLK_WORLD_39
#  \li annchienta.SDLK_WORLD_40
#  \li annchienta.SDLK_WORLD_41
#  \li annchienta.SDLK_WORLD_42
#  \li annchienta.SDLK_WORLD_43
#  \li annchienta.SDLK_WORLD_44
#  \li annchienta.SDLK_WORLD_45
#  \li annchienta.SDLK_WORLD_46
#  \li annchienta.SDLK_WORLD_47
#  \li annchienta.SDLK_WORLD_48
#  \li annchienta.SDLK_WORLD_49
#  \li annchienta.SDLK_WORLD_50
#  \li annchienta.SDLK_WORLD_51
#  \li annchienta.SDLK_WORLD_52
#  \li annchienta.SDLK_WORLD_53
#  \li annchienta.SDLK_WORLD_54
#  \li annchienta.SDLK_WORLD_55
#  \li annchienta.SDLK_WORLD_56
#  \li annchienta.SDLK_WORLD_57
#  \li annchienta.SDLK_WORLD_58
#  \li annchienta.SDLK_WORLD_59
#  \li annchienta.SDLK_WORLD_60
#  \li annchienta.SDLK_WORLD_61
#  \li annchienta.SDLK_WORLD_62
#  \li annchienta.SDLK_WORLD_63
#  \li annchienta.SDLK_WORLD_64
#  \li annchienta.SDLK_WORLD_65
#  \li annchienta.SDLK_WORLD_66
#  \li annchienta.SDLK_WORLD_67
#  \li annchienta.SDLK_WORLD_68
#  \li annchienta.SDLK_WORLD_69
#  \li annchienta.SDLK_WORLD_70
#  \li annchienta.SDLK_WORLD_71
#  \li annchienta.SDLK_WORLD_72
#  \li annchienta.SDLK_WORLD_73
#  \li annchienta.SDLK_WORLD_74
#  \li annchienta.SDLK_WORLD_75
#  \li annchienta.SDLK_WORLD_76
#  \li annchienta.SDLK_WORLD_77
#  \li annchienta.SDLK_WORLD_78
#  \li annchienta.SDLK_WORLD_79
#  \li annchienta.SDLK_WORLD_80
#  \li annchienta.SDLK_WORLD_81
#  \li annchienta.SDLK_WORLD_82
#  \li annchienta.SDLK_WORLD_83
#  \li annchienta.SDLK_WORLD_84
#  \li annchienta.SDLK_WORLD_85
#  \li annchienta.SDLK_WORLD_86
#  \li annchienta.SDLK_WORLD_87
#  \li annchienta.SDLK_WORLD_88
#  \li annchienta.SDLK_WORLD_89
#  \li annchienta.SDLK_WORLD_90
#  \li annchienta.SDLK_WORLD_91
#  \li annchienta.SDLK_WORLD_92
#  \li annchienta.SDLK_WORLD_93
#  \li annchienta.SDLK_WORLD_94
#  \li annchienta.SDLK_WORLD_95
#  \li annchienta.SDLK_KP0
#  \li annchienta.SDLK_KP1
#  \li annchienta.SDLK_KP2
#  \li annchienta.SDLK_KP3
#  \li annchienta.SDLK_KP4
#  \li annchienta.SDLK_KP5
#  \li annchienta.SDLK_KP6
#  \li annchienta.SDLK_KP7
#  \li annchienta.SDLK_KP8
#  \li annchienta.SDLK_KP9
#  \li annchienta.SDLK_KP_PERIOD
#  \li annchienta.SDLK_KP_DIVIDE
#  \li annchienta.SDLK_KP_MULTIPLY
#  \li annchienta.SDLK_KP_MINUS
#  \li annchienta.SDLK_KP_PLUS
#  \li annchienta.SDLK_KP_ENTER
#  \li annchienta.SDLK_KP_EQUALS
#  \li annchienta.SDLK_UP
#  \li annchienta.SDLK_DOWN
#  \li annchienta.SDLK_RIGHT
#  \li annchienta.SDLK_LEFT
#  \li annchienta.SDLK_INSERT
#  \li annchienta.SDLK_HOME
#  \li annchienta.SDLK_END
#  \li annchienta.SDLK_PAGEUP
#  \li annchienta.SDLK_PAGEDOWN
#  \li annchienta.SDLK_F1
#  \li annchienta.SDLK_F2
#  \li annchienta.SDLK_F3
#  \li annchienta.SDLK_F4
#  \li annchienta.SDLK_F5
#  \li annchienta.SDLK_F6
#  \li annchienta.SDLK_F7
#  \li annchienta.SDLK_F8
#  \li annchienta.SDLK_F9
#  \li annchienta.SDLK_F10
#  \li annchienta.SDLK_F11
#  \li annchienta.SDLK_F12
#  \li annchienta.SDLK_F13
#  \li annchienta.SDLK_F14
#  \li annchienta.SDLK_F15
#  \li annchienta.SDLK_NUMLOCK
#  \li annchienta.SDLK_CAPSLOCK
#  \li annchienta.SDLK_SCROLLOCK
#  \li annchienta.SDLK_RSHIFT
#  \li annchienta.SDLK_LSHIFT
#  \li annchienta.SDLK_RCTRL
#  \li annchienta.SDLK_LCTRL
#  \li annchienta.SDLK_RALT
#  \li annchienta.SDLK_LALT
#  \li annchienta.SDLK_RMETA
#  \li annchienta.SDLK_LMETA
#  \li annchienta.SDLK_LSUPER
#  \li annchienta.SDLK_RSUPER
#  \li annchienta.SDLK_MODE
#  \li annchienta.SDLK_COMPOSE
#  \li annchienta.SDLK_HELP
#  \li annchienta.SDLK_PRINT
#  \li annchienta.SDLK_SYSREQ
#  \li annchienta.SDLK_BREAK
#  \li annchienta.SDLK_MENU
#  \li annchienta.SDLK_POWER
#  \li annchienta.SDLK_EURO
#  \li annchienta.SDLK_UNDO
#  \li annchienta.SDLK_LAST
#  \li annchienta.KMOD_NONE
#  \li annchienta.KMOD_LSHIFT
#  \li annchienta.KMOD_RSHIFT
#  \li annchienta.KMOD_LCTRL
#  \li annchienta.KMOD_RCTRL
#  \li annchienta.KMOD_LALT
#  \li annchienta.KMOD_RALT
#  \li annchienta.KMOD_LMETA
#  \li annchienta.KMOD_RMETA
#  \li annchienta.KMOD_NUM
#  \li annchienta.KMOD_CAPS
#  \li annchienta.KMOD_MODE
#  \li annchienta.KMOD_RESERVED


## \brief Holds a Map layer.
#
#  This class is used for holding layers in a Map.
#
class Layer:

    ## \brief Sets the layer opacity.
    #
    #  Default is 255.
    #
    #  \param opacity A value [0-255].
    def setOpacity( opacity ):
        pass

    ## \brief Gets the opacity.
    #
    #  \return The opacity of this layer.
    def getOpacity():
        pass

    ## \brief Sets the Z offset.
    #
    #  \param z The new Z offset.
    def setZ( z ):
        pass

    ## \brief Gets Z offset.
    #
    #  \return The Z offset.
    def getZ():
        pass

    ## \brief Updates this Layer.
    #
    #  Updating a Layer also updates all entities in it.
    def update():
        pass

    ## \brief Draws this Layer to the screen.
    #
    def draw():
        pass

    ## \brief Draws this terrain to the screen.
    #
    #  Same as draw(), but only draws the tiles.
    def drawTerrain():
        pass

    ## \brief Sorts all entities in the Layer.
    #
    #  This function sorts all entities in the Layer, so they will be
    #  drawn in the correct order.
    def depthSort():
        pass

    ## \brief Adds an Entity.
    #
    #  \param entity Entity to be added to this Layer.
    def addEntity( entity ):
        pass

    ## \brief Adds an Area.
    #
    #  \param area Area to be added to this Layer.
    def addArea( area ):
        pass

    ## \brief Gets width of this Layer.
    #
    #  \return The width of this Layer.
    def getWidth():
        pass

    ## \brief Gets height of this Layer.
    #
    #  \return The height of this Layer.
    def getWidth():
        pass

    ## \brief Gets a reference to a Tile.
    #
    #  \param x X coordinate of the Tile to be obtained.
    #  \param y Y coordinate of the Tile to be obtained.
    #  \return The Tile at the given position.
    def getTile( x, y ):
        pass

    ## \brief Gets a reference to an object.
    #
    #  \param index The index of the object you want.
    #  \return The StaticObject or Person at the given index.
    def getObject( index ):
        pass

    ## \brief Gets a reference to an object.
    #
    #  \param name The name of the object you want.
    #  \return The StaticObject or Person at the given index.
    def getObject( name ):
        pass

    ## \brief Counts the number of objects.
    #
    #  \return The number of StaticObjects and Persons.
    def getNumberOfObjects():
        pass

    ## \brief Removes an object from this Layer.
    #
    #  \param object The StaticObject or Person to be removed.
    def removeObject( object ):
        pass

    ## \brief Gets a reference to an Area.
    #
    #  \param index The index of the Area you want.
    def getArea( index ):
        pass

## \package annchienta
#
#  \brief The main Annchienta package.
#
#  This package contains all Annchienta classes and functions.
#

## \mainpage Annchienta API Index
#
#  \section section1 What is Annchienta?
#
#  Simply put, Annchienta is an Isometric RPG Engine.
#
#  \section section2 Where do I start?
#
#  You could best start in \ref tutorial1
#


## \brief Holds a Map.
#
#  This class is used for holding maps.
#
class Map:

    ## \brief Loads a Map.
    #
    #  This function loads a Map from a valid Map XML file.
    #  \param filename XML file to be loaded.
    #  \return A new Map.
    def __init__( filename ):
        pass

    ## \brief Creates a new Map.
    #
    #  This function creates a new Map from scratch. This newly created
    #  Map will already contain one new Layer.
    #  \param width The width of the Map to be created.
    #  \param height The height of the Map to be created.
    #  \param tileSetDirectory The directory in which the tiles are situated.
    #  \return A new Map.
    def __init__( width, height, tileSetDirectory ):
        pass

    ## \brief Gets a reference to the current Layer.
    #
    #  \return The current Layer.
    def getCurrentLayer():
        pass

    ## \brief Gets a reference to a Layer in the Map.
    #
    #  \param index Index of the Layer to be returned.
    #  \return The Layer at the given index.
    def getLayer( index ):
        pass

    ## \brief Gets the index of the current Layer.
    #
    #  \return The index of the current Layer.
    def getCurrentLayerIndex():
        pass

    ## \brief Sets the current Layer.
    #
    #  \param index Index of the Layer to become the current Layer.
    def setCurrentLayer( index ):
        pass

    ## \brief Gets the number of Layers.
    #
    #  \return The number of Layers in this Map.
    def getNumberOfLayers():
        pass

    ## \brief Gets the filename.
    #
    #  \return The xml filename from which this map was loaded.
    def getFileName():
        pass

    ## \brief Gets the Map width.
    #
    #  \return The width of this Map.
    def getWidth():
        pass

    ## \brief Gets the Map height.
    #
    #  \return The height of this Map.
    def getHeight():
        pass

    ## \brief Adds a new Layer to this Map.
    #
    #  \param z The Z offset of the new Layer.
    def addNewLayer( z ):
        pass

    ## \brief Gets a reference to the TileSet used.
    #
    #  \return The TileSet used by this Map.
    def getTileSet():
        pass

    ## \brief Finds an object in this Map.
    #
    #  \param name The name of the Person or StaticObject to be found.
    #  \return The Person or StaticObject with the given name.
    def getObject( name ):
        pass

    ## \brief Adds an object.
    #
    #  The object given is added to the current Layer.
    #  \param object The Person or StaticObject to be added.
    def addObject( object ):
        pass

    ## \brief Removes an object.
    #
    #  \param object The Person or StaticObject to be removed.
    def removeObject( object ):
        pass

    ## \brief Updates the Map.
    #
    #  This function calls Layer.update() for all Layers.
    def update():
        pass

    ## \brief Draws the Map.
    #
    #  This function draws the Map and everything in it.
    def draw():
        pass

    ## \brief Draws the terrain.
    #
    #  This function only draws the tiles of this Map.
    def drawTerrain():
        pass

    ## \brief Sorts the Map.
    #
    #  This function calls Layer.depthSort() for all Layers.
    def depthSort():
        pass

    ## \brief Sorts the Layers.
    #
    #  This function performs a sort on all Layers to order them based
    #  on their Z offset so that they will be drawn in the correct
    #  order. This function does not modify Layer indexes used by
    #  getLayer().
    def sortLayers():
        pass


## \page mapfileformat The Map File Format.
#
#  \section mapfileformat_section1 Brief explanation.
#
#  To store maps, Annchienta uses an XML-based data format.
#


## \brief Obtain the MapManager instance.
#
#  Use this function to get access to the MapManager
#  instance anywhere.
#
#  \return The global MapManager instance.
def getMapManager():
    pass


## \brief Handles the map.
#
#  Use this class to control various maps and their
#  behaviour.
class MapManager:

    ## \brief Sets the tile width.
    #
    #  \param tileWidth The new tile width.
    def setTileWidth( tileWidth ):
        pass

    ## \brief Gets the tile width.
    #
    #  \return The current tile width.
    def getTileWidth():
        pass

    ## \brief Sets the tile height.
    #
    #  \param tileHeight The new tile height.
    def setTileHeight( tileHeight ):
        pass

    ## \brief Gets the tile height.
    #
    #  \return The current tile height.
    def getTileHeight():
        pass

    ## \brief Sets the camera X coordinate.
    #
    #  \param x The new camera X coordinate.
    def setCameraX( x ):
        pass

    ## \brief Gets the camera X coordinate.
    #
    #  \return The current camera X coordinate.
    def getCameraX():
        pass

    ## \brief Sets the camera Y coordinate.
    #
    #  \param y The new camera Y coordinate.
    def setCameraX( y ):
        pass

    ## \brief Gets the camera Y coordinate.
    #
    #  \return The current camera Y coordinate.
    def getCameraY():
        pass

    ## \brief Makes the camera follow an object.
    #
    #  \param object The StaticObject or Person the camera needs to follow.
    def cameraFollow( object ):
        pass

    ## \brief Makes the camera take a peek at an object.
    #
    #  The camera will only look at this object until update() is
    #  called. After that, it will look at the object set with
    #  cameraFollow( object ) again.
    #
    #  \param object The StaticObject or Person the camera needs to peek at.
    #  \param instantly If set to true, the camera will "jump" to the given target.
    def cameraPeekAt( object, instantly=False ):
        pass

    ## \brief Sets the number of updates per second.
    #
    #  While the framerate is variable, the number of updates per
    #  second is not. 60 should be a good value.
    #
    #  \param rate The update rate.
    def setUpdatesPerSecond( rate ):
        pass

    ## \brief Sets the current Map.
    #
    #  This should be called in the beginning of your game,
    #  and when the player moves to a next Map.
    #
    #  \code
    # myMap = annchienta.Map( "data/maps/mymap.xml" )
    # mapManager.setCurrentMap( myMap )
    #  \endcode
    #
    #  \param map The new Map to be set.
    def setCurrentMap( map ):
        pass

    ## \brief Get the current Map.
    #
    #  \return A reference to the current map.
    def getCurrentMap():
        pass

    ## \brief Sets maximum ascent height.
    #
    #  This variable is used for example when the player is trying
    #  to walk up a slope. He will only be able to do this when
    #  the difference between the height of the slope and his
    #  current height is smaller than the maximum ascent height.
    #  So simply put, the maximum height a player can climb in
    #  one step.
    #
    #  The maximum descent height is the same, but relevates to
    #  descending...
    #
    #  \param mah The new maximum ascent height.
    def setMaxAscentHeight( mah ):
        pass

    ## \brief Gets the maximum ascent height.
    #
    #  See setMaxAscentHeight() for an explanation of this
    #  variable.
    #
    #  \return The maximum ascent height.
    def getMaxAscentHeight():
        pass

    ## \brief Sets maximum descent height.
    #
    #  See setMaxAscentHeight() for an explanation of this
    #  variable.
    #
    #  \param mdh The new maximum descent height.
    def setMaxDescentHeight( mdh ):
        pass

    ## \brief Gets the maximum descent height.
    #
    #  See setMaxAscentHeight() for an explanation of this
    #  variable.
    #
    #  \return The maximum descent height.
    def getMaxDescentHeight():
        pass

    ## \brief Retrieve an object by it's name.
    #
    #  Search for a Person or StaticObject in the current
    #  Map and return it. If there are multiple objects with this
    #  name, the first one found will be returned.
    #
    #  \param name Name of the object to search for.
    #  \return The Person or StaticObject with the given name.
    def getObject( name ):
        pass

    ## \brief Set script to be executed every update.
    #
    #  \param script This script will be executed every update from now on.
    def setOnUpdateScript( script ):
        pass

    ## \brief Set code to be executed every update.
    #
    #  \param code This piece of code will be executed every update from now on.
    def setOnUpdateCode( code ):
        pass

    ## \brief Start the MapManager.
    #
    #  This basically runs the game. It does not return until
    #  the game is quitted or finished...
    def run():
        pass

    ## \brief Updates the current MapManager.
    #
    #  This function updates the MapManager a few times, or not
    #  even once, this all depends on the time passed since the
    #  last update. So use this function when you do not want to
    #  disturb the game's timing, else, use updateOnce().
    #
    #  \param updateInput Whether the input should be updates as well or not.
    def update( updateInput=True ):
        pass

    ## \brief Updates the current MapManager once.
    #
    #  See explanation with update(). You will probably want
    #  to call resync() after using this.
    #
    #  \param updateInput Whether the input should be updates as well or not.
    def updateOnce( updateInput=True ):
        pass

    ## \brief Renders a frame.
    #
    #  Draws the current Map with all the entities in it.
    def renderFrame():
        pass

    ## \brief Renders a terrain frame.
    #
    #  Same as renderFrame() but this function only renders tiles.
    def renderTerrain():
        pass

    ## \brief Resyncs update timing.
    #
    #  Use this function whenever you disturbed timing. After
    #  calling this, all timing should be back in order.
    def resync():
        pass




TilePoint, IsometricPoint, MapPoint, ScreenPoint = 0,1,2,3

## \brief Holds a Point.
#
#  This class is used for holding Points. You can
#  manipulate the coordinates directly.
#
#  \section point_example1 Example:
#  \code
# import annchienta
# point = annchienta.Point( annchienta.TilePoint, 2, 2 )
# point.x = point.y = point.z = 0
#  \endcode
#
#  Points consist of two or three Coordinates. There are
#  four types of points:
#
#  \section point_types Point Types
#
#  \li TilePoint
#
#  Has X, Y and Z coordinates and refers to a Tile. This
#  means that Point(TilePoint,4,4) would be in the same
#  place as the 4th Tile on the 4th row of Tiles.
#
#  \li IsometricPoint
#
#  Has X, Y and Z coordinates and refers to a Point in
#  an isometric axis system.
#
#  \li MapPoint
#
#  Has X, Y and Z coordinates. Refers to a Point in an ortho
#  axis system. The upper point of the Map translates as
#  (0,0,0). This means negative numbers will occur in the X
#  coordinate.
#
#  \li ScreenPoint
#
#  Has X and Y coordinates and refers to a Point on the
#  screen, where the top-left corner of the game window
#  is (0,0).
#
#  Converting between types is easy, just use the to() and
#  convert() functions.
#
#  \section point_example2 Example:
#  \code
# import annchienta
# videoManager = annchienta.getVideoManager()
# point = annchienta.Point( annchienta.TilePoint, 2, 2 )
# point.convert( ScreenPoint )
# videoManager.drawLine( point.x, point.y, 0, 0 )
#  \endcode
#
#
class Point:

    ## \brief Creates a new Point.
    #
    #  This function creates a new Point with the given
    #  parameters.
    #
    #  \param type Either TilePoint, IsometricPoint, MapPoint or ScreenPoint. See \ref point_types.
    #  \param x Initial X coordinate.
    #  \param y Initial Y coordinate.
    #  \param z Initial Z coordinate.
    #  \return A new Point.
    def __init__( type, x=0, y=0, z=0 ):
        pass

    ## \brief Returns the type of this Point.
    #
    #  \return The type. See \ref point_types.
    def getType():
        pass

    ## \brief Converts to another type.
    #
    #  \param type The new type for this Point. See \ref point_types.
    def convert( type ):
        pass

    ## \brief Creates another type.
    #
    #  \param type The type for the new Point. See \ref point_types.
    #  \return A new Point with the given type.
    def to( type ):
        pass

    ## \brief Checks if this point lies in a rectangle.
    #
    #  \param topLeft Top-left point of the rectangle.
    #  \param bottomRight Bottom-right point of the rectangle.
    #  \return True if this point is enclosed in the rectangle, False if not.
    def isEnclosedBy( topLeft, bottomRight ):
        pass




## \brief Holds a sound.
#
#  This class is used for holding digital sounds.
#
#  \section sound_example1 Example:
#  \code
# sound = annchienta.Sound( "scream.ogg" )
# soundManager = annchienta.getSoundManager()
# soundManager.playSound( sound )
#  \endcode
#
class Sound:

    ## \brief Loads a new Sound.
    #
    #  This function loads the sound specified by filename.
    #
    #  \param filename The sound to load.
    #
    #  \return A new Sound.
    #
    def __init__( filename ):
        pass



## \brief Holds a video surface.
#
#  This class is used for holding video surfaces. Surfaces are mostly images.
#
#  \section surface_example1 Example:
#  \code
# surface = annchienta.Surface( "image.png" )
# videoManager.drawSurface( surface, 0, 0 )
#  \endcode
#
class Surface:

    ## \brief Constructs a new Surface from an image.
    #
    #  The function loads the image specified by filename, which MUST be a valid PNG image.
    #
    #  \param filename The PNG image to load.
    #
    #  \return A new Surface.
    #
    def __init__( filename ):
        pass

    ## \brief Constructs a new empty Surface.
    #
    #  This function creates an empty Surface with the given size.
    #
    #  \param width The Surface width.
    #  \param height The Surface height.
    #  \param pixelSize Number of bytes per pixel. Best set to 3 or 4 for stability issues.
    #
    #  \return A new Surface.
    #
    def __init__( width, height, pixelSize=3 ):
        pass

    ## \brief Returns the Surface width.
    #
    #  \return The Surface width.
    def getWidth():
        pass

    ## \brief Returns the Surface height.
    #
    #  \return The Surface height.
    def getHeight():
        pass

    ## \brief Set scaling method to linear.
    def setLinearScaling():
        pass

    ## \brief Set scaling method to nearest.
    def setNearestScaling():
        pass


## \brief Holds a Tile.
#
#  This class is used to hold parts of the Layer, called tiles.
#  Because we are using an isometric system, tiles are usually
#  shaped like a rhombus.
#
#  A Tile consist of four Points, indexed like this:
#  \image html tile_pointindexes.png
#
#  A Tile has a top Surface and a Side Surface.
#  \image html tile_anatomy.png
#
class Tile(Entity):

    ## \brief Checks for collision with a Point.
    #
    #  \param point Point to be checked.
    #  \return True is the given Point lies on this Tile, False if not.
    def hasPoint( point ):
        pass

    ## \brief Checks if this Tile is a NullTile.
    #
    #  A NullTile is a Tile that should not be drawn at all
    #  because it is entirely transparent.
    #
    #  \return True is this Tile is a NullTile.
    def isNullTile():
        pass

    ## \brief Sets Z value of a Point.
    #
    #  \param index Index of the Point of which you want to change the Z coord.
    #  \param z The new Z value for that Point.
    def setZ( index, z ):
        pass

    ## \brief Gets Z value of a Point.
    #
    #  \param index Index of the Point of which you want to retrieve the Z coord.
    #  \return The Z value of that Point.
    def getZ( index ):
        pass

    ## \brief Gets a reference to a Point of this tile.
    #
    #  \param index Index of the Point you want to retrieve.
    #  \return One of the Points of this Tile.
    def getPointPointer( index ):
        pass

    ## \brief Sets the Top Surface.
    #
    #  \param index Index of the Point this Surface needs to be asigned to.
    #  \param surfaceNumber Number of the Surface you want in the TileSet being used in this Map.
    def setSurface( index, surfaceNumber ):
        pass

    ## \brief Sets the Side Surface.
    #
    #  \param sideSurfaceNumber Number of the SideSurface you want in the TileSet being used in this Map.
    def setSideSurface( sideSurfaceNumber ):
        pass

    ## \brief Sets Side Surface offset.
    #
    #  By default, the Side Surface starts at the top of the Tile
    #  goes until the ground. By setting this offset value, the
    #  Side Surface will only go to this offset instead of to the
    #  ground.
    #
    #  \param sso The new Side Surface offset.
    def setSideSurfaceOffset( sso ):
        pass

    ## \brief Gets the Surface.
    #
    #  \param index Index of the Point of which you want the Surface.
    #  \return Number of the Surface used.
    def getSurface( index ):
        pass

    ## \brief Gets the Side Surface.
    #
    #  \return Number of the SideSurface being used.
    def getSideSurface():
        pass

    ## \brief Gets the Side Surface offset.
    #
    #  \return The Side Surface offset. See setSideSurfaceOffset().
    def getSideSurfaceOffset():
        pass

    ## \brief Sets the ObstructionType.
    #
    #  There are three possibilities:
    #
    #  \li DefaultObstruction
    #
    #  The default value. Persons will be able to step on this Tile,
    #  depending on the height and the values set by
    #  MapManager.setMaxAscentHeight() and
    #  MapManager.setMaxDescentHeight().
    #
    #  \li NoObstruction
    #
    #  All Persons will always be able to step on this Tile,
    #  regardless of it's height.
    #
    #  \li FullObstruction
    #
    #  Nobody will ever be able to step on this Tile,
    #  regardless of it's height.
    #
    #  \param obstructionType The new ObstructionType for this tile.
    def setObstructionType( obstructionType ):
        pass

    ## \brief Gets the ObstructionType.
    #
    #  See setObstructionType().
    #
    #  \return The current ObstructionType.
    def getObstructionType():
        pass


## \brief Holds Tiles.
#
#  This class is used for holding a number of Tile
#  Surfaces.
#
class TileSet:

    ## \brief Loads a new TileSet.
    #
    #  This function will load all Tile Surfaces and Tile
    #  Side Surfaces in the given directory. The Tile
    #  Surfaces must be called directory/{n}.png and the Tile
    #  Side Surfaces directory/side{n}.png, where n is an
    #  integer starting at 1. The Surfaces with number 0 are
    #  automatically generated and entirely transparent. For
    #  an explanation about Surfaces and Side Surfaces, see the
    #  Tile documentation.
    #
    def __init__( directory ):
        pass

    ## \brief Gets a Surface.
    #
    #  \param number Number of the Surface you want to retrieve.
    #  \return The Surface with the given number.
    def getSurface( number ):
        pass

    ## \brief Gets a Side Surface.
    #
    #  \param number Number of the Side Surface you want to retrieve.
    #  \return The Side Surface with the given number.
    def getSideSurface( number ):
        pass

    ## \brief Gets the Tile Mask.
    #
    #  \return A Mask used for Tile collisions.
    def getMask():
        pass

    ## \brief Gets the directory.
    #
    #  \return The directory in which these Surfaces are situated.
    def getDirectory():
        pass


## \page tutorial1 Tutorial 1: The Basics.
#
#  \section t1_section1 Your first game.
#
#  Allright, let's dive in. Open up AnnEdit, create a new project, ...
#


## \brief Obtain the VideoManager instance.
#
#  Use this function to get access to the VideoManager
#  instance anywhere.
#
#  \return The global VideoManager instance.
def getVideoManager():
    pass


## \brief Handles video tasks.
#
#  This class is used for drawing, flipping and other video
#  operations. Remember to use setVideoMode() before actually
#  using it.
class VideoManager:

    ## \brief Sets the video mode.
    #
    #  Sets the current video mode as being screenWidth*screenHeight pixels.
    #
    #  \param screenWidth The screen width.
    #  \param screenHeight The screen height.
    #  \param title The window title.
    #  \param fullscreen Whether the window should be fullscreen'd or not.
    #
    def setVideoMode( screenWidth, screenHeight, title="Annchienta RPG Engine", fullscreen=False ):
        pass

    ## \brief Acquire the screen width.
    #
    #  \return The screen width.
    def getScreenWidth():
        pass

    ## \brief Acquire the screen height.
    #
    #  \return The screen height.
    def getScreenHeight():
        pass

    ## \brief Resets stuff.
    #
    #  This function resets the current matrix and color.
    def reset():
        pass

    ## \brief Translates the current matrix.
    #
    #  \param x X translate distance.
    #  \param y Y translate distance.
    def translate( x, y ):
        pass

    ## \brief Rotates the current matrix.
    #
    #  \param degrees Degrees to be rotated. Clockwise.
    def rotate( degrees ):
        pass

    ## \brief Scales the current matrix.
    #
    #  \param x X scale factor.
    #  \param y Y scale factor.
    def scale( x, y ):
        pass

    ## \brief Pushes the current matrix to the stack.
    #
    def pushMatrix():
        pass

    ## \brief Pops a matrix from the stack.
    #
    def popMatrix():
        pass

    ## \brief Begins the scene.
    #
    #  Clears and resets the scene.
    def begin():
        pass

    ## \brief Draws the buffer to the screen.
    #
    #  Ends the scene and draws the buffer to the screen.
    def end():
        pass

    ## \brief Sets the color.
    #
    #  Sets the color, used for surface, text and primitives drawing.
    #
    #  \param r Red Component. [0-255].
    #  \param g Green Component. [0-255].
    #  \param b Blue Component. [0-255].
    #  \param a Alpha Component. [0-255].
    def setColor( r, g, b, a ):
        pass

    ## \brief Sets the alpha component.
    #
    #  Sets the alpha component, used for surface, text and primitives drawing.
    #
    #  \param a Alpha Component. [0-255].
    def setAlpha( a ):
        pass

    ## \brief Draws a line.
    #
    #  \param x1 X coord of point 1.
    #  \param y1 Y coord of point 1.
    #  \param x2 X coord of point 2.
    #  \param y2 Y coord of point 2.
    def drawLine( x1, y1, x2, y2 ):
        pass

    ## \brief Draws a triangle.
    #
    #  \param x1 X coord of point 1.
    #  \param y1 Y coord of point 1.
    #  \param x2 X coord of point 2.
    #  \param y2 Y coord of point 2.
    #  \param x3 X coord of point 3.
    #  \param y3 Y coord of point 3.
    def drawTriangle( x1, y1, x2, y2, x3, y3 ):
        pass

    ## \brief Draws an axis-aligned rectangle.
    #
    #  \param x1 Top-left X coordinate.
    #  \param y1 Top-left Y coordinate.
    #  \param x2 Bottom-right X coordinate.
    #  \param y2 Bottom-right Y coordinate
    def drawRectangle( x1, y1, x2, y2 ):
        pass

    ## \brief Draws a quad.
    #
    #  You should pass the coordinates counterclockwise.
    #
    #  \param x1 X coordinate of point 1.
    #  \param y1 Y coordinate of point 1.
    #  \param x2 X coordinate of point 2.
    #  \param y2 Y coordinate of point 2.
    #  \param x3 X coordinate of point 3.
    #  \param y3 Y coordinate of point 3.
    #  \param x4 X coordinate of point 4.
    #  \param y4 Y coordinate of point 4.
    def drawQuad( x1, y1, x2, y2, x3, y3, x4, y4 ):
        pass

    ## \brief Draws a Surface.
    #
    #  \param surface Surface to be drawn.
    #  \param x Top-left X coord.
    #  \param y Top-left Y coord.
    def drawSurface( surface, x, y ):
        pass

    ## \brief Draws a part of a Surface.
    #
    #  \param surface Surface to be drawn.
    #  \param dx Destination X coordinate.
    #  \param dy Destination Y coordinate.
    #  \param sx1 Top-left X coordinate of source rectangle in the surface.
    #  \param sy1 Top-left Y coordinate of source rectangle in the surface.
    #  \param sx2 Bottom-right X coordinate of source rectangle in the surface.
    #  \param sy2 Bottom-right Y coordinate of source rectangle in the surface.
    def drawSurface( surface, dx, dy, sx1, sy1, sx2, sy2 ):
        pass

    ## \brief Draws a Surface as a pattern.
    #
    #  This function fills the rectangle defined by the function parameters
    #  with the given Surface.
    #
    #  \param surface Surface to be drawn.
    #  \param x1 Top-left X coordinate.
    #  \param y1 Top-left Y coordinate.
    #  \param x2 Bottom-right X coordinate.
    #  \param y2 Bottom-right Y coordinate.
    def drawPattern( surface, x1, y1, x2, y2 ):
        pass

    ## \brief Draws a string.
    #
    #  \param font Font to be used.
    #  \param string String to be drawn.
    #  \param x Upper-left X coord.
    #  \param y Upper-left Y coord.
    def drawString( font, string, x, y ):
        pass

    ## \brief Draws a string centered.
    #
    #  \param font Font to be used.
    #  \param string String to be drawn.
    #  \param x Middle X coord.
    #  \param y Upper-left Y coord.
    def drawStringCentered( font, string, x, y ):
        pass

    ## \brief Draws a string right-aligned.
    #
    #  \param font Font to be used.
    #  \param string String to be drawn.
    #  \param x Right X coord.
    #  \param y Upper Y coord.
    def drawStringRight( font, string, x, y ):
        pass

    ## \brief Grabs the buffer.
    #
    #  Copies the buffer to the given Surface.
    #  \attention The given Surface must be large enough to hold
    #  the buffer you are copying to it.
    #
    #  \param surface The destination Surface.
    def grabBuffer( surface ):
        pass

    ## \brief Grabs a part of the buffer.
    #
    #  Copies the rectangular area given by the coordinates to a given Surface.
    #
    #  \code
    # surface = annchienta.Surface( 50, 50 )
    # videoManager.grabBuffer( surface, 100, 100, 150, 150 )
    #  \endcode
    #
    #  \param surface The destination Surface.
    #  \param x1 Top-left X coord.
    #  \param y1 Top-left Y coord.
    #  \param x2 Bottom-right X coord.
    #  \param y2 Bottom-right Y coord.
    def grabBuffer( surface, x1, y1, x2, y2 ):
        pass

    ## \brief Saves the current buffer in a slot.
    #
    #  \param slot Number of the slot to be used. All implementations support at least slots [0-7].
    def storeBuffer( slot ):
        pass

    ## \brief Restores a buffer from a slot.
    #
    #  This basically draws a previsouly saved buffer to the screen.
    #
    #  \param slot Slot of the buffer which you would like to be restored.
    def restoreBuffer( slot ):
