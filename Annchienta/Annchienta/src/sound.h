/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_SOUND_H
#define ANNCHIENTA_SOUND_H

#include <SDL_mixer.h>

namespace Annchienta
{
    /** Used to hold a chunk of audio, obviously.
     */
    class Sound
    {
        private:
            Mix_Chunk *chunk;

        public:

            /** Load audio from a file.
             *  \param filename Some audio file. Format need to be supported by SDL_mixer.
             */
            Sound( const char *filename );
            ~Sound();

            #ifndef SWIG
                /** Plays back the sound.
                 *  \note Not available in Python.
                 *  \note Use AudioManager::playSound().
                 */
                void play() const;
            #endif
    };
};

#endif
