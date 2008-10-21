/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_AUXFUNC_H
#define ANNCHIENTA_AUXFUNC_H

namespace Annchienta
{
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
