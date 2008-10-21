/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "Vector.h"

#include <cmath>

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
    
};

