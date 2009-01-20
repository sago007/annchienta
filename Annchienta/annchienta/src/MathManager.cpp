/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
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
        newRandomSeed();

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

    void MathManager::newRandomSeed() const
    {
        srand( time( 0 ) );
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

    float MathManager::abs( const float &value ) const
    {
        return value>0?value:-value;
    }

};

