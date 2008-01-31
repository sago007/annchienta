/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_AUXFUNC_H
#define ANNCHIENTA_AUXFUNC_H

namespace Annchienta
{
    #define square( a ) ((a)*(a))

    const int nearestPowerOfTwo( const int &input );

    /* return will be beneath maximum
     */
    const int randInt( const int &maximum );

    bool isValidFile( const char *filename );

    float distance( float x2, float y2, float x2, float y2 );
    float squaredDistance( float x2, float y2, float x2, float y2 );

    #ifndef SWIG
        template <class T>
        void swap( T &a, T &b )
        {
            T temp = a;
            a = b;
            b = temp;
        }

        template <class T>
        void sort( T *array, int size )
        {

        }
    #endif
};

#endif
