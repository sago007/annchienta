/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "engine.h"

#include <SDL.h>
#include <SDL_opengl.h>
#include <Python.h>
#include <stdio.h>

#include "logmanager.h"
#include "videomanager.h"
#include "inputmanager.h"
#include "mapmanager.h"
#include "audiomanager.h"
#include "cachemanager.h"

namespace Annchienta
{
    Engine *engine = 0;

    /* When we really want to stop...
     */
    Uint32 forcedExitCallback( Uint32 interval, void *param )
    {
        getLogManager()->warning("Grace period for Py_Finalize() exceeded... forcing exit.");

        /* Try to free a little anyway so we don't waste too much.
         */
        delete getVideoManager();
        delete getInputManager();
        delete getMapManager();
        delete getAudioManager();
        delete getCacheManager();
        SDL_Quit();

        exit(0);
        return interval;
    }

    Engine::Engine( const char *_writeDirectory )
    {
        /* Store write directory.
         */
        sprintf( writeDirectory, "%s/", _writeDirectory );

        /* Set global engine...
         */
        engine = this;

        /* Init some things...
         */
        Py_Initialize();
        SDL_Init( SDL_INIT_EVERYTHING );

        /* Create a filename in our writeDirectory.
         */
        char logFile[DEFAULT_STRING_SIZE];
        sprintf( logFile, "%slog.txt", writeDirectory ); 

        /* Init other Single-Instance classes.
         */
        logManager = new LogManager( logFile );
        videoManager = new VideoManager();
        inputManager = new InputManager();
        mapManager = new MapManager();
        audioManager = new AudioManager();
        cacheManager = new CacheManager();
    }

    Engine::~Engine()
    {
        /* Free up other Single-Instance classes.
         */
        delete videoManager;
        delete inputManager;
        delete mapManager;
        delete audioManager;
        delete cacheManager;

        /* Quit our libraries.
         */
        SDL_Quit();

        /* LogManager goes last because errors might have
         * happened in the other delete statements, and
         * we want all errors to be reported.
         */
        delete logManager;
    }

    void Engine::runPythonScript( const char *filename ) const
    {
        char buffer[ DEFAULT_STRING_SIZE ];
        sprintf( buffer, "execfile(\"%s\")\n", filename );

        PyRun_SimpleString( buffer );
    }


    bool Engine::evaluatePythonBoolean( const char *start, const char *conditional )
    {
        const char script[] = "import annchienta\n%s\nannchienta.getEngine().setPythonBoolean(%s)\n";
        char code[ LARGE_STRING_SIZE ];
        sprintf( code, script, start, conditional );
        PyRun_SimpleString( code );
        return pythonBoolean;
    }

    void Engine::toPythonCode( char **strptr )
    {
        /* Remove spaces on the end.
         */
        int newLength = strlen(*strptr);
        for( int i=newLength-1; i>=0; i-- )
            if( isspace( (*strptr)[i] ) )
                newLength--;
            else
                i = -1;

        char *newCode = new char[newLength+1];
        strncpy( newCode, *strptr, newLength );
        newCode[ newLength ] = '\0';
        delete[] *strptr;
        *strptr = newCode;
    }

    const char *Engine::getWriteDirectory() const
    {
        return writeDirectory;
    }

    void Engine::setWriteDirectory( const char *wd )
    {
        sprintf( writeDirectory, "%s/", wd );
    }
    
    void Engine::write( const char *text ) const
    {
        printf( text );
        printf( "\n" );
    }

    void Engine::setWindowTitle( const char *title ) const
    {
        SDL_WM_SetCaption( title, NULL );
    }

    unsigned int Engine::getTicks() const
    {
        return SDL_GetTicks();
    }

    void Engine::delay( int ms ) const
    {
        if( ms>0 )
            SDL_Delay( ms );
    }

    void Engine::setPythonBoolean( bool b )
    {
        pythonBoolean = b;
    }

    void init( const char *writeDir )
    {
        engine = new Engine( writeDir );
    }
    
    void quit()
    {
        delete engine;
    }

    Engine *getEngine()
    {
        return engine;
    }

};

