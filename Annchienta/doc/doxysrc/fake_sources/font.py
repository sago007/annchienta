
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
