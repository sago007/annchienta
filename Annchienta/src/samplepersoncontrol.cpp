/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "samplepersoncontrol.h"

#include "person.h"

namespace Annchienta
{

    SamplePersonControl::SamplePersonControl( Person *_person ): PersonControl(_person)
    {

    }

    SamplePersonControl::~SamplePersonControl()
    {
    }

    void SamplePersonControl::affect()
    {
        int x = 0, y = 0;

        person->move( x, y );
    }

};
