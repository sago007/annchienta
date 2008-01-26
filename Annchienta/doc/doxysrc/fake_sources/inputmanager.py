
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
    #  pending events.
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

