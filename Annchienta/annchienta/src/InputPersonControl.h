/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_INPUTPERSONCONTROL_H
#define ANNCHIENTA_INPUTPERSONCONTROL_H

#include "PersonControl.h"

namespace Annchienta
{
    class InputManager;
    class MathManager;

    class InputPersonControl: public PersonControl
    {
        protected:
            InputManager *inputManager;
            MathManager *mathManager;

        public:
            InputPersonControl( Person *person );
            virtual ~InputPersonControl();

            virtual void affect();
            void tryInteract();
    };
};

#endif
