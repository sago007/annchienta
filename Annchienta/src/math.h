/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MATH_H
#define ANNCHIENTA_MATH_H

namespace Annchienta
{
    const int nearestPowerOfTwo( const int &input );

    /* return will be beneath maximum
     */
    const int randInt( const int &maximum );

    #ifndef SWIG
        template <class T>
        void swap( T &a, T &b )
        {
            T temp = a;
            a = b;
            b = temp;
        }
    #endif
};

#endif
