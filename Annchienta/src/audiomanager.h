/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_AUDIOMANAGER_H
#define ANNCHIENTA_AUDIOMANAGER_H

#include <SDL_mixer.h>

namespace Annchienta
{

    class Sound;

    class AudioManager
    {
        private:
            Mix_Music *music;
            char musicFilename[512];

        public:
            #ifndef SWIG
                AudioManager();
                ~AudioManager();
                Mix_Music *getMusic() const;
            #endif

            void playSound( Sound *sound ) const;
            void playMusic( const char *filename );

            const char *getPlayingMusic() const;
    };

    AudioManager *getAudioManager();

};

#endif
