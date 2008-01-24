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

        /* The game is now running...
         */
        run = true;

        /* No keys are ticked by default.
         */
        for (int i(0); i < SDLK_LAST; i++)
            tickedKeys[i] = false;

        /* Get the keys address.
         */
        keyState = SDL_GetKeyState( NULL );
    }

    InputManager::~InputManager()
    {
    }

    void InputManager::update()
    {
        /* Reset the ticked keys.
         */
        for (int i(0); i < SDLK_LAST; i++)
            tickedKeys[i] = false;

        SDL_Event event;

        /* Process all events that happened since the last update.
         */
        while ( SDL_PollEvent( &event ) )
        {
            switch ( event.type )
            {
                case SDL_QUIT:
                    run = false;
                    break;

                case SDL_KEYDOWN:
                    tickedKeys[ event.key.keysym.sym ] = true;
                    break;

                default:
                    break;
            }
        }
    }

    bool InputManager::running()
    {
        return run;
    }

    void InputManager::stop()
    {
        run = false;
    }

    bool InputManager::keyDown( int keyCode )
    {
        return keyState[keyCode];
    }
    
    bool InputManager::keyTicked( int keyCode )
    {
        return tickedKeys[keyCode];
    }

    InputManager *getInputManager()
    {
        return inputManager;
    }

};
