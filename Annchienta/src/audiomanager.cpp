/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "audiomanager.h"

#include "sound.h"

namespace Annchienta
{
    AudioManager *audioManager;

    AudioManager::AudioManager()
    {
        /* Set reference to single-instance class.
         */
        audioManager = this;

        if( Mix_OpenAudio( MIX_DEFAULT_FREQUENCY, MIX_DEFAULT_FORMAT, 2, 1024 ) )
            printf( "Could not init SDL_mixer: %s\n", SDL_GetError() );
    }

    AudioManager::~AudioManager()
    {
        Mix_CloseAudio();
    }

    void AudioManager::playSound( Sound *sound ) const
    {
        sound->play();
    }

    AudioManager *getAudioManager()
    {
        return audioManager;
    }

};
