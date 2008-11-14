/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_SURFACE_H
#define ANNCHIENTA_SURFACE_H

#include <SDL_opengl.h>

namespace Annchienta
{
    /** Holds Surfaces, so mostly images.
     */
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
            /** Construct a new empty instance.
             *  \param width Width of the new Surface.
             *  \param height Height of the new Surface.
             *  \param pixelSize Number of bytes per pixel. Use 3 for RGB and 4 for RGBA.
             */
            Surface( int width, int height, int pixelSize=3 );

            /** Load an image into a surface.
             *  \param filename Valid PNG file.
             */
            Surface( const char *filename );

            ~Surface();

            /** \return The Surface width.
             */
            int getWidth() const;

            /** \return The Surface height.
             */
            int getHeight() const;

            /** Set OpenGL scaling mode to Linear for this surface.
             */
            void setLinearScaling() const;

            /** Set OpenGL scaling mode to Nearest. This is the default behaviour.
             */
            void setNearestScaling() const;

            #ifndef SWIG

                /** Draws the surface at the given position.
                 *  This method is slightly faster than the other draw()
                 *  methods because it makes use of display lists.
                 *  \note Use VideoManager.drawSurface() instead.
                 *  \note Not available in Python.
                 */
                void draw( int x, int y ) const;

                /** Draws a part of the surface to the given position.
                 *  \note Use VideoManager.drawSurface() instead.
                 *  \note Not available in Python.
                 */
                void draw( int dx, int dy, int sx1, int sy1, int sx2, int sy2 ) const;

                /** Draws the surface, stretched to rectangle on the screen.
                 *  \note Use VideoManager.drawSurface() instead.
                 *  \note Not available in Python.
                 */
                void draw( int x1, int y1, int x2, int y2 ) const;

                /** \return The actual OpenGL texture.
                 *  \note Not available in Python.
                 */
                GLuint getTexture() const;

                /** \return The actual width of the OpenGL texture, so a power of two.
                 *  \note Not available in Python.
                 */
                int getGlWidth() const;

                /** \return The actual height of the OpenGL texture, so a power of two.
                 *  \note Not available in Python.
                 */
                int getGlHeight() const;

                /** \return Left Texture Coordinate of the image on the OpenGL texture.
                 *  \note Not available in Python.
                 */
                float getLeftTexCoord() const;

                /** \return Right Texture Coordinate of the image on the OpenGL texture.
                 *  \note Not available in Python.
                 */
                float getRightTexCoord() const;

                /** \return Top Texture Coordinate of the image on the OpenGL texture.
                 *  \note Not available in Python.
                 */
                float getTopTexCoord() const;

                /** \return Bottom Texture Coordinate of the image on the OpenGL texture.
                 *  \note Not available in Python.
                 */
                float getBottomTexCoord() const;
            #endif

    };
};

#endif
