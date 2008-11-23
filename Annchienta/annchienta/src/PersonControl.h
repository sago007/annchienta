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

#ifndef ANNCHIENTA_PERSONCONTROL_H
#define ANNCHIENTA_PERSONCONTROL_H

namespace Annchienta
{
    class Person;

    /** This is an abstract class that controls a
     *  Person, meaning a facility to move a Person
     *  around the Map. See SamplePersonControl or
     *  InputPersonControl for implementations.
     */
    class PersonControl
    {
        protected:
            Person *person;

        public:

            /** Create a new PersonControl for a Person.
             *  \param person Person to control.
             */
            PersonControl( Person *person );

            /** Desturctor.
             */
            virtual ~PersonControl();

            /** Affect the Person to be controlled.
             */
            virtual void affect() = 0;
    };
};

#endif
