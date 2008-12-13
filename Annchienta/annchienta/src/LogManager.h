/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
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

            /** Whether the logManager should log to a file
             *  or to stdout.
             */
            bool m_logToFile;

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

            /** Makes the Logger log to a file instead of to
             *  stdout. Disabled by default.
             *  \param value If the LogManager should log to a file.
             */
            bool logToFile( bool value );

            /** Checks if the Logger should log to a file.
             *  \return If the Logger logs to a file.
             */
            bool isLogToFile() const;

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
