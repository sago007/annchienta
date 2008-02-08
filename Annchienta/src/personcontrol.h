/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_PERSONCONTROL_H
#define ANNCHIENTA_PERSONCONTROL_H

namespace Annchienta
{
    class Person;

    class PersonControl
    {
        protected:
            Person *person;

        public:
            PersonControl( Person *person );
            virtual ~PersonControl();

            virtual void affect() = 0;
    };
};

#endif
