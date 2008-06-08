/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "sound.h"
#include "logmanager.h"

namespace Annchienta
{

    Sound::Sound( const char *filename )
    {
        chunk = Mix_LoadWAV( filename );
        if( !chunk )
            getLogManager()->error( "Could not open '%s' as sound.", filename );
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
