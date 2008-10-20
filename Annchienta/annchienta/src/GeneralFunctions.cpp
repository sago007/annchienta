/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "GeneralFunctions.h"

#include <cstdlib>
#include <cstdio>
#include <cmath>

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
        return rand()%(max+1);
    }

    const int randInt( const int &min, const int &max )
    {
        return min+rand()%(max-min+1);
    }

    const float randFloat()
    {
        return rand()/(float(RAND_MAX)+1.0f);
    }

    const float randFloat( const float &min, const float &max )
    {
        return randFloat()*(max-min)+min;
    }

    float distance( float x1, float y1, float x2, float y2 )
    {
        return sqrt( squaredDistance(x1,y1,x2,y2) );
    }

    float squaredDistance( float x1, float y1, float x2, float y2 )
    {
        return ( square(x2-x1) + square(y2-y1) );
    }

};
