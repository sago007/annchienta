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
            /* Load our chunk and start complaining if it failed. */
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
        /* Simply play once, automatically choose any
         * free channel to play it on. */
        if( audioManager->inittedSuccesfully() )
            Mix_PlayChannel( -1, chunk, 0 );
    }

};
