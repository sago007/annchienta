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

#ifndef ANNCHIENTA_MATHMANAGER_H
#define ANNCHIENTA_MATHMANAGER_H

namespace Annchienta
{

    /** A class which can be used to solve mathematical
     *  problems. It is mainly used for generating random
     *  numbers.
	 */
    class MathManager
    {
        private:

        public:

            #ifndef SWIG
                MathManager();
                ~MathManager();
            #endif

            /** Returns the next power of two.
             *  \param input Any positive integer.
             *  \return A power of two, larger than input.
             */
            int nearestPowerOfTwo( const int &input ) const;

            /** Get a random integer.
             *  \param maximum The maximum, exclusive.
             *  \return The random integer.
             */
            int randInt( const int &maximum ) const;

            /** Get a random integer.
             *  \param minimum The minimum, inclusive.
             *  \param maximum The maximum, exclusive.
             *  \return The random integer.
             */
            int randInt( const int &minimum, const int &maximum ) const;

            /** Get a random floating point number between 0 and 1,
             *  both inclusive.
             *  \return A floating point number.
             */
            float randFloat() const;

            /** Get a random floating point number.
             *  \param minimum The minimum, inclusive.
             *  \param maximum The maximum, inclusice.
             *  \return A floating point number.
             */
            float randFloat( const float &minimum, const float &maximum) const;

            /** Returns a or b, whichever is the smallest.
             *  \param a An integer.
             *  \param b An integer.
             *  \return The smallest of a and b.
             */
            int min( const int &a, const int &b ) const;

            /** Returns a or b, whichever is the largest.
             *  \param a An integer.
             *  \param b An integer.
             *  \return The largest of a and b.
             */
            int max( const int &a, const int &b ) const;

            /** Returns the absolute value.
             *  \param value An integer.
             *  \return The absolute value of the input.
             */
            int abs( const int &value ) const;

    };

    /** \return An instance of the global MathManager.
     */
    MathManager *getMathManager();

};

#endif
