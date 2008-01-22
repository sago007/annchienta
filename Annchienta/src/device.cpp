/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "device.h"

#include <SDL.h>
#include <GL/gl.h>

namespace Annchienta
{
    Device::Device()
    {
    }

    Device::~Device()
    {
    }

    void Device::setVideoMode( int w, int h, bool fullscreen )
    {
        /* Choose *best* settings for BitsPerPixel
         */
        Uint32 bpp = SDL_GetVideoInfo()->vfmt->BitsPerPixel;

        /* Preferred video flags
         */
        Uint32 flags = SDL_HWSURFACE | SDL_OPENGL | SDL_HWACCEL;
        if( fullscreen )
            flags |= SDL_FULLSCREEN;

        SDL_Surface *screen = SDL_SetVideoMode( w, h, bpp, flags );

        glMatrixMode( GL_PROJECTION );
        glOrtho( 0, screen->w, screen->h, 0, -1, 1 );

        glMatrixMode( GL_MODELVIEW );
    }

};
