#include <Python.h>
#include <SDL.h>
#include <time.h>
#include <stdlib.h>

#include "engine.h"

extern "C" void init_annchienta(void);

int main( int argc, char **argv )
{
    srand( time(NULL) );

    Annchienta::Engine *engine = new Annchienta::Engine();

    char gameToRun[512];

    if( argc<2 )
        strcpy( gameToRun, "../games/default.py" );
    else
        strcpy( gameToRun, argv[1] );

    init_annchienta();

    /* Some strange error regarding paths and not finding the right
     * custom modules when not using shared ones, but this harmless
     * piece of code fixes it: it adds the current working directory
     * to the "path"... while it should already be there. Not running
     * this will result in an error, though.
     */
    PyRun_SimpleString( "from sys import path\nfrom os import getcwdu\npath.append( getcwdu() )" );

    /* Run our game.
     */
    engine->runPythonScript( gameToRun );
 
    delete engine;

};
