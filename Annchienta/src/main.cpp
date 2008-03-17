#include <Python.h>
#include <SDL.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

#include "engine.h"
#include "auxfunc.h"

extern "C" void init_annchienta(void);

Annchienta::Engine *engine;

void runGame( const char *filename )
{

    if( !Annchienta::isValidFile(filename) )
    {
        printf( "Could not run %s because it is not a valid file.\n", filename );
        return;
    }

    init_annchienta();

    /* Some strange error regarding paths and not finding the right
     * custom modules when not using shared ones, but this harmless
     * piece of code fixes it: it adds the current working directory
     * to the "path"... while it should already be there. Not running
     * this will result in an error, though.
     *
     * Then, we set the current working directory to the one in which
     * the game script is located.
     */
    char initScript[1024];

    sprintf( initScript,
"\
import sys\n\
import os\n\
\n\
sys.path.append( os.path.abspath( os.getcwdu() ) )\n\
os.chdir( os.path.dirname( \"%s\" ) )\n\
sys.path.append( os.path.abspath( os.getcwdu() ) )\n\
execfile( os.path.basename( \"%s\" ) )\n\
",
    filename, filename );

    PyRun_SimpleString( initScript );

    /* Run our game.
     */
    //engine->runPythonScript( filename );
}


int main( int argc, char **argv )
{
    srand( time(NULL) );

    engine = new Annchienta::Engine();

    char gameToRun[512];

    if( argc<2 )
        strcpy( gameToRun, "../games/test/main.py" );
    else
        strcpy( gameToRun, argv[1] );

    runGame( gameToRun );

    delete engine;

};
