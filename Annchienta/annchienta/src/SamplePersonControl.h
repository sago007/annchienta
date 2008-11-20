/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_SAMPLEPERSONCONTROL_H
#define ANNCHIENTA_SAMPLEPERSONCONTROL_H

#include "PersonControl.h"
#include "Point.h"

namespace Annchienta
{
    /** A subclass of PersonControl. This class
     *  moves the controlled Person around a bit
     *  quite randomly. The Person walks around
     *  the field and evades other objects.
     */
    class SamplePersonControl: public PersonControl
    {
        protected:
            int walkTimeGiven;
            Point *target;
            int mx, my;

        public:

            /** Create a new SamplePersonControl instance
             *  for a given person.
             *  \param person Person to create the control for.
             */
            SamplePersonControl( Person *person );

            /** Delete this PersonControl.
             */
            virtual ~SamplePersonControl();

            /** Update the Person associated with this object.
             */
            virtual void affect();
    };
};

#endif
