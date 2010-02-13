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

#ifndef ANNCHIENTA_SOUND_H
#define ANNCHIENTA_SOUND_H

#include <SDL_mixer.h>
#include "Cacheable.h"

namespace Annchienta
{
    class AudioManager;

    /** Used to hold a chunk of audio, obviously.
     */
    class Sound: public Cacheable
    {
        private:
            Mix_Chunk *chunk;
            AudioManager *audioManager;

        public:

            /** Load audio from a file.
             *  \param filename Some audio file. Format need to be supported by SDL_mixer.
             */
            Sound( const char *filename );
            virtual ~Sound();

            /** \return SoundCacheable
             */
            virtual CacheableType getCacheableType() const;

            #ifndef SWIG
                /** Plays back the sound.
                 *  \param volume Volume to play the sound at.
                 *  \note Not available in Python.
                 *  \note Use AudioManager::playSound().
                 */
                void play(Uint8 volume) const;
            #endif
    };
};

#endif
