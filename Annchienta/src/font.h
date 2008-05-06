/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_FONT_H
#define ANNCHIENTA_FONT_H

#include <GL/gl.h>

namespace Annchienta
{

    /** Class used for holding, loading fonts.
     */
    class Font
    {
        private:
            int height;
            int lineHeight;

            GLuint *textures;
            GLuint list;

            int *advance;

        public:
            /** Attempts to load a valid TTF font.
             *  \param filename TTF font to be loaded.
             *  \param height Size for the new font. (in pixels)
             */
            Font( const char *filename, int height=14 );
            ~Font();

            /** \return The height (size) of this font.
             */
            int getHeight() const;

            /** \return The height (size) of this font and a little extra space for space between lines.
             */
            int getLineHeight() const;

            /** Predict how wide a string will be when drawn.
             *  \param text The string of which the width should be calculated.
             *  \return The width in pixels.
             */
            int getStringWidth( const char *text ) const;

            #ifndef SWIG
                /** Draws a font to the screen.
                 *  \note Use VideoManager::drawString().
                 *  \note Not available in Python.
                 */
                void draw( const char *text, int x, int y ) const;
            #endif
    };
};

#endif
