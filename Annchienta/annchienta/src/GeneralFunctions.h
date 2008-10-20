/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_AUXFUNC_H
#define ANNCHIENTA_AUXFUNC_H

namespace Annchienta
{
    const int nearestPowerOfTwo( const int &input );

    /* 0 <= return value <= maximum
     */
    const int randInt( const int &maximum );
    /* minimum <= return value <= maximum
     */
    const int randInt( const int &minimum, const int &maximum );
    /* 0 <= return value <= 1
     */
    const float randFloat();
    /* minimum <= return value <= maximum
     */
    const float randFloat( const float &minimum, const float &maximum );

    float distance( float x1, float y1, float x2, float y2 );
    float squaredDistance( float x1, float y1, float x2, float y2 );

    #ifndef SWIG
        #define square( a ) ((a)*(a))
        #define min( a, b ) ( (a)>(b)?(b):(a) )
        #define max( a, b ) ( (a)>(b)?(a):(b) )

        /** Returns the absolute value of a number.
         */
        #define absValue( a ) ( (a)>0? (a):-(a) )

    #endif
};

#endif
