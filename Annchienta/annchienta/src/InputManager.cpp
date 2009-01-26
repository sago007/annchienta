/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "InputManager.h"
#include "LogManager.h"
#include "VideoManager.h"

namespace Annchienta
{
    InputManager *inputManager;

    InputManager::InputManager(): inputControlledPerson(0), inputMode(InteractiveMode)
    {
        /* Set reference to single-instance class.
         */
        inputManager = this;

        /* The engine is now uunning...
         */
        running = true;

        /* No keys are ticked by default.
         */
        for (int i(0); i < SDLK_LAST; i++)
            tickedKeys[i] = false;

        tickedButtons[0] = tickedButtons[1] = mouseState = mouseX = mouseY = 0;

        /* Get the keys address.
         */
        keyState = SDL_GetKeyState( NULL );

        /* We want key repeats.
         */
        SDL_EnableKeyRepeat( SDL_DEFAULT_REPEAT_DELAY, SDL_DEFAULT_REPEAT_INTERVAL );

        /* Set mouse */
        bool mouseMoved = true;
        interactKey = SDLK_SPACE;
        cancelKey = SDLK_ESCAPE;

        getLogManager()->message("Succesfully started InputManager.");
    }

    InputManager::~InputManager()
    {
        getLogManager()->message("Deleting InputManager...");
    }

    void InputManager::update()
    {
        /* Reset the ticked keys.
         */
        for (int i(0); i < SDLK_LAST; i++)
            tickedKeys[i] = false;

        tickedButtons[0] = tickedButtons[1] = 0;
        mouseMoved = false;

        SDL_Event event;

        /* Process all events that happened since the last update.
         */
        while ( SDL_PollEvent( &event ) )
        {
            switch ( event.type )
            {
                case SDL_QUIT:
                    running = false;
                    break;

                case SDL_KEYDOWN:
                    tickedKeys[ event.key.keysym.sym ] = true;
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
        int newMouseX, newMouseY;
        mouseState = SDL_GetMouseState( &newMouseX, &newMouseY );

        /* Take video scale into account. */
        int scale = getVideoManager()->getVideoScale();
        mouseX /= scale;
        mouseY /= scale;

        if( newMouseX != mouseX || newMouseY != mouseY )
            mouseMoved = true;
        mouseX = newMouseX;
        mouseY = newMouseY;

    }

    bool InputManager::isRunning()
    {
        return running;
    }

    void InputManager::stop()
    {
        running = false;
    }

    bool InputManager::keyDown( int keyCode ) const
    {
        return (bool)keyState[keyCode];
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

    bool InputManager::isMouseMoved() const
    {
        return mouseMoved;
    }

    bool InputManager::buttonDown( int buttonCode ) const
    {
        if( buttonCode==0 )
            buttonCode = SDL_BUTTON_LEFT;
        else
            buttonCode = SDL_BUTTON_RIGHT;

        return (bool)( mouseState & SDL_BUTTON( buttonCode ) );
    }

    bool InputManager::buttonTicked( int buttonCode ) const
    {
        return tickedButtons[ buttonCode ];
    }

    Point InputManager::getMousePoint() const
    {
        return Point( ScreenPoint, mouseX, mouseY );
    }

    bool InputManager::hover( int x1, int y1, int x2, int y2 ) const
    {
        return mouseX>=x1 && mouseX<x2 && mouseY>=y1 && mouseY<y2;
    }

    bool InputManager::clicked( int x1, int y1, int x2, int y2 ) const
    {
        return buttonTicked(0) && hover(x1,y1,x2,y2);
    }

    void InputManager::setInputControlledPerson( Person *person )
    {
        inputControlledPerson = person;
    }

    Person *InputManager::getInputControlledPerson() const
    {
        return inputControlledPerson;
    }

    void InputManager::setInputMode( InputMode mode )
    {
        inputMode = mode;
    }

    InputMode InputManager::getInputMode() const
    {
        return inputMode;
    }

    void InputManager::setInteractKey( int k )
    {
        interactKey = k;
    }

    int InputManager::getInteractKey() const
    {
        return interactKey;
    }

    void InputManager::setCancelKey( int k )
    {
        cancelKey = k;
    }

    int InputManager::getCancelKey() const
    {
        return cancelKey;
    }

    bool InputManager::interactKeyTicked() const
    {
        return keyTicked( interactKey );
    }

    bool InputManager::cancelKeyTicked() const
    {
        return keyTicked( cancelKey );
    }

    void InputManager::setMouseVisibility( bool value ) const
    {
        SDL_ShowCursor( (int)value );
    }

    InputManager *getInputManager()
    {
        return inputManager;
    }

};
