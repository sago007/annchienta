/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_INPUTMANAGER_H
#define ANNCHIENTA_INPUTMANAGER_H

#include <SDL.h>

namespace Annchienta
{
    class InputManager
    {
        private:
            bool run;
            bool tickedKeys[ SDLK_LAST ];
            Uint8 *keyState;

        public:
            #ifndef SWIG
                InputManager();
                ~InputManager();
            #endif

            void update();

            bool running();
            void stop();

            bool keyDown( int );
            bool keyTicked( int );

    };

    InputManager *getInputManager();

};

#endif
