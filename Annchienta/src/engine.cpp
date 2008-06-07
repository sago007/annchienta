/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "engine.h"

#include <SDL.h>
#include <GL/gl.h>
#include <Python.h>

#include "logmanager.h"
#include "videomanager.h"
#include "inputmanager.h"
#include "mapmanager.h"
#include "audiomanager.h"
#include "cachemanager.h"

namespace Annchienta
{
    Engine *engine = 0;

    Engine::Engine()
    {
        /* Set global engine...
         */
        engine = this;

        /* Init some things...
         */
        Py_Initialize();
        SDL_Init( SDL_INIT_EVERYTHING );

        /* Init other Single-Instance classes.
         */
        logManager = new LogManager();
        videoManager = new VideoManager();
        inputManager = new InputManager();
        mapManager = new MapManager();
        audioManager = new AudioManager();
        cacheManager = new CacheManager();
    }

    Engine::~Engine()
    {
        /* Free up Python stuff first.
         */
        Py_Finalize();

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
        char buffer[ strlen(filename)+32 ];
        sprintf( buffer, "execfile(\"%s\")\n", filename );

        PyRun_SimpleString( buffer );
    }


    bool Engine::evaluatePythonBoolean( const char *start, const char *conditional )
    {
        const char script[] = "import annchienta\n%s\nannchienta.getEngine().setPythonBoolean(%s)\n";
        char code[ strlen(script) + strlen( start ) + strlen( conditional ) + 4 ];
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

    Engine *getEngine()
    {
        if( !engine )
            return (engine = new Engine);
        return engine;
    }

};
