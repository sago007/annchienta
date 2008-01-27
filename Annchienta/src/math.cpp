/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "math.h"

#include <stdlib.h>

namespace Annchienta
{
    const int nearestPowerOfTwo( const int &input )
    {
        int value = 1;
        while( value<input )
            value <<= 1;
        return value;
    }

    const int randInt( const int &max )
    {
        return rand()%max;
    }
};
