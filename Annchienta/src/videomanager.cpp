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

        backBuffers = new Surface*[numberOfBackBuffers];
        for( int i=0; i<numberOfBackBuffers; i++ )
            backBuffers[i] = 0;
    }

    VideoManager::~VideoManager()
    {
        for( int i=0; i<numberOfBackBuffers; i++ )
            if( backBuffers[i] )
                delete backBuffers[i];
        delete[] backBuffers;
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

        glClearColor( 0.388f, 0.694f, 0.706f, 0.0f );

        for( int i=0; i<numberOfBackBuffers; i++ )
        {
            if( backBuffers[i] )
                delete backBuffers[i];
            backBuffers[i] = new Surface( screenWidth, screenHeight );
        }
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

    void VideoManager::begin()
    {
        glClear( GL_COLOR_BUFFER_BIT );
        this->reset();
    }

    void VideoManager::end()
    {
        SDL_GL_SwapBuffers();
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

    void VideoManager::setClippingRectangle( int x1, int y1, int x2, int y2 ) const
    {
        glScissor( x1, getScreenHeight()-y2, x2-x1, y2-y1 );
        glEnable( GL_SCISSOR_TEST );
    }

    void VideoManager::disableClipping() const
    {
        glDisable( GL_SCISSOR_TEST );
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

    void VideoManager::drawRectangle( int x1, int y1, int x2, int y2 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_QUADS );
            glVertex2f( x1, y1 );
            glVertex2f( x1, y2 );
            glVertex2f( x2, y2 );
            glVertex2f( x2, y1 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void VideoManager::drawQuad( int x1, int y1, int x2, int y2, int x3, int y3, int x4, int y4 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_QUADS );
            glVertex2f( x1, y1 );
            glVertex2f( x2, y2 );
            glVertex2f( x3, y3 );
            glVertex2f( x4, y4 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void VideoManager::drawSurface( Surface *surface, int x, int y ) const
    {
        surface->draw( x, y );
    }

    void VideoManager::drawSurface( Surface *surface, int dx, int dy, int sx1, int sy1, int sx2, int sy2 ) const
    {
        float left = (float)sx1/(float)surface->getGlWidth(),
              right = (float)sx2/(float)surface->getGlWidth(),
              top = 1.0f - (float)sy1/(float)surface->getGlHeight(),
              bottom = 1.0f - (float)sy2/(float)surface->getGlHeight();

        glBindTexture( GL_TEXTURE_2D, surface->getTexture() );
        glBegin( GL_QUADS );

            glTexCoord2f( left, top );
            glVertex2f( dx, dy );

            glTexCoord2f( left, bottom );
            glVertex2f( dx, dy+sy2-sy1 );

            glTexCoord2f( right, bottom );
            glVertex2f( dx+sx2-sx1, dy+sy2-sy1 );

            glTexCoord2f( right, top );
            glVertex2f( dx+sx2-sx1, dy );
        glEnd();
    }

    void VideoManager::drawPattern( Surface *surface, int x1, int y1, int x2, int y2 ) const
    {
        int x, y;

        for( y = y1; y+surface->getHeight()<=y2; y+=surface->getHeight() )
        {
            for( x = x1; x+surface->getWidth()<=x2; x+=surface->getWidth() )
                drawSurface( surface, x, y );

            if( x != x2 )
                drawSurface( surface, x, y, 0, 0, x2-x, surface->getHeight() );
        }

        if( y != y2 )
        {
            for( x = x1; x+surface->getWidth()<=x2; x+=surface->getWidth() )
                drawSurface( surface, x, y, 0, 0, surface->getWidth(), y2-y );

            if( x != x2 )
                drawSurface( surface, x, y, 0, 0, x2-x, y2-y );
        }
    }

    void VideoManager::drawString( Font *font, const char *str, int x, int y ) const
    {
        font->draw( str, x, y );
    }

    void VideoManager::drawStringCentered( Font *font, const char *str, int x, int y ) const
    {
        font->draw( str, x - font->getStringWidth( str )/2, y );
    }

    void VideoManager::drawStringRight( Font *font, const char *str, int x, int y ) const
    {
        font->draw( str, x - font->getStringWidth( str ), y );
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

    void VideoManager::storeBuffer( int slot )
    {
        if( slot>=0 && slot<numberOfBackBuffers )
            this->grabBuffer( backBuffers[slot] );
    }

    void VideoManager::restoreBuffer( int slot ) const
    {
        if( slot>=0 && slot<numberOfBackBuffers )
            backBuffers[slot]->draw( 0, 0 );
    }

    VideoManager *getVideoManager()
    {
        return videoManager;
    }

};
