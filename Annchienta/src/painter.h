/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_PAINTER_H
#define ANNCHIENTA_PAINTER_H

namespace Annchienta
{
    class Painter
    {
        private:

        public:
            #ifndef SWIG
                Painter();
                ~Painter();
            #endif

            /** Resets matrix and colors.
             */
            void reset();

            /** A few matrix operations.
             */
            void translate( float x, float y ) const;
            void rotate( float degrees ) const;
            void scale( float x, float y ) const;

            void pushMatrix() const;
            void popMatrix() const;

            /** Draws the buffer to the screen. Then clears the buffer.
             */
            void flip() const;

            /** Sets a color, used for text and surface drawing.
             */
            void setColor( int red=0xff, int green=0xff, int blue=0xff, int alpha=0xff ) const;

            /** Drawing primitives.
             */
            void drawLine( int x1, int y1, int x2, int y2 ) const;
            void drawTriangle( int x1, int y1, int x2, int y2, int x3, int y3 ) const;
    };

    Painter *getPainter();

};

#endif
