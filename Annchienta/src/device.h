/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_DEVICE_H
#define ANNCHIENTA_DEVICE_H

namespace Annchienta
{

    class Painter;
    class InputManager;

    class Device
    {
        private:
            Painter *painter;
            InputManager *inputManager;

        public:
            #ifndef SWIG
                Device();
                ~Device();
            #endif

            void setVideoMode( int w, int h, bool fullscreen=false );

    };

    Device *getDevice();
};

#endif
