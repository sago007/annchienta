/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "painter.h"

#include <SDL.h>
#include <GL/gl.h>

namespace Annchienta
{
    Painter *painter;

    Painter::Painter()
    {
        painter = this;

        reset();
    }

    Painter::~Painter()
    {
    }
    
    void Painter::reset()
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
    
    void Painter::translate( float x, float y ) const
    {
        glTranslatef( x, y, 0.0f );
    }

    void Painter::rotate( float degrees ) const
    {
        glRotatef( degrees, 0.0f, 0.0f, 1.0f );
    }

    void Painter::scale( float x, float y ) const
    {
        glScalef( x, y, 1.0f );
    }

    void Painter::pushMatrix() const
    {
        glPushMatrix();
    }

    void Painter::popMatrix() const
    {
        glPopMatrix();
    }

    void Painter::flip() const
    {
        SDL_GL_SwapBuffers();
        glClear( GL_COLOR_BUFFER_BIT );
    }

    void Painter::setColor( int red, int green, int blue, int alpha ) const
    {
        glColor4ub( red, green, blue, alpha );
    }

    void Painter::drawLine( int x1, int y1, int x2, int y2 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_LINES );
            glVertex2f( x1, y1 );
            glVertex2f( x2, y2 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    void Painter::drawTriangle( int x1, int y1, int x2, int y2, int x3, int y3 ) const
    {
        glDisable( GL_TEXTURE_2D );

        glBegin( GL_TRIANGLES );
            glVertex2f( x1, y1 );
            glVertex2f( x2, y2 );
            glVertex2f( x3, y3 );
        glEnd();

        glEnable( GL_TEXTURE_2D );
    }

    Painter *getPainter()
    {
        return painter;
    }

};
