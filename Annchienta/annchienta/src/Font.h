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

#ifndef ANNCHIENTA_FONT_H
#define ANNCHIENTA_FONT_H

#include <SDL_opengl.h>

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
