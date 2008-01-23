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

            void draw( int x, int y, const char *text );
    };
};

#endif
