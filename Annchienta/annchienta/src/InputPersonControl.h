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

    /** A subclass of PersonControl. This class
     *  allows the player to control a player with
     *  input, like mouse movements.
     */
    class InputPersonControl: public PersonControl
    {
        protected:
            InputManager *inputManager;
            MathManager *mathManager;

        public:
            /** Create a new InputPersonControl instance for
             *  a given person.
             *  \param person Person to create the control for.
             */
            InputPersonControl( Person *person );

            /** Delete this PersonControl.
             */
            virtual ~InputPersonControl();

            /** Update the Person associated with this object.
             */
            virtual void affect();

            /** Internally used function that tries to have
             *  the associated Person interact with the world.
             */
            void tryInteract();
    };
};

#endif
