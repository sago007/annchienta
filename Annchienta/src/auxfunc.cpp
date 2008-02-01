/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "auxfunc.h"

#include <stdlib.h>
#include <stdio.h>
#include <math.h>

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

    bool isValidFile( const char *filename )
    {
        FILE *f = fopen( filename, "r" );

        if( f==NULL )
            return false;

        fclose( f );
        return true;
    }

    float distance( float x1, float y1, float x2, float y2 )
    {
        return sqrt( square(x2-x1) + square(y2-y1) );
    }


    float squaredDistance( float x1, float y1, float x2, float y2 )
    {
        return ( square(x2-x1) + square(y2-y1) );
    }

    void copyFile( const char *srcFname, const char *dstFname )
    {
        FILE *src = fopen( srcFname, "r" );
        FILE *dst = fopen( dstFname, "w" );

        if( !src )
            return;

        if( !dst )
            return;

        char ch;

        while( !feof(src) )
        {
            ch = getc( src );
            if( !feof(src) )
                putc( ch, dst );
        }

        fclose( src );
        fclose( dst );
    }

};
