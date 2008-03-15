
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


