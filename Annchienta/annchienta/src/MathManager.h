/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MATHMANAGER_H
#define ANNCHIENTA_MATHMANAGER_H

namespace Annchienta
{

    /** A class which can be used to solve mathematical
     *  problems.
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
             */
            int min( const int &a, const int &b ) const;

            /** Returns a or b, whichever is the largest.
             */
            int max( const int &a, const int &b ) const;

            /** Returns the absolute value.
             */
            int abs( const int &value ) const;
    };

    /** \return An instance of the global MathManager.
     */
    MathManager *getMathManager();

};

#endif
