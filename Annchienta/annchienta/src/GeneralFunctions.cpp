/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "GeneralFunctions.h"

#include <cstdlib>
#include <cstdio>
#include <cmath>

namespace Annchienta
{
    float distance( float x1, float y1, float x2, float y2 )
    {
        return sqrt( squaredDistance(x1,y1,x2,y2) );
    }

    float squaredDistance( float x1, float y1, float x2, float y2 )
    {
        return ( square(x2-x1) + square(y2-y1) );
    }

};
