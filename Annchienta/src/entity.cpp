/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "entity.h"

#include <stdio.h>
#include <math.h>
#include "mapmanager.h"
#include "auxfunc.h"

namespace Annchienta
{

    void Entity::setDrawn( bool d )
    {
        drawn = d;
    }

    bool Entity::isDrawn() const
    {
        return drawn;
    }

};
