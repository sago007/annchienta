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

    bool isValidFile( const char *filename );

    float distance( float x1, float y1, float x2, float y2 );
    float squaredDistance( float x1, float y1, float x2, float y2 );

    void copyFile( const char *src, const char *dst );

    int strcmpCaseInsensitive( const char *str1, const char *str2 );

    #ifndef SWIG
        template <class T>
        void swap( T &a, T &b )
        {
            T temp = a;
            a = b;
            b = temp;
        }

        #define square( a ) ((a)*(a))
        #define min( a, b ) ( (a)>(b)?(b):(a) )
        #define max( a, b ) ( (a)>(b)?(a):(b) )

        /** Returns the absolute value of a number.
         */
        #define absValue( a ) ( (a)>0? (a):-(a) )

        /** Sign is a 'method' to determine the sign
         *  of a number. If this function returns -1,
         *  we're dealing with a negative number, if
         *  it returns 1, our number is positive. It
         *  returns 0 if our number is 0.
         */
        #define sign( a ) ( (a)>0?1:((a)<0?-1:0) )

    #endif
};

#endif
