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

#include "SamplePersonControl.h"

#include <cstdlib>
#include "Person.h"
#include "InputManager.h"

namespace Annchienta
{

    SamplePersonControl::SamplePersonControl( Person *_person ): PersonControl(_person)
    {
        walkTimeGiven = 0;
        mx = my = 0;
    }

    SamplePersonControl::~SamplePersonControl()
    {
    }

    void SamplePersonControl::affect()
    {
        /* Stops walking and choose a new direction,
         * or wait a little. */
        if( walkTimeGiven <= 0 )
        {
            mx = my = 0;
            /* 50% chance to walk walk on standing still. */
            if( rand()%2 )
            {
                int r = rand()%4;
                if( r==0 )
                    mx = -1;
                else if( r==1 )
                    my = -1;
                else if( r==2 )
                    mx = 1;
                else
                    my = 1;
            }

            walkTimeGiven = 10 + rand()%100;
        }
        /* Take a step in the moving direction. if we can't
         * move in that direction, set walkTimeGiven to 0
         * so we stop moving and choose a different direction
         * on the next update. */
        else
        {
            bool result = person->move( mx, my );

            if( result )
                walkTimeGiven--;
            else
                walkTimeGiven = 0;
        }
    }

};
