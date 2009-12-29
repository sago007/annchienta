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

#include "Vector.h"

#include <cmath>

using namespace std;

namespace Annchienta
{
    Vector::Vector( float _x, float _y ): x(_x), y(_y)
    {
    }

    Vector::Vector( const Vector &other ): x(other.x), y(other.y)
    {
    }

    Vector::~Vector()
    {
    }

    Vector &Vector::operator= (const Vector &other)
    {
        x = other.x;
        y = other.y;
        return *this;
    }
       
    Vector Vector::operator+(const Vector &other) const
    {
        return Vector( x+other.x, y+other.y );
    }
    
    Vector Vector::operator-(const Vector &other) const
    {
        return Vector( x-other.x, y-other.y );
    }
    
    Vector Vector::operator*(const float &scalar) const
    {
        return Vector( x*scalar, y*scalar );
    }
    
    Vector Vector::operator/(const float &scalar) const
    {
        return Vector( x*scalar, y*scalar );
    } 
    Vector &Vector::operator+=(const Vector &other)
    {
        (*this) = (*this) + other;
        return (*this);
    }
    
    Vector &Vector::operator-=(const Vector &other)
    {
        (*this) = (*this) - other;
        return (*this);
    }
    
    Vector &Vector::operator*=(const float &scalar)
    {
        (*this) = (*this) * scalar;
        return (*this);
    }
    
    Vector &Vector::operator/=(const float &scalar)
    {
        (*this) = (*this) / scalar;
        return (*this);
    }

    float Vector::operator*(const Vector &other) const
    {
        return x*other.x + y*other.y;
    }
    
    float Vector::length() const
    {
        return sqrt( lengthSquared() );
    }

    float Vector::lengthSquared() const
    {
        return x*x + y*y;
    }

    float Vector::distance( const Vector &other ) const
    {
        return ((*this)-other).length();
    }

    void Vector::normalize()
    {
        float l = length();
        if( l>0.0f )
        {
            x /= l;
            y /= l;
        }
    }

    void Vector::cap( const float &minimum, const float &maximum )
    {
        if( x<minimum )
            x = minimum;
        if( y<minimum )
            y = minimum;
        if( x>maximum )
            x = maximum;
        if( y>maximum )
            y = maximum;
    }

    void Vector::fromPolar( const float &r, const float &theta )
    {
        x = r * cos( theta );        
        y = r * sin( theta );        
    }

    float Vector::getAngle() const
    {
        return atan2( y, x );
    }
    
};

