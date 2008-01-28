/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "videomanager.h"

#include <SDL.h>
#include <GL/gl.h>

#include "surface.h"
#include "font.h"
#include "auxfunc.h"

namespace Annchienta
{
    VideoManager *videoManager;

    VideoManager::VideoManager() : screenWidth(0), screenHeight(0)
    {
        videoManager = this;

        reset();
    }

    VideoManager::~VideoManager()
    {
    }
    
    void VideoManager::setVideoMode( int w, int h, const char *title, bool fullscreen )
    {
        /* Get some variables.
         */
        screenWidth = w;
        screenHeight = h;

        /* Choose *best* settings for BitsPerPixel
         */
        Uint32 bpp = SDL_GetVideoInfo()->vfmt->BitsPerPixel;

        /* Preferred video flags.
         */
        Uint32 flags = SDL_HWSURFACE | SDL_OPENGL | SDL_HWACCEL;
        if( fullscreen )
            flags |= SDL_FULLSCREEN;

        /* Set the video mode.
         */
        SDL_Surface *screen = SDL_SetVideoMode( w, h, bpp, flags );

        /* Set the window title.
         */
        SDL_WM_SetCaption( title, NULL );

        /* Make sure we're in the right matrix.
         */
        glMatrixMode( GL_PROJECTION );
        glOrtho( 0, screenWidth, screenHeight, 0, -1, 1 );
        glViewport( 0, 0, screenWidth, screenHeight );

        glMatrixMode( GL_MODELVIEW );

        /* Set some flags.
         */
        glEnable( GL_TEXTURE_2D );
        glEnable( GL_BLEND );
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
        glEnable( GL_CULL_FACE );
        glCullFace( GL_BACK );
    }

    int VideoManager::getScreenWidth() const
    {
        return screenWidth;
    }

    int VideoManager::getScreenHeight() const
    {
        return screenHeight;
    }

    void VideoManager::reset()
    {
        /* Reset the matrix.
        */
        glLoadIdentity();
    
        /* Reset the color.
        */
        this->setColor();

        /* Reset some flags.
         */
        glEnable( GL_TEXTURE_2D );
        glEnable( GL_BLEND );
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
    }
    
    void VideoManager::translate( float x, float y ) const
    {
        glTranslatef( x, y, 0.0f );
    }

    void VideoManager::rotate( float degrees ) const
    {
        glRotatef( degrees, 0.0f, 0.0f, 1.0f );
    }

    void VideoManager::scale( float x, float y ) const
    {
        glScalef( x, y, 1.0f );
    }

    void VideoManager::pushMatrix() const
    {
        glPushMatrix();
    }

    void VideoManager::popMatrix() const
    {
        glPopMatrix();
    }

    void VideoManager::flip() const
    {
        SDL_GL_SwapBuffers();
        glClear( GL_COLOR_BUFFER_BIT );
    }

    void VideoManager::setColor( int red, int green, int blue, int alpha ) const
    {
        glColor4ub( red, green, blue, alpha );
    }

    void VideoManager::setAlpha( int alpha ) const
    {
        GLfloat colors[4];
        glGetFloatv( GL_CURRENT_COLOR, colors );
        colors[3] = (float)alpha/255.0f;
        glColor4fv( colors );
    }

    void VideoManager::drawLine( int x1, int y1, int x2, int y2 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_LINES );
            glVertex2f( x1, y1 );
            glVertex2f( x2, y2 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void VideoManager::drawTriangle( int x1, int y1, int x2, int y2, int x3, int y3 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_TRIANGLES );
            glVertex2f( x1, y1 );
            glVertex2f( x2, y2 );
            glVertex2f( x3, y3 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void VideoManager::drawSurface( Surface *surface, int x, int y ) const
    {
        surface->draw( x, y );
    }

    void VideoManager::drawString( Font *font, const char *str, int x, int y ) const
    {
        font->draw( str, x, y );
    }

    void VideoManager::grabBuffer( Surface *surface ) const
    {
        glBindTexture( GL_TEXTURE_2D, surface->getTexture() );

        glCopyTexSubImage2D( GL_TEXTURE_2D, 0, 0, surface->getGlHeight()-surface->getHeight(), 0, 0, surface->getWidth(), surface->getHeight() );
    }

    void VideoManager::grabBuffer( Surface *surface, int x1, int y1, int x2, int y2 ) const
    {
        if( x1>x2 )
            swap<int>(x1, x2);
        if( y1>y2 )
            swap<int>(y1, y2);

        int width  = x2 - x1,
            height = y2 - y1;

        glBindTexture( GL_TEXTURE_2D, surface->getTexture() );

        glCopyTexSubImage2D( GL_TEXTURE_2D, 0, 0, surface->getGlHeight()-surface->getHeight(), x1, getScreenHeight()-surface->getHeight()-y1, width, height );
    }

    VideoManager *getVideoManager()
    {
        return videoManager;
    }

};
