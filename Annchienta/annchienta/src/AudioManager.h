/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
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
            char musicFilename[DEFAULT_STRING_SIZE];

            /* We can continue happily without audio.
             */
            bool initted;

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
    };

    AudioManager *getAudioManager();

};

#endif
