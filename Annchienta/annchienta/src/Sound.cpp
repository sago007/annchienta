/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "Sound.h"
#include "LogManager.h"
#include "AudioManager.h"

namespace Annchienta
{

    Sound::Sound( const char *filename )
    {
        audioManager = getAudioManager();

        if( audioManager->inittedSuccesfully() )
        {
            chunk = Mix_LoadWAV( filename );
            if( !chunk )
                getLogManager()->error( "Could not open '%s' as sound.", filename );
        }
    }

    Sound::~Sound()
    {
        if( audioManager->inittedSuccesfully() )
            Mix_FreeChunk( chunk );
    }

    void Sound::play() const
    {
        if( audioManager->inittedSuccesfully() )
            Mix_PlayChannel( -1, chunk, 0 );
    }

};
