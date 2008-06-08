/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_INPUTPERSONCONTROL_H
#define ANNCHIENTA_INPUTPERSONCONTROL_H

#include "personcontrol.h"

namespace Annchienta
{
    class InputManager;

    class InputPersonControl: public PersonControl
    {
        protected:
            InputManager *inputManager;

        public:
            InputPersonControl( Person *person );
            virtual ~InputPersonControl();

            virtual void affect();
            void tryInteract();
    };
};

#endif
