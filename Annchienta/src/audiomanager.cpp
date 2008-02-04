/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "audiomanager.h"

#include "sound.h"

namespace Annchienta
{
    AudioManager *audioManager;

    AudioManager::AudioManager(): music(0)
    {
        /* Set reference to single-instance class.
         */
        audioManager = this;

        if( Mix_OpenAudio( MIX_DEFAULT_FREQUENCY, MIX_DEFAULT_FORMAT, 2, 1024 ) )
            printf( "Could not init SDL_mixer: %s\n", SDL_GetError() );

        sprintf( musicFilename, "none" );
    }

    AudioManager::~AudioManager()
    {
        Mix_CloseAudio();
    }

    Mix_Music *AudioManager::getMusic() const
    {
        return music;
    }

    void AudioManager::playSound( Sound *sound ) const
    {
        sound->play();
    }

    void AudioManager::playMusic( const char *filename )
    {
        if( !strcmp(filename, musicFilename) )
            return;

        sprintf( musicFilename, filename );

        if( Mix_PlayingMusic() )
            Mix_FadeOutMusic( 100 );

        if( music )
        {
            Mix_FreeMusic( music );
            music = 0;
        }

        music = Mix_LoadMUS( filename );
        if( !music )
            printf( "Error - Could not open music: %s\n", filename );

        Mix_PlayMusic( music, -1 );
    }

    AudioManager *getAudioManager()
    {
        return audioManager;
    }

};
