/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
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
