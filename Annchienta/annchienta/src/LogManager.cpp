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

#include "LogManager.h"

#include <cstdlib>
#include <cstdarg>

namespace Annchienta
{
    LogManager *logManager;

    LogManager::LogManager( const char *filename )
    {
        /* Set reference to single-instance class.
         */
        logManager = this;

        logFile = fopen( filename, "w" );

        if( !logFile )
            printf( "Could not open log file %s for writing.\n", filename );
        else
            message( "Succesfully started LogManager." );

        enabled = true;
    }

    LogManager::~LogManager()
    {
        message( "Deleting LogManager..." );
        fclose( logFile );
    }

    void LogManager::enable( bool e )
    {
        enabled = e;
    }

    bool LogManager::isEnabled() const
    {
        return enabled;
    }

    void LogManager::message( const char *fmt, ... )
    {
        va_list arg;

        va_start( arg, fmt );

        if( logFile )
        {
            fprintf( logFile, "Message - " );
            vfprintf( logFile, fmt, arg );
            fprintf( logFile, "\n" );
            fflush( logFile );
        }

        va_end( arg );
    }

    void LogManager::warning( const char *fmt, ... )
    {
        va_list arg;

        va_start( arg, fmt );

        if( logFile )
        {
            fprintf( logFile, "Warning - " );
            vfprintf( logFile, fmt, arg );
            fprintf( logFile, "\n" );
            fflush( logFile );
        }

        va_end( arg );
    }

    void LogManager::error( const char *fmt, ... )
    {
        va_list arg;

        va_start( arg, fmt );

        if( logFile )
        {
            fprintf( logFile, "Error - " );
            vfprintf( logFile, fmt, arg );
            fprintf( logFile, "\n" );
            fflush( logFile );
            fclose( logFile );
        }

        va_end( arg );

        exit(1);
    }

    LogManager *getLogManager()
    {
        return logManager;
    }

};
