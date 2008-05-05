#include <Python.h>
#include <SDL.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

#include "engine.h"
#include "auxfunc.h"

extern "C" void init_annchienta(void);

Annchienta::Engine *engine;

void runGame( const char *filename, const char *modules )
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
\n\
sys.path.append( \"%s\" )\n\
\
import os\n\
sys.path.append( os.path.abspath( \"%s\" )  )\n\
sys.path.append( os.path.abspath( os.getcwdu() ) )\n\
os.chdir( os.path.dirname( \"%s\" ) )\n\
sys.path.append( os.path.abspath( os.getcwdu() ) )\n\
execfile( os.path.basename( \"%s\" ) )\n\
",
    modules, modules, filename, filename );

    PyRun_SimpleString( initScript );

    /* Show debugging information.
     */
    if( PyErr_Occurred() )
        PyErr_Print();
}


int main( int argc, char **argv )
{
    srand( time(NULL) );

    /* Creates a new one.
     */
    engine = Annchienta::getEngine();

    char gameToRun[512];
    char moduleDir[512];

    /* Select default values for parameters not given.
     */
    if( argc<2 )
        strcpy( gameToRun, "../games/elegiac_convergence/main.py" );
    else
        strcpy( gameToRun, argv[1] );

    if( argc<3 )
        strcpy( moduleDir, "../modules" );
    else
        strcpy( moduleDir, argv[2] );

    runGame( gameToRun, moduleDir );

    delete engine;

};
