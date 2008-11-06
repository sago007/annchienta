/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "AudioManager.h"

#include "Sound.h"
#include "LogManager.h"

namespace Annchienta
{
    AudioManager *audioManager;

    AudioManager::AudioManager(): music(0)
    {
        /* Set reference to single-instance class.
         */
        audioManager = this;

        /* Init SDL_mixer and print error when failed.
         */
        if( Mix_OpenAudio( MIX_DEFAULT_FREQUENCY, MIX_DEFAULT_FORMAT, 2, 1024 ) )
        {
            getLogManager()->warning( "Could not init SDL_mixer: '%s'.", SDL_GetError() );
            initted = false;
        }
        else
        {
            getLogManager()->message( "Succesfully started AudioManager." );
            initted = true;
        }

        /* Initialize musicFileName.
         */
        sprintf( musicFileName, "none" );
    }

    AudioManager::~AudioManager()
    {
        getLogManager()->message( "Deleting AudioManager..." );

        /* Quit SDL_mixer.
         */
        if( initted )
            Mix_CloseAudio();
    }

    Mix_Music *AudioManager::getMusic() const
    {
        return music;
    }

    bool AudioManager::inittedSuccesfully() const
    {
        return initted;
    }

    void AudioManager::playSound( Sound *sound ) const
    {
        if( initted )
            sound->play();
    }

    void AudioManager::playMusic( const char *filename )
    {
        /* Return if the given music is already playing.
         */
        if( !strcmp(filename, musicFileName) )
            return;

        /* Store the new filename and stop previous music
         * if needed.
         */
        sprintf( musicFileName, filename );

        if( !initted )
            return;

        if( Mix_PlayingMusic() )
            Mix_FadeOutMusic( 100 );

        if( music )
        {
            Mix_FreeMusic( music );
            music = 0;
        }

        /* Load the new music and play it, endlessly looping.
         */
        music = Mix_LoadMUS( filename );
        if( !music )
            getLogManager()->error( "Could not open music: '%s'.", filename );

        Mix_PlayMusic( music, -1 );
    }

    const char *AudioManager::getPlayingMusic() const
    {
        return musicFileName;
    }

    AudioManager *getAudioManager()
    {
        return audioManager;
    }

};
