/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "MathManager.h"

#include <ctime>
#include <cstdlib>

#include "LogManager.h"

namespace Annchienta
{
    MathManager *mathManager;

    MathManager::MathManager()
    {
        /* Set reference to single-instance class. */
        mathManager = this;

        /* Start random numbers. */
        srand( time( 0 ) );

        getLogManager()->message("Succesfully started MathManager.");
    }

    MathManager::~MathManager()
    {
        getLogManager()->message("Deleting MathManager...");
    }

    MathManager *getMathManager()
    {
        return mathManager;
    }

    int MathManager::nearestPowerOfTwo( const int &input ) const
    {
        int value = 1;
        while( value<input )
            value <<= 1;
        return value;
    }

    int MathManager::randInt( const int &maximum ) const
    {
        return rand()%maximum;
    }

    int MathManager::randInt( const int &minimum, const int &maximum ) const
    {
        return minimum + rand()%(maximum-minimum);
    }

    float MathManager::randFloat() const
    {
        return rand()/(float(RAND_MAX)+1.0f);
    }

    float MathManager::randFloat( const float &minimum, const float &maximum) const
    {
        return minimum + randFloat()*(maximum-minimum);
    }

    int MathManager::min( const int &a, const int &b ) const
    {
        return a<b?a:b;
    }

    int MathManager::max( const int &a, const int &b ) const
    {
        return a>b?a:b;
    }

    int MathManager::abs( const int &value ) const
    {
        return value>0?value:-value;
    }

};

