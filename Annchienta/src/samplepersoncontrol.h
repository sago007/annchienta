/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_SAMPLEPERSONCONTROL_H
#define ANNCHIENTA_SAMPLEPERSONCONTROL_H

#include "personcontrol.h"
#include "point.h"

namespace Annchienta
{
    class SamplePersonControl: public PersonControl
    {
        protected:
            Point *target;

        public:
            SamplePersonControl( Person *person );
            virtual ~SamplePersonControl();

            virtual void affect();
    };
};

#endif
