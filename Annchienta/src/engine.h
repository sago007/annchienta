/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_ENGINE_H
#define ANNCHIENTA_ENGINE_H

namespace Annchienta
{

    class VideoManager;
    class InputManager;
    class MapManager;
    class AudioManager;
    class CacheManager;

    class Engine
    {
        private:
            VideoManager *videoManager;
            InputManager *inputManager;
            MapManager *mapManager;
            AudioManager *audioManager;
            CacheManager *cacheManager;

        public:
            #ifndef SWIG
                Engine();
                ~Engine();
                void runPythonScript( const char *filename ) const;
            #endif

            /** Simply prints some text to stdout. This should be preferred
             *  over the regular Python 'print' statement, because else, the
             *  text might not appear when compiled under certain conditions.
             */
            void write( const char *text ) const;

            void setWindowTitle( const char *title ) const;

            unsigned int getTicks() const;

    };

    Engine *getEngine();
};

#endif
