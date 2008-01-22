/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_DEVICE_H
#define ANNCHIENTA_DEVICE_H

namespace Annchienta
{
    class Device
    {
        private:

        public:
            Device();
            ~Device();

            void setVideoMode( int w, int h, bool fullscreen );

    };
};

#endif
