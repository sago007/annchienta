/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_INPUTMANAGER_H
#define ANNCHIENTA_INPUTMANAGER_H

#include <SDL.h>
#include "point.h"

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
            bool run;
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
            bool running();

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

            void setInputControlledPerson( Person *person );
            Person *getInputControlledPerson() const;

            void setInputMode( InputMode mode );
            InputMode getInputMode() const;

            void setInteractKey( int );
            int getInteractKey() const;
    };

    InputManager *getInputManager();

};

#endif
