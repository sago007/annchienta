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
#include "font.h"

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
        cacheManager = new CacheManager();

        defaultFont = new Font("../data/defaultFont.ttf", 14);
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

        delete defaultFont;

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

    Font *Engine::getDefaultFont() const
    {
        return defaultFont;
    }

    Engine *getEngine()
    {
        return engine;
    }

};
