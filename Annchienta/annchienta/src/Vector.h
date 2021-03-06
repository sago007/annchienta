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

#ifndef ANNCHIENTA_VECTOR_H
#define ANNCHIENTA_VECTOR_H

namespace Annchienta
{

    /** This is a class that can be used to perform
     *  mathematical operations with 2D vectors, and
     *  thus comes in handy in a lot of games.
     *
     *  Note that this class is designed to be 'independent'
     *  of the other classes in the engine, meaning
     *  no functions in the engine will require or return
     *  Vectors (altough some classes use this class
     *  internally).
     *
     *  If you want to represent a point on the map,
     *  it would be better to use the \ref Point class,
     *  designed for this.
     */
    class Vector
    {
        public:
        
            /** The X coordinate of the Vector.
             */
            float x;
            /** The Y coordinate of the Vector.
             */
            float y;
        
            /** Creates a new Vector with given coordinates.
             *  \param x X coordinate for the Vector.
             *  \param y Y coordinate for the Vector.
             */
            Vector( float x=0, float y=0 );
            
            /** Creates a new Vector based on another Vector,
             *  copy constructor.
             *  \param other Vector to copy.
             */
            Vector( const Vector &other );
            ~Vector();
            
            #ifndef SWIG
                Vector &operator=(const Vector &other);
            #endif
            
            Vector operator+(const Vector &other) const;
            Vector operator-(const Vector &other) const;
            
            Vector operator*(const float &scalar) const;
            Vector operator/(const float &scalar) const;
            
            Vector &operator+=(const Vector &other);
            Vector &operator-=(const Vector &other);
            
            Vector &operator*=(const float &scalar);
            Vector &operator/=(const float &scalar);
            
            /** Note: this calculates the Dot product.
             */
            float operator*(const Vector &other) const;
            
            /** Gets the length of this Vector.
             *  \return This Vector's length.
             */
            float length() const;
            
            /** Returns the squared length of this Vector.
             *  this method is a lot faster than the length()
             *  method.
             *  \return The length of this Vector, squared.
             */
            float lengthSquared() const;
            
            /** Calculates the distance between the representation
             *  of this Vector as a cartesian coordinate and an the
             *  representation of another Vector.
             *  \param other The other Vector.
             *  \return The distance between this and the other Vector.
             */
            float distance( const Vector &other ) const;

            /** Normalizes the Vector: this will change the Vector
             *  so it has length 1, while maintaining the ratio
             *  between the X and Y values.
             */
            void normalize();

            /** Cap the vector coordinates. For example, a vector
             *  with coordinates (-5,2) would become (-3,2) after
             *  capping with -3 as mimimum and 3 as maximum.
             *  \param minimum The mimum value of a coordinate.
             *  \param maximum The maximum value of a coordinate.
             */
            void cap( const float &minimum, const float &maximum );

            /** Set the X and Y coordinates from polar coordinates.
             *  \param r The distance, radius to the polar coordinate.
             *  \param theta The rotation, angle to the polar coordinate in radians.
             */
            void fromPolar( const float &r, const float &theta );

            /** Get the angle for this Vector: this is the angle between
             *  the (1,0) Vector and this vector, or, in other words, the
             *  theta argument to fromPolar()
             *  \return The requested angle.
             */
            float getAngle() const;
    };

};

#endif
