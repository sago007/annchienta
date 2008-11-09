/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_VIDEOMANAGER_H
#define ANNCHIENTA_VIDEOMANAGER_H

namespace Annchienta
{

    class Surface;
    class Font;

    /** A class used for painting on the screen.
     */
    class VideoManager
    {
        private:
            int screenWidth, screenHeight;
            bool fullScreen;
            static const int numberOfBackBuffers = 8;
            Surface **backBuffers;

        public:
            #ifndef SWIG
                VideoManager();
                ~VideoManager();
            #endif

            /** Sets the video mode. Use this before doing any drawing operations.
             *  \param w Width for the screen.
             *  \param h Height for the screen.
             *  \param title Caption to be used for the window.
             *  \param fullscreen Should the game run in fullscreen mode? (Might not always work with all resolutions.)
             */
            void setVideoMode( int w, int h, const char *title="Annchienta RPG Engine", bool fullscreen=false );

            /** \return Width of the screen.
             */
            int getScreenWidth() const;

            /** \return Height of the screen.
             */
            int getScreenHeight() const;

            /** \return If we are in full screen mode.
             */
            int isFullScreen() const;

            /** Resets all matrixes, colors...
             */
            void reset();

            /** Loads identity matrix.
             */
            void identity() const;

            /** Multiply the current matrix with a translation matrix.
             *  \param x X translation distance.
             *  \param y Y translation distance.
             */
            void translate( float x, float y ) const;

            /** Multiply the current matrix with a rotation matrix.
             *  \param degrees Degrees to be rotated clockwise.
             */
            void rotate( float degrees ) const;

            /** Multiply the current matrix with a scalar matrix.
             *  \param x X scale factor.
             *  \param y Y scale factor.
             */
            void scale( float x, float y ) const;

            /** Pushes the current matrix onto the stack.
             */
            void pushMatrix() const;

            /** Restores a matrix from the stack.
             */
            void popMatrix() const;

            /** Begins the scene. Clears and resets the screen.
             */
            void begin();

            /** Draw the buffer to the screen.
             */
            void end();

            /** Sets the color used for clearing the screen with.
             */
            void setClearColor( int red=0xff, int green=0xff, int blue=0xff, int alpha=0xff ) const;

            /** Sets the color used for all drawing.
             */
            void setColor( int red=0xff, int green=0xff, int blue=0xff, int alpha=0xff ) const;

            /** Sets the alpha component for the current color.
             *  \param alpha Alpha Component. [0-255].
             */
            void setAlpha( int alpha=0xff ) const;

            /** Sets clipping rectangle.
             */
            void setClippingRectangle( int x1, int y1, int x2, int y2 ) const;
            void disableClipping() const;

            /** Drawing functions.
             */
            void drawLine( int x1, int y1, int x2, int y2 ) const;
            void drawTriangle( int x1, int y1, int x2, int y2, int x3, int y3 ) const;
            void drawRectangle( int x1, int y1, int x2, int y2 ) const;
            void drawQuad( int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4 ) const;
            void drawSurface( Surface *surface, int x, int y ) const;
            void drawSurface( Surface *surface, int dx, int dy, int sx1, int sy1, int sx2, int sy2 ) const;
            void drawPattern( Surface *surface, int x1, int y1, int x2, int y2 ) const;
            void drawString( Font *font, const char *str, int x, int y ) const;
            void drawStringCentered( Font *font, const char *str, int x, int y ) const;
            void drawStringRight( Font *font, const char *str, int x, int y ) const;

            /** Copies the buffer to a surface.
             */
            void grabBuffer( Surface* ) const;
            void grabBuffer( Surface*, int x1, int y1, int x2, int y2 ) const;

            void storeBuffer( int slot );
            void restoreBuffer( int slot ) const;

            /** Does not work when a clipping rectangle is set.
             */
            void boxBlur( int x1, int y1, int x2, int y2, int radius=2 );
    };

    VideoManager *getVideoManager();

};

#endif
