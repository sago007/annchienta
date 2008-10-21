/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_VECTOR_H
#define ANNCHIENTA_VECTOR_H

namespace Annchienta
{

    class Vector
    {
        public:
            float x, y;
        
            Vector( float x, float y );
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
            
            /** Dot product
             */
            float operator*(const Vector &other) const;
            
            float length() const;
            float lengthSquared() const;
            float distance( const Vector &other ) const;

            void normalize();

            /** Cap the vector coordinates. For example, a vector
             *  with coordinates (-5,2) would become (-3,2) after
             *  capping with -3 as mimimum and 3 as maximum.
             *  \param minimum The mimum value of a coordinate.
             *  \param maximum The maximum value of a coordinate.
             */
            void cap( const float &minimum, const float &maximum );
    };

};

#endif
