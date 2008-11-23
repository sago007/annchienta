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
