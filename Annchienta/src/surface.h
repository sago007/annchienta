/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_SURFACE_H
#define ANNCHIENTA_SURFACE_H

#include <GL/gl.h>

namespace Annchienta
{
    class Surface
    {
        private:
            int width, height;
            int glWidth, glHeight;
            int pixelSize;

            float leftTexCoord, rightTexCoord, topTexCoord, bottomTexCoord;

            GLuint texture;
            GLuint list;

            GLubyte *pixels;

            void generateTextureFromPixels();
            void compileList();

        public:
            Surface( int width, int height, int pixelSize=3 );
            Surface( const char *filename );

            ~Surface();

            int getWidth() const;
            int getHeight() const;

            #ifndef SWIG
                void draw( int x, int y ) const;
                GLuint getTexture() const;
                int getGlWidth() const;
                int getGlHeight() const;

                float getLeftTexCoord() const;
                float getRightTexCoord() const;
                float getTopTexCoord() const;
                float getBottomTexCoord() const;
            #endif

    };
};

#endif
