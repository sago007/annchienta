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

        tickedButtons[0] = tickedButtons[1] = mouseState = mouseX = mouseY = 0;

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

        tickedButtons[0] = tickedButtons[1] = 0;

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
                    if( event.key.keysym.sym == SDLK_ESCAPE )
                        run = false;
                    break;

                case SDL_MOUSEBUTTONDOWN:
                    if( event.button.button == SDL_BUTTON_LEFT )
                        tickedButtons[0] = true;
                    if( event.button.button == SDL_BUTTON_RIGHT )
                        tickedButtons[1] = true;
                    break;

                default:
                    break;
            }
        }

        /* Take a little look at the mouse.
         */
        mouseState = SDL_GetMouseState( &mouseX, &mouseY );

    }

    bool InputManager::running()
    {
        return run;
    }

    void InputManager::stop()
    {
        run = false;
    }

    bool InputManager::keyDown( int keyCode ) const
    {
        return keyState[keyCode];
    }
    
    bool InputManager::keyTicked( int keyCode ) const
    {
        return tickedKeys[keyCode];
    }

    int InputManager::getMouseX() const
    {
        return mouseX;
    }

    int InputManager::getMouseY() const
    {
        return mouseY;
    }

    bool InputManager::buttonDown( int buttonCode ) const
    {
        if( buttonCode==0 )
            buttonCode = SDL_BUTTON_LEFT;
        else
            buttonCode = SDL_BUTTON_RIGHT;

        return ( mouseState & SDL_BUTTON( buttonCode ) );
    }

    bool InputManager::buttonTicked( int buttonCode ) const
    {
        return tickedButtons[ buttonCode ];
    }

    InputManager *getInputManager()
    {
        return inputManager;
    }

};
