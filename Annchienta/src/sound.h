/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_SOUND_H
#define ANNCHIENTA_SOUND_H

#include <SDL_mixer.h>

namespace Annchienta
{
    class Sound
    {
        private:
            Mix_Chunk *chunk;

        public:
            Sound( const char *filename );
            ~Sound();

            #ifndef SWIG
                void play() const;
            #endif
    };
};

#endif
