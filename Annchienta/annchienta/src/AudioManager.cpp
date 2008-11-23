/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
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
