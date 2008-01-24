/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_DEVICE_H
#define ANNCHIENTA_DEVICE_H

namespace Annchienta
{

    class VideoManager;
    class InputManager;

    class Device
    {
        private:
            VideoManager *videoManager;
            InputManager *inputManager;

        public:
            #ifndef SWIG
                Device();
                ~Device();
            #endif

            /** Simply does what PyRun_SimpleFile does, but this is a
             *  safer way...
             */
            void runPythonScript( const char *filename ) const;

            /** Simply prints some text to stdout. This should be preferred
             *  over the regular Python 'print' statement, because else, the
             *  text might not appear when compiled under certain conditions.
             */
            void write( const char *text ) const;

    };

    Device *getDevice();
};

#endif
