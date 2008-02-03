/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "sound.h"

namespace Annchienta
{

    Sound::Sound( const char *filename )
    {
        chunk = Mix_LoadWAV( filename );
        if( !chunk )
            printf("Error - could not open %s as sound.\n", filename );
    }

    Sound::~Sound()
    {
        Mix_FreeChunk( chunk );
    }

    void Sound::play() const
    {
        Mix_PlayChannel( -1, chunk, 0 );
    }

};
