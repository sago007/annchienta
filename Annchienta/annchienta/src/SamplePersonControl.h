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
