/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "Vector.h"

#include <math.h>
#include "GeneralFunctions.h"

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
        return sqrt( square(x)+square(y) );
    }

    float Vector::distance( const Vector &other ) const
    {
        return ((*this)-other).length();
    }
    
};
