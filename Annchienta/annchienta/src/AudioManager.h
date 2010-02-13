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

#ifndef ANNCHIENTA_AUDIOMANAGER_H
#define ANNCHIENTA_AUDIOMANAGER_H

#include <SDL_mixer.h>
#include "Engine.h"

namespace Annchienta
{

    class Sound;

    /** Used for playing audio and music.
     */
    class AudioManager
    {
        private:
            Mix_Music *music;
            char musicFileName[DEFAULT_STRING_SIZE];

            /* We can continue happily without audio.
             */
            bool initted;

            Uint8 volume;

        public:
            #ifndef SWIG
                AudioManager();
                ~AudioManager();

                /** \return The playing music.
                 *  \note Not available in Python.
                 */
                Mix_Music *getMusic() const;
            #endif

            /** Checks if the AudioManager was succesfully
             *  initted.
             */
            bool inittedSuccesfully() const;

            /** Play back a loaded Sound.
             *  \param sound Sound to play.
             */
            void playSound( Sound *sound ) const;

            /** Starts streaming background music. When the file
             *  given is already playing, nothing will happen. If
             *  other music is already playing, that music will be
             *  stopped first.
             *  \param filename Music to stream.
             */
            void playMusic( const char *filename );

            /** \return Filename of the music currently streaming.
             */
            const char *getPlayingMusic() const;

            /** Sets the audo volume.
             *  \param volume The new volume, in [0, 1].
             */
            void setVolume( float volume );
    };

    AudioManager *getAudioManager();

};

#endif
