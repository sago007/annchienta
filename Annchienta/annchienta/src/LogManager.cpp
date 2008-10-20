/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
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
