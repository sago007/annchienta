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

#include "Engine.h"

#include <SDL.h>
#include <SDL_opengl.h>
#include <Python.h>
#include <cstdio>
#include <cstdlib>
#include <ctime>

#include "LogManager.h"
#include "VideoManager.h"
#include "InputManager.h"
#include "MapManager.h"
#include "AudioManager.h"
#include "CacheManager.h"
#include "MathManager.h"

namespace Annchienta
{
    Engine *engine = 0;

    Engine::Engine( const char *_writeDirectory )
    {
        /* Store write directory. */
        sprintf( writeDirectory, "%s/", _writeDirectory );

        /* Set global engine... */
        engine = this;

        /* Init some things... */
        Py_Initialize();
        SDL_Init( SDL_INIT_EVERYTHING );

        /* Create a filename in our writeDirectory. */
        char logFile[DEFAULT_STRING_SIZE];
        sprintf( logFile, "%slog.txt", writeDirectory ); 

        /* Init other Single-Instance classes. */
        logManager = new LogManager( logFile );
        videoManager = new VideoManager();
        inputManager = new InputManager();
        mapManager = new MapManager();
        audioManager = new AudioManager();
        cacheManager = new CacheManager();
        mathManager = new MathManager();
    }

    Engine::~Engine()
    {
        /* Free up other Single-Instance classes. */
        delete videoManager;
        delete inputManager;
        delete mapManager;
        delete audioManager;
        delete cacheManager;
        delete mathManager;

        /* Quit our libraries.
         */
        SDL_Quit();

        /* LogManager goes last because errors might have
         * happened in the other delete statements, and
         * we want all errors to be reported.
         */
        delete logManager;
    }

    void Engine::runPythonCode( const char *code ) const
    {
        PyRun_SimpleString( code );
    }

    void Engine::runPythonScript( const char *filename ) const
    {
        char buffer[ LARGE_STRING_SIZE ];
        sprintf( buffer, "ann_scriptFile=open(\"%s\",'r')\nexec(ann_scriptFile)\nann_scriptFile.close()\n", filename );

        runPythonCode( buffer );
    }

    bool Engine::evaluatePythonBoolean( const char *start, const char *conditional )
    {
        const char script[] = "import annchienta\n%s\nannchienta.getEngine().setPythonBoolean(%s)\n";
        char code[ LARGE_STRING_SIZE ];
        sprintf( code, script, start, conditional );
        runPythonCode( code );
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
        printf( "%s\n", text );
    }

    bool Engine::isValidFile( const char *filename ) const
    {
        FILE *f = fopen( filename, "r" );

        if( f==NULL )
            return false;

        fclose( f );
        return true;
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

