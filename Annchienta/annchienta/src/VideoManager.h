/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_VIDEOMANAGER_H
#define ANNCHIENTA_VIDEOMANAGER_H

namespace Annchienta
{

    class Surface;
    class Font;

    /** A class used for painting on the screen. This supports
     *  2D drawing features.
     */
    class VideoManager
    {
        private:
            int screenWidth, screenHeight;
            bool fullScreen;
            int videoScale;
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
             *  \param fullScreen Should the game run in fullscreen mode? (Might not always work with all resolutions.)
             *  \param videoScale Defaults to 1, choose a higher number to get a larger screen.
             */
            void setVideoMode( int w, int h, const char *title="Annchienta RPG Engine", bool fullScreen=false, int videoScale=1 );

            /** \return Width of the screen.
             */
            int getScreenWidth() const;

            /** \return Height of the screen.
             */
            int getScreenHeight() const;

            /** \return If we are in full screen mode.
             */
            int isFullScreen() const;

            /** \return The video mode scale.
             */
            int getVideoScale() const;

            /** \return The number of backbuffers available.
             */
            int getNumberOfBackBuffers() const;

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
            void push() const;

            /** Restores a matrix from the stack.
             */
            void pop() const;

            /** Begins the scene. Clears and resets the screen.
             */
            void clear();

            /** Draw the buffer to the screen.
             */
            void flip();

            /** Sets the color used for clearing the screen with.
             *  \param red Red component of clearing color. [0-255].
             *  \param green Green component of clearing color. [0-255].
             *  \param blue Blue component of clearing color. [0-255].
             *  \param alpha Alpha component of clearing color. [0-255].
             */
            void setClearColor( int red=0xff, int green=0xff, int blue=0xff, int alpha=0xff ) const;

            /** Sets the color used for all drawing of primitives and
             *  text. This color gets applied to a Surface too. When you
             *  want to draw a Surface in it's regular color, set the color
             *  to white.
             *  \param red Red component of clearing color. [0-255].
             *  \param green Green component of clearing color. [0-255].
             *  \param blue Blue component of clearing color. [0-255].
             *  \param alpha Alpha component of clearing color. [0-255].
             */
            void setColor( int red=0xff, int green=0xff, int blue=0xff, int alpha=0xff ) const;

            /** Sets the alpha component for the current color.
             *  \param alpha Alpha Component. [0-255].
             */
            void setAlpha( int alpha=0xff ) const;

            /** Sets clipping rectangle. This means all drawing, from now on,
             *  will be clipped to the rectangle specified.
             *  \param x1 Top left x coord of the rectangle.
             *  \param y1 Top left y coord of the rectangle.
             *  \param x2 Bottom right x coord of the rectangle.
             *  \param y2 Bottom right y coord of the rectangle.
             *  \warning Matrix transformations do not apply to this.
             */
            void setClippingRectangle( int x1, int y1, int x2, int y2 ) const;

            /** Disable the clipping rectangle set with setClippingRectangle().
             */
            void disableClipping() const;

            /** Draw a straight line between two points.
             *  \param x1 X coord of the 1st point.
             *  \param y1 Y coord of the 1st point.
             *  \param x2 X coord of the 2nd point.
             *  \param y2 Y coord of the 2nd point.
             */
            void drawLine( int x1, int y1, int x2, int y2 ) const;

            /** Draw a triangle between three points.
             *  \param x1 X coord of the 1st point.
             *  \param y1 Y coord of the 1st point.
             *  \param x2 X coord of the 2nd point.
             *  \param y2 Y coord of the 2nd point.
             *  \param x3 X coord of the 3rd point.
             *  \param y3 Y coord of the 3rd point.
             */
            void drawTriangle( int x1, int y1, int x2, int y2, int x3, int y3 ) const;

            /** Draw an axis-aligned rectangle.
             *  \param x1 Top left x coord of the rectangle.
             *  \param y1 Top left y coord of the rectangle.
             *  \param x2 Bottom right x coord of the rectangle.
             *  \param y2 Bottom right y coord of the rectangle.
             */
            void drawRectangle( int x1, int y1, int x2, int y2 ) const;

            /** Draw a quad between four points.
             *  \param x1 X coord of the 1st point.
             *  \param y1 Y coord of the 1st point.
             *  \param x2 X coord of the 2nd point.
             *  \param y2 Y coord of the 2nd point.
             *  \param x3 X coord of the 3rd point.
             *  \param y3 Y coord of the 3rd point.
             *  \param x4 X coord of the 4rd point.
             *  \param y4 Y coord of the 4rd point.
             */
            void drawQuad( int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4 ) const;

            /** Draws an entire surface to the screen.
             *  This should be slightly faster than the other drawSurface()
             *  methods because it is optimized.
             *  \param surface Surface to be drawn.
             *  \param x X coord of destination on screen.
             *  \param y Y coord of destination on screen.
             */
            void drawSurface( Surface *surface, int x, int y ) const;

            /** Draws a rectangular part of a surface to the screen.
             *  \param surface Surface to be drawn.
             *  \param dx X coord of destination on screen.
             *  \param dy Y coord of destination on screen.
             *  \param sx1 Top left x coord of the rectangle.
             *  \param sy1 Top left y coord of the rectangle.
             *  \param sx2 Bottom right x coord of the rectangle.
             *  \param sy2 Bottom right y coord of the rectangle.
             */
            void drawSurface( Surface *surface, int dx, int dy, int sx1, int sy1, int sx2, int sy2 ) const;

            /** Draws a surface, stretched to a rectangle on the screen.
             *  \param surface Surface to be drawn.
             *  \param x1 Top left x coord of the rectangle.
             *  \param y1 Top left y coord of the rectangle.
             *  \param x2 Bottom right x coord of the rectangle.
             *  \param y2 Bottom right y coord of the rectangle.
             */
            void drawSurface( Surface *surface, int x1, int y1, int x2, int y2 ) const;

            /** Draws a surface, tiled like a pattern to rectangle
             *  on the screen.
             *  \param surface Surface to be drawn.
             *  \param x1 Top left x coord of the rectangle.
             *  \param y1 Top left y coord of the rectangle.
             *  \param x2 Bottom right x coord of the rectangle.
             *  \param y2 Bottom right y coord of the rectangle.
             */
            void drawPattern( Surface *surface, int x1, int y1, int x2, int y2 ) const;

            /** Draws a string to the screen.
             *  \param font Font to be used.
             *  \param str The string to be drawn.
             *  \param x X destination coord on the screen.
             *  \param y Y destination coord on the screen.
             */
            void drawString( Font *font, const char *str, int x, int y ) const;

            /** Draws a string to the screen, horizontally centered.
             *  \param font Font to be used.
             *  \param str The string to be drawn.
             *  \param x X destination coord on the screen.
             *  \param y Y destination coord on the screen.
             */
            void drawStringCentered( Font *font, const char *str, int x, int y ) const;

            /** Draws a string to the screen, horizontally right-aligned.
             *  \param font Font to be used.
             *  \param str The string to be drawn.
             *  \param x X destination coord on the screen.
             *  \param y Y destination coord on the screen.
             */
            void drawStringRight( Font *font, const char *str, int x, int y ) const;

            /** Copy the entire buffer to a Surface. Make sure your
             *  Surface is large enough, especially when the videoScale
             *  set is larger than 1.
             *  \param surface Destination of the buffer pixels.
             *  \warning Matrix transformations to not apply to this.
             *  \note It is safer to use the storeBuffer() and restoreBuffer() methods.
             */
            void grabBuffer( Surface *surface ) const;

            /** Copy a part of the buffer to a Surface. Make sure your
             *  Surface is large enough, especially when the videoScale
             *  set is larger than 1.
             *  \param surface Destination of the buffer pixels.
             *  \param x1 Top left x coord of the rectangle.
             *  \param y1 Top left y coord of the rectangle.
             *  \param x2 Bottom right x coord of the rectangle.
             *  \param y2 Bottom right y coord of the rectangle.
             *  \warning Matrix transformations do not apply to this.
             *  \note It is safer to use the storeBuffer() and restoreBuffer() methods.
             */
            void grabBuffer( Surface *surface, int x1, int y1, int x2, int y2 ) const;

            /** Saves the current buffer to a slot. There are certainly 8 slots,
             *  so [0-7] can be used. I advise however to use [1-7] exclusively
             *  because slot 0 is sometimes internally used.
             *  You can use getNumberOfBackBuffers() to determine the exact
             *  number of slots.
             *  \param slot Slot to save to.
             */
            void storeBuffer( int slot );

            /** Restores a buffer, stored with storeBuffer().
             *  \param slot Slot to restore from.
             */
            void restoreBuffer( int slot ) const;

            /** Perform a fairly quick box blur to a rectangle of
             *  the current buffer.
             *  This is pretty nice for visual effects.
             *  \param x1 Top left x coord of the rectangle.
             *  \param y1 Top left y coord of the rectangle.
             *  \param x2 Bottom right x coord of the rectangle.
             *  \param y2 Bottom right y coord of the rectangle.
             *  \param radius Blur radius. A large radius will slow down this function.
             *  \warning Matrix transformations do not apply to this.
             */
            void boxBlur( int x1, int y1, int x2, int y2, int radius=2 );
    };

    VideoManager *getVideoManager();

};

#endif
