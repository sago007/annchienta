/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_LOGMANAGER_H
#define ANNCHIENTA_LOGMANAGER_H

#include <cstdio>

namespace Annchienta
{
    /** This is a class used to place stuff in the
     *  log file.
     */
    class LogManager
    {
        private:
            /** File everything will be written to.
             */
            FILE *logFile;

            /** Whether the LogManager should log or not.
             */
            bool enabled;

        public:
            #ifndef SWIG
                LogManager( const char *fileName = "log.txt" );
                ~LogManager();
            #endif

            /** Enables or disables the logger. The logger is
             *  enabled by default.
             *  \param enableLogger If the LogManager should log.
             */
            void enable( bool enableLogger );

            /** Checks if the logger is enabled.
             *  \return If the LogManager is enabled.
             */
            bool isEnabled() const;

            /** Prints a message to the log file.
             *  \param fmt Text, like passed to prinf in C.
             */
            void message( const char *fmt, ... );

            /** Prints a warning to the log file.
             *  \param fmt Text, like passed to prinf in C.
             */
            void warning( const char *fmt, ... );

            /** Prints an error to the log file. And stops
             *  the engine.
             *  \param fmt Text, like passed to prinf in C.
             */
            void error( const char *fmt, ... );

    };

    /** Retrieve the global LogManager instance.
     */
    LogManager *getLogManager();

};

#endif
