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

#ifndef ANNCHIENTA_FOLLOWPATHPERSONCONTROL_H
#define ANNCHIENTA_FOLLOWPATHPERSONCONTROL_H

#include "PersonControl.h"
#include "Point.h"
#include <vector>

namespace Annchienta
{
    class Person;

    /** This class moves a Person according to a 
     *  given path.
     */
    class FollowPathPersonControl: public PersonControl
    {
        protected:
            std::vector<Point> points;
            int targetPoint;

        public:

            /** Create a new PersonControl for a Person.
             *  \param person Person to control.
             */
            FollowPathPersonControl( Person *person );

            /** Desturctor.
             */
            virtual ~FollowPathPersonControl();

            /** Affect the Person to be controlled.
             */
            void affect();

            /** Add a Point to this path.
             *  \param point Point to be added.
             */
            void addPoint( Point point );
    };
};

#endif
