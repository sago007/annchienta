/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "engine.h"

#include <SDL.h>
#include <GL/gl.h>
#include <Python.h>

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
    }

    void Engine::runPythonScript( const char *filename ) const
    {
        char buffer[ strlen(filename)+32 ];
        sprintf( buffer, "execfile(\"%s\")\n", filename );

        PyRun_SimpleString( buffer );
    }

    void Engine::write( const char *text ) const
    {
        printf( text );
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

    bool Engine::evaluatePythonBoolean( const char *start, const char *conditional )
    {
        const char script[] = "import annchienta\n%s\nannchienta.getEngine().setPythonBoolean(%s)\n";
        char code[ strlen(script) + strlen( start ) + strlen( conditional ) + 4 ];
        sprintf( code, script, start, conditional );
        PyRun_SimpleString( code );
        return pythonBoolean;
    }

    Engine *getEngine()
    {
        if( !engine )
            return (engine = new Engine);
        return engine;
    }

};
