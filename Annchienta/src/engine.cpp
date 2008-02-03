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

namespace Annchienta
{
    Engine *engine;

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
    }

    Engine::~Engine()
    {

        /* Free up other Single-Instance classes.
         */
        delete videoManager;
        delete inputManager;
        delete mapManager;
        delete audioManager;

        /* Quit our libraries.
         */
        Py_Finalize();
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

    Engine *getEngine()
    {
        return engine;
    }

};
