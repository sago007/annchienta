/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_AUDIOMANAGER_H
#define ANNCHIENTA_AUDIOMANAGER_H

namespace Annchienta
{

    class Sound;

    class AudioManager
    {
        private:

        public:
            #ifndef SWIG
                AudioManager();
                ~AudioManager();
            #endif

            void playSound( Sound *sound ) const;

    };

    AudioManager *getAudioManager();

};

#endif
