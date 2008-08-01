/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "GeneralFunctions.h"

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
        return sqrt( squaredDistance(x1,y1,x2,y2) );
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

    int strcmpCaseInsensitive( const char *str1, const char *str2 )
    {
        const int caseDiff = 'A' - 'a';

        while( *str1 || *str2 )
        {
            if( (*str1 == *str2) || (*str1 == *str2+caseDiff) || (*str1 == *str2-caseDiff) )
            {
                str1++;
                str2++;
            }
            else
            {
                return 1;
            }
        }
        return 0;
    }

};