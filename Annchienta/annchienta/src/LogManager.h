/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_LOGMANAGER_H
#define ANNCHIENTA_LOGMANAGER_H

#include <cstdio>

namespace Annchienta
{
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
             */
            void enable( bool e );

            /** Checks if the logger is enabled.
             */
            bool isEnabled() const;

            /** Prints a message to the log file.
             */
            void message( const char *fmt, ... );

            /** Prints a warning to the log file.
             */
            void warning( const char *fmt, ... );

            /** Quits with the given error in the log file.
             */
            void error( const char *fmt, ... );

    };

    LogManager *getLogManager();

};

#endif
