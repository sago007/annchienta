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

        /* Init SDL_mixer and print error when failed.
         */
        if( Mix_OpenAudio( MIX_DEFAULT_FREQUENCY, MIX_DEFAULT_FORMAT, 2, 1024 ) )
            printf( "Could not init SDL_mixer: %s\n", SDL_GetError() );

        /* Initialize musicFilename.
         */
        sprintf( musicFilename, "none" );
    }

    AudioManager::~AudioManager()
    {
        /* Quit SDL_mixer.
         */
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
        /* Return if the given music is already playing.
         */
        if( !strcmp(filename, musicFilename) )
            return;

        /* Store the new filename and stop previous music
         * if needed.
         */
        sprintf( musicFilename, filename );

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
            printf( "Error - Could not open music: %s\n", filename );

        Mix_PlayMusic( music, -1 );
    }

    const char *AudioManager::getPlayingMusic() const
    {
        return musicFilename;
    }

    AudioManager *getAudioManager()
    {
        return audioManager;
    }

};
