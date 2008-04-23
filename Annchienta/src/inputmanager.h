/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_INPUTMANAGER_H
#define ANNCHIENTA_INPUTMANAGER_H

#include <SDL.h>

namespace Annchienta
{
    class Person;

    enum InputMode
    {
        CinematicMode=0,
        InteractiveMode=1
    };

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

            void update();

            bool running();
            void stop();

            bool keyDown( int ) const;
            bool keyTicked( int ) const;

            int getMouseX() const;
            int getMouseY() const;

            bool buttonDown( int ) const;
            bool buttonTicked( int ) const;

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
