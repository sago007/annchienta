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

#include "VideoManager.h"

#include <SDL.h>
#include <SDL_opengl.h>

#include "Surface.h"
#include "Font.h"
#include "LogManager.h"

namespace Annchienta
{
    VideoManager *videoManager;

    VideoManager::VideoManager()
    {
        videoManager = this;

        videoModeSet = false;
        screenWidth = 0;
        screenHeight = 0;
        fullScreen = false;
        videoScale = 1;

        /* Create room for pointers to backbuffers but don't
         * actually create them, we can only do that when we
         * know the screen size.
         */
        backBuffers = new Surface*[numberOfBackBuffers];
        for( int i=0; i<numberOfBackBuffers; i++ )
            backBuffers[i] = 0;

        getLogManager()->message("Succesfully started VideoManager.");
    }

    VideoManager::~VideoManager()
    {
        getLogManager()->message("Deleting VideoManager...");

        for( int i=0; i<numberOfBackBuffers; i++ )
            if( backBuffers[i] )
                delete backBuffers[i];
        delete[] backBuffers;
    }

    void VideoManager::setVideoMode( int w, int h, const char *title, bool _fullScreen, int _videoScale )
    {
        LogManager *logManager = getLogManager();

        /* Register that we (will) set it. */
        videoModeSet = true;

        /* Get some variables. */
        screenWidth = w;
        screenHeight = h;
        fullScreen = _fullScreen;
        videoScale = _videoScale;

        /* Make sure we have decent values. */
        if( screenWidth<=0 || screenHeight<=0 || videoScale<=0 )
            logManager->error( "Can not set video mode to %dx%d, scale %d.", screenWidth, screenHeight, videoScale );

        /* Choose *best* settings for BitsPerPixel */
        Uint32 bpp = SDL_GetVideoInfo()->vfmt->BitsPerPixel;

        /* Preferred video flags. */
        Uint32 flags = SDL_HWSURFACE | SDL_OPENGL | SDL_HWACCEL;
        if( fullScreen )
            flags |= SDL_FULLSCREEN;

        /* Set the video mode. */
        SDL_Surface *screen = SDL_SetVideoMode( w*videoScale, h*videoScale, bpp, flags );

        /* Make sure we have a screen now. */
        if( !screen )
            logManager->error("Could not set video mode. SDL_Error: %s", SDL_GetError() );
        /* Set the window title. */
        SDL_WM_SetCaption( title, NULL );

        /* Make sure we're in the right matrix. */
        glMatrixMode( GL_PROJECTION );
        glLoadIdentity();
        glOrtho( 0, screenWidth, screenHeight, 0, -1, 1 );
        glViewport( 0, 0, screenWidth*videoScale, screenHeight*videoScale );

        glMatrixMode( GL_MODELVIEW );
        glLoadIdentity();

        /* Set some flags. */
        glEnable( GL_TEXTURE_2D );
        glEnable( GL_BLEND );
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );

        /* Only enable culling under certain circumstances. */
        //glEnable( GL_CULL_FACE );
        glCullFace( GL_BACK );

        glClearColor( 0.388f, 0.694f, 0.706f, 1.0f );

        for( int i=0; i<numberOfBackBuffers; i++ )
        {
            if( backBuffers[i] )
                delete backBuffers[i];
            backBuffers[i] = new Surface( screenWidth*videoScale, screenHeight*videoScale );
        }

        /* Give some information to our good friend Log. */
        logManager->message( "Set video mode as %dx%d pixels.", screenWidth, screenHeight );
        logManager->message( "Using OpenGL %s by %s on renderer %s.", glGetString(GL_VERSION), glGetString(GL_VENDOR), glGetString(GL_RENDERER) );

        /* Reset colors and matrices. */
        this->reset();
    }

    bool VideoManager::isVideoModeSet() const
    {
        return videoModeSet;
    }

    int VideoManager::getScreenWidth() const
    {
        return screenWidth;
    }

    int VideoManager::getScreenHeight() const
    {
        return screenHeight;
    }

    int VideoManager::isFullScreen() const
    {
        return fullScreen;
    }

    int VideoManager::getVideoScale() const
    {
        return videoScale;
    }

    int VideoManager::getNumberOfBackBuffers() const
    {
        return numberOfBackBuffers;
    }

    void VideoManager::reset()
    {
        /* Reset the matrix. */
        glLoadIdentity();
    
        /* Reset the color. */
        this->setColor();

        /* Reset some flags. */
        glEnable( GL_TEXTURE_2D );
        glEnable( GL_BLEND );
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
    }
    
    void VideoManager::identity() const
    {
        glLoadIdentity();
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

    void VideoManager::push() const
    {
        glPushMatrix();
    }

    void VideoManager::pop() const
    {
        glPopMatrix();
    }

    void VideoManager::clear()
    {
        glClear( GL_COLOR_BUFFER_BIT );
        this->reset();
    }

    void VideoManager::flip()
    {
        SDL_GL_SwapBuffers();
    }

    void VideoManager::setClearColor( int red, int green, int blue, int alpha ) const
    {
        glClearColor( float(red)/255.0f, float(green)/255.0f, float(blue)/255.0f, float(alpha)/255.0f );
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
        glScissor( x1*videoScale, (getScreenHeight()-y2)*videoScale, (x2-x1)*videoScale, (y2-y1)*videoScale );
        glEnable( GL_SCISSOR_TEST );
    }

    void VideoManager::disableClipping() const
    {
        glDisable( GL_SCISSOR_TEST );
    }

    void VideoManager::drawLine( float x1, float y1, float x2, float y2 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_LINES );
            glVertex2f( (GLfloat)x1, (GLfloat)y1 );
            glVertex2f( (GLfloat)x2, (GLfloat)y2 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void VideoManager::drawTriangle( float x1, float y1, float x2, float y2, float x3, float y3 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_TRIANGLES );
            glVertex2f( (GLfloat)x1, (GLfloat)y1 );
            glVertex2f( (GLfloat)x2, (GLfloat)y2 );
            glVertex2f( (GLfloat)x3, (GLfloat)y3 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void VideoManager::drawRectangle( float x1, float y1, float x2, float y2 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_QUADS );
            glVertex2f( (GLfloat)x1, (GLfloat)y1 );
            glVertex2f( (GLfloat)x1, (GLfloat)y2 );
            glVertex2f( (GLfloat)x2, (GLfloat)y2 );
            glVertex2f( (GLfloat)x2, (GLfloat)y1 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void VideoManager::drawQuad( float x1, float y1, float x2, float y2, float x3, float y3, float x4, float y4 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_QUADS );
            glVertex2f( (GLfloat)x1, (GLfloat)y1 );
            glVertex2f( (GLfloat)x2, (GLfloat)y2 );
            glVertex2f( (GLfloat)x3, (GLfloat)y3 );
            glVertex2f( (GLfloat)x4, (GLfloat)y4 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void VideoManager::drawSurface( Surface *surface, float x, float y ) const
    {
        surface->draw( x, y );
    }

    void VideoManager::drawSurface( Surface *surface, float dx, float dy, float sx1, float sy1, float sx2, float sy2 ) const
    {
        surface->draw( dx, dy, sx1, sy1, sx2, sy2 );
    }

    void VideoManager::drawSurface( Surface *surface, float x1, float y1, float x2, float y2 ) const
    {
        surface->draw( x1, y1, x2, y2 );
    }

    void VideoManager::drawPattern( Surface *surface, float x1, float y1, float x2, float y2 ) const
    {
        float x, y;

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

    void VideoManager::drawString( Font *font, const char *str, float x, float y ) const
    {
        font->draw( str, x, y );
    }

    void VideoManager::drawStringCentered( Font *font, const char *str, float x, float y ) const
    {
        font->draw( str, x - font->getStringWidth( str )/2, y );
    }

    void VideoManager::drawStringRight( Font *font, const char *str, float x, float y ) const
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
        x1 *= videoScale;
        y1 *= videoScale;
        x2 *= videoScale;
        y2 *= videoScale;

        int width  = x2 - x1,
            height = y2 - y1;

        glBindTexture( GL_TEXTURE_2D, surface->getTexture() );
        glCopyTexSubImage2D( GL_TEXTURE_2D, 0, 0, surface->getGlHeight()-height, x1, getScreenHeight()*videoScale-y1-height, width, height );
    }

    void VideoManager::storeBuffer( int slot )
    {
        if( slot>=0 && slot<numberOfBackBuffers )
            this->grabBuffer( backBuffers[slot] );
    }

    void VideoManager::restoreBuffer( int slot ) const
    {
        if( slot>=0 && slot<numberOfBackBuffers )
            drawSurface( backBuffers[slot], 0, 0, getScreenWidth(), getScreenHeight() );
    }

    void VideoManager::boxBlur( int x1, int y1, int x2, int y2, int radius )
    {
        /* Save original matrix. */
        push();

        /* Restrict box blur to given rectangle. */
        setClippingRectangle( x1, y1, x2, y2 );

        /* Revert the scaling we set... Too bad grabBuffer won't take
         * it into account by default. */
        scale( 1.0f/(GLfloat)videoScale, 1.0f/(GLfloat)videoScale );

        /* Caluculate various parameters. */
        int side = radius*2+1;
        int times = side*side;
        float alphaInc = -255.0f/(float)times;
        float alpha = 255.0f;

        /* Store the buffer we will use. */
        grabBuffer( backBuffers[0], x1, y1, x2, y2 );

        for( int y=-radius; y<=radius; y++ )
        {
            for( int x=-radius; x<=radius; x++ )
            {
                /* Choose the correct color. */
                setColor( 255, 255, 255, (int)alpha );

                /* Draw the buffer stretched to position. */
                drawSurface( backBuffers[0], (x1+x)*videoScale, (y1+y)*videoScale, 0, 0, (x2-x1)*videoScale, (y2-y1)*videoScale );

                /* Every time, we increase our alpha value. */
                alpha += alphaInc;
            }
        }

        /* Disable clipping and restore matrix. */
        disableClipping();
        pop();
        setColor();
    }

    VideoManager *getVideoManager()
    {
        return videoManager;
    }

};
