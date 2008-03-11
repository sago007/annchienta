
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

