
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
