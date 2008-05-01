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

    /** This is a class that holds most other classes and some
     *  general engine functionality. To obtain it, use
     *  getEngine()
     */
    class Engine
    {
        private:
            VideoManager *videoManager;
            InputManager *inputManager;
            MapManager *mapManager;
            AudioManager *audioManager;
            CacheManager *cacheManager;

            bool pythonBoolean;

        public:
            #ifndef SWIG
                Engine();
                ~Engine();

                /** Safe method for running Python scripts.
                 *  \note Not available in Python.
                 *  \param filename The script to be ran.
                 */
                void runPythonScript( const char *filename ) const;

                /** Returns the value of a Python boolean expression.
                 *  an example could be
                 *  \code engine->evaluatePythonBoolean( "a=3", "a>1" ); \endcode
                 *  \param code Code to be executed before checking the boolean value.
                 *  \param conditional The boolean expression.
                 */
                bool evaluatePythonBoolean( const char *code, const char *conditional );

                /** Converts a string to proper Python code. For now,
                 *  this means removing extra spaces at the end.
                 *  \param code Code to be converted.
                 */
                void toPythonCode( char **code );
            #endif

            /** This simply writes some text to stdout. This is
             *  preferred to the default Python "print" function
             *  because that might be unsafe on certain operating
             *  systems.
             *  \param text The string to write.
             */
            void write( const char *text ) const;

            /** Sets the window caption.
             *  \param title The new window caption.
             */
            void setWindowTitle( const char *title ) const;

            /** Get the time since the engine was initted.
             *  \return The number of milliseconds passed since initting.
             */
            unsigned int getTicks() const;

            /** Waits a time and then returns.
             *  \param ms Number of milliseconds to wait.
             */
            void delay( int ms ) const;

            /** Used by evaluatePythonBoolean(). I can't imagine
             *  this is needed in any other situation, so don't use
             *  it.
             */
            void setPythonBoolean( bool b );
    };

    Engine *getEngine();
};

#endif
