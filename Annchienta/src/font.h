/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_FONT_H
#define ANNCHIENTA_FONT_H

#include <GL/gl.h>

namespace Annchienta
{
    class Font
    {
        private:
            int height;
            int lineHeight;

            GLuint *textures;
            GLuint list;

            int *advance;

        public:
            Font( const char *filename, int height );
            ~Font();

            int getHeight() const;
            int getLineHeight() const;
            int getStringWidth( const char *text ) const;

            #ifndef SWIG
                void draw( const char *text, int x, int y ) const;
            #endif
    };
};

#endif
