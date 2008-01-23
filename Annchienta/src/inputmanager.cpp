/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "inputmanager.h"

namespace Annchienta
{
    InputManager *inputManager;

    InputManager::InputManager()
    {
        /* Set reference to single-instance class.
         */
        inputManager = this;
    }

    InputManager::~InputManager()
    {
    }
    

    InputManager *getInputManager()
    {
        return inputManager;
    }

};
