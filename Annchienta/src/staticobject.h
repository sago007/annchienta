/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_STATICOBJECT_H
#define ANNCHIENTA_STATICOBJECT_H

#include "entity.h"

namespace Annchienta
{
    class StaticObject: public Entity
    {
        public:
            StaticObject();
            ~StaticObject();

            virtual void draw();
            virtual int getDepthSortY() const;
    };
};

#endif
