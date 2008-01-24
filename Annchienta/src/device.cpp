/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "device.h"

#include <SDL.h>
#include <GL/gl.h>
#include <Python.h>

#include "painter.h"
#include "inputmanager.h"

namespace Annchienta
{
    Device *device;

    Device::Device()
    {
        /* Set global device...
         */
        device = this;

        /* Init some things...
         */
        Py_Initialize();
        SDL_Init( SDL_INIT_EVERYTHING );

        /* Init other Single-Instance classes.
         */
        painter = new Painter();
        inputManager = new InputManager();
    }

    Device::~Device()
    {

        /* Free up other Single-Instance classes.
         */
        delete painter;
        delete inputManager;

        /* Quit our libraries.
         */
        Py_Finalize();
        SDL_Quit();
    }

    void Device::setVideoMode( int w, int h, const char *title, bool fullscreen )
    {
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
        glOrtho( 0, screen->w, screen->h, 0, -1, 1 );
        glViewport( 0, 0, screen->w, screen->h );

        glMatrixMode( GL_MODELVIEW );

        /* Set some flags.
         */
        glEnable( GL_TEXTURE_2D );
        glEnable( GL_BLEND );
        glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
    }

    void Device::runPythonScript( const char *filename ) const
    {
        char buffer[ strlen(filename)+32 ];
        sprintf( buffer, "execfile(\"%s\")\n", filename );

        PyRun_SimpleString( buffer );
    }

    void Device::write( const char *text ) const
    {
        printf( text );
    }

    Device *getDevice()
    {
        return device;
    }

};
