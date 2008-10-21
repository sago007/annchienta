/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_ENGINE_H
#define ANNCHIENTA_ENGINE_H

#define SMALL_STRING_SIZE 128
#define DEFAULT_STRING_SIZE 512
#define LARGE_STRING_SIZE 1024

namespace Annchienta
{

    class LogManager;
    class VideoManager;
    class InputManager;
    class MapManager;
    class AudioManager;
    class CacheManager;
    class MathManager;

    /** This is a class that holds most other classes and some
     *  general engine functionality. To obtain it, use
     *  getEngine()
     */
    class Engine
    {
        private:
            LogManager *logManager;
            VideoManager *videoManager;
            InputManager *inputManager;
            MapManager *mapManager;
            AudioManager *audioManager;
            CacheManager *cacheManager;
            MathManager *mathManager;

            char writeDirectory[DEFAULT_STRING_SIZE];

            bool pythonBoolean;

        public:
            #ifndef SWIG
                /** Write directory is the directory where files such
                 *  as save files and logs will be placed.
                 */
                Engine( const char *writeDirectory="." );
                ~Engine();

                /** Safe method for running Python scripts.
                 *  \param filename The script to be ran.
                 *  \note Not available in Python.
                 */
                void runPythonScript( const char *filename ) const;

                /** Returns the value of a Python boolean expression.
                 *  an example could be
                 *  \code engine->evaluatePythonBoolean( "a=3", "a>1" ); \endcode
                 *  \param code Code to be executed before checking the boolean value.
                 *  \param conditional The boolean expression.
                 *  \note Not available in Python.
                 */
                bool evaluatePythonBoolean( const char *code, const char *conditional );

                /** Converts a string to proper Python code. For now,
                 *  this means removing extra spaces at the end.
                 *  \param code Code to be converted.
                 *  \note Not available in Python.
                 */
                void toPythonCode( char **code );
            #endif

            /** Finds out the writing directory. This should be used
             *  if you want to know where to place save files etc.
             */
            const char *getWriteDirectory() const;

            /** Use with care!!! */
            void setWriteDirectory( const char* );
            
            /** This simply writes some text to stdout. This is
             *  preferred to the default Python "print" function
             *  because that might be unsafe on certain operating
             *  systems.
             *  \param text The string to write.
             */
            void write( const char *text ) const;

            /** Checks if the given file exists and can be read.
             *  \param filename File to be checked.
             *  \return If the file can be accessed.
             */
            bool isValidFile( const char *filename ) const;

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

    /* Starts the engine. Call this before using any functions from the
     * annchienta module.
     * \param writeDir path to directory where temporary log files can be placed.
     */
    void init( const char *writeDir="." );
    
    /** Quits and deletes the engine. Call this at the end of your game...
     */
    void quit();

    /** Returns the global engine.
     */
    Engine *getEngine();
};

#endif

