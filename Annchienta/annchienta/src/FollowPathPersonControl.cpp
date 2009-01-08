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

#include "FollowPathPersonControl.h"

#include "Person.h"

namespace Annchienta
{

    FollowPathPersonControl::FollowPathPersonControl( Person *_person ): PersonControl(_person)
    {
        targetPoint = 0;
    }

    FollowPathPersonControl::~FollowPathPersonControl()
    {
    }

    void FollowPathPersonControl::affect()
    {
        if( points.size() > 0 )
        {
            bool moved = person->stepTo( points[targetPoint] );

            if( !moved )
            {
                targetPoint = (targetPoint+1) % points.size();
            }
        }
    }

    void FollowPathPersonControl::addPoint( Point point )
    {
        points.push_back( point );
    }
};
