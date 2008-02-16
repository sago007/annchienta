/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "samplepersoncontrol.h"

#include <stdlib.h>
#include "person.h"

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
         * or wait a little.
         */
        if( walkTimeGiven <= 0 )
        {
            mx = my = 0;
            /* 50% walk on standing still.
             */
            if( rand()%2 )
            {
                int r = rand()%4;
                if( r==0 )
                    mx = -1;
                else
                    if( r==1 )
                        my = -1;
                    else
                        if( r==2 )
                            mx = 1;
                        else
                            my = 1;
            }

            walkTimeGiven = 10 + rand()%300;
        }
        /* Take a step in the moving direction.
         */
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
