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

#ifndef ANNCHIENTA_INPUTMANAGER_H
#define ANNCHIENTA_INPUTMANAGER_H

#include <SDL.h>
#include "Point.h"

namespace Annchienta
{
    class Person;

    enum InputMode
    {
        /** No input is accepted from the user. Used for cinematic
         *  sequences.
         */
        CinematicMode=0,
        /** In this mode, the game accepts user input, which means
         *  the player can control his character.
         */
        InteractiveMode=1
    };

    /** Used to handle input tasks. Remember to call update() every
     *  frame.
     */
    class InputManager
    {
        private:
            bool running;
            bool tickedKeys[ SDLK_LAST ];
            bool tickedButtons[ 2 ];
            Uint8 *keyState;
            int mouseX, mouseY;
            Uint8 mouseState;
            bool supportMouse;
            Person *inputControlledPerson;
            InputMode inputMode;
            int interactKey;

        public:
            #ifndef SWIG
                InputManager();
                ~InputManager();
            #endif

            /** Updates all keys to their current state.
             */
            void update();

            /** This function should be called if you want to know
             *  if the engine is still running. This function will
             *  return false if the user closed the window.
             *  \return Whether the engine is still running or not.
             */
            bool isRunning();

            /** Stops the game. running() will return false from now
             *  on.
             */
            void stop();

            /** \param code See \ref keycodes
             *  \return Is the given key pressed down?
             */
            bool keyDown( int code ) const;

            /** This is a function like keyDown(), but slightly
             *  different: this function only returns true if the key
             *  was ticked since the last update. That means that,
             *  even when the user keeps pressing the key, this
             *  function will only return true the first time. Quite
             *  useful for menus and things like that.
             *  \param code See \ref keycodes
             *  \return Is the given key ticked?
             */
            bool keyTicked( int code ) const;

            /** \return Mouse X.
             */
            int getMouseX() const;

            /** \return Mouse Y.
             */
            int getMouseY() const;

            /** \param code 0 for left mouse button, 1 for right mouse button.
             *  \return Is the given button currently down?
             */
            bool buttonDown( int code ) const;

            /** \param code 0 for left mouse button, 1 for right mouse button.
             *  \return Is the given button ticked? (See keyTicked())
             */
            bool buttonTicked( int code ) const;

            /** \return A Point indicating mouse coordinates.
             */
            Point getMousePoint() const;

            /** Checks if the mouse is in a given rectangle.
             *  \param x1 Left X of that rectangle.
             *  \param y1 Top Y of that rectangle.
             *  \param x2 Right X of that rectangle.
             *  \param y2 Bottom Y of that rectangle.
             *  \return Is the mouse in that area?
             */
            bool hover( int x1, int y1, int x2, int y2 ) const;

            /** Checks if a certain area is clicked.
             *  \return Was this area clicked since the last update()?
             */
            bool clicked( int x1, int y1, int x2, int y2 ) const;

            /** Sets the Person controlled by input. If there already
             *  is one, the previous setting will be overwritten.
             *  \param person The Person to be controlled by the user.
             */
            void setInputControlledPerson( Person *person );

            /** \return Obtain the Person controlled by the user.
             */
            Person *getInputControlledPerson() const;

            /** \param mode See InputMode.
             */
            void setInputMode( InputMode mode );

            /** \return See InputMode.
             */
            InputMode getInputMode() const;

            /** Sets the default interact key.
             *  \param code See \ref keycodes
             */
            void setInteractKey( int code );

            /** \return The interact key. See \ref keycodes
             */
            int getInteractKey() const;

            /** \return Quick check for interact key.
             */
            bool interactKeyTicked() const;
            
            /** \param value Whether the mouse should be visible or not.
             */
            void setMouseVisibility( bool value ) const;
    };

    InputManager *getInputManager();

};

#endif
