
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
