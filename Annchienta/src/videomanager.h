/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_VIDEOMANAGER_H
#define ANNCHIENTA_VIDEOMANAGER_H

namespace Annchienta
{

    class Surface;
    class Font;

    class VideoManager
    {
        private:
            int screenWidth, screenHeight;
            static const int numberOfBackBuffers = 8;
            Surface **backBuffers;

        public:
            #ifndef SWIG
                VideoManager();
                ~VideoManager();
            #endif

            /** Sets the video mode.
             */
            void setVideoMode( int w, int h, const char *title="Annchienta RPG Engine", bool fullscreen=false );
            int getScreenWidth() const;
            int getScreenHeight() const;

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
            void begin();
            void end();

            /** Sets a color, used for text and surface drawing.
             */
            void setColor( int red=0xff, int green=0xff, int blue=0xff, int alpha=0xff ) const;
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
    };

    VideoManager *getVideoManager();

};

#endif
