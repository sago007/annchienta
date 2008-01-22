/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "painter.h"

#include <SDL.h>
#include <GL/gl.h>

namespace Annchienta
{
    Painter::Painter()
    {
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
    
    void Painter::translate( float x, float y )
    {
        glTranslatef( x, y, 0.0f );
    }

    void Painter::rotate( float degrees )
    {
        glRotatef( degrees, 0.0f, 0.0f, 1.0f );
    }

    void Painter::scale( float x, float y )
    {
        glScalef( x, y, 1.0f );
    }

    void Painter::pushMatrix()
    {
        glPushMatrix();
    }

    void Painter::popMatrix()
    {
        glPopMatrix();
    }

    void Painter::flip()
    {
        SDL_GL_SwapBuffers();
        glClear( GL_COLOR_BUFFER_BIT );
    }

    void Painter::setColor( int red, int green, int blue, int alpha )
    {
        glColor4ub( red, green, blue, alpha );
    }

    void Painter::drawLine( int x1, int x2, int y1, int y2 )
    {
        glBegin( GL_LINES );
            glVertex2f( x1, x2 );
            glVertex2f( y1, y2 );
        glEnd();
    }

};
