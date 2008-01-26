
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

    ## \brief Draws the buffer to the screen.
    #
    #  First draws the buffer to the screen, then clears it.
    def flip():
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

    ## \brief Draws a Surface.
    #
    #  \param surface Surface to be drawn.
    #  \param x Upper-left X coord.
    #  \param y Upper-left Y coord.
    def drawSurface( surface, x, y ):
        pass

    ## \brief Draws a string.
    #
    #  \param font Font to be used.
    #  \param string String to be drawn.
    #  \param x Upper-left X coord.
    #  \param y Upper-left Y coord.
    def drawString( font, string, x, y ):
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


