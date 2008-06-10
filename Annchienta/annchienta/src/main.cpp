#include <Python.h>
#include <SDL.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

#include "engine.h"
#include "logmanager.h"
#include "auxfunc.h"

/* Forward declaration here, implementation in the
 * file generated by SWIG: annchienta_wrap.cpp
 */
extern "C" void init_annchienta(void);

Annchienta::Engine *engine;
Annchienta::LogManager *logManager;

void runGame( const char *filename, const char *modules, const char *writeDir )
{
    /* Creates a new engine, and get LogManager.
     */
    engine = Annchienta::getEngine( writeDir );
    logManager = Annchienta::getLogManager();

    /* Make sure the given filename is valid.
     */
    if( !Annchienta::isValidFile(filename) )
        logManager->error( "Could not run '%s' because it is not a valid file.", filename );

    /* Init our module.
     */
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
    char initScript[2048];

    /* Append the modules, cd to the filename path, append it
     * and then run the game.
     */
    sprintf( initScript,
"\
import sys, os\n\
\n\
# Add modules path, whiwh means we have annchienta now\n\
sys.path.append( os.path.abspath( \"%s\" )  )\n\
\n\
# Import annchienta and make write dir absolute.\n\
import annchienta\n\
engine = annchienta.getEngine()\n\
engine.setWriteDirectory( os.path.abspath( engine.getWriteDirectory() ) )\n\
\n\
# Cd to main.py file and execute.\n\
os.chdir( os.path.dirname( \"%s\" ) )\n\
execfile( os.path.basename( \"%s\" ) )\n\
",
    modules, filename, filename );

    PyRun_SimpleString( initScript );

    /* Clear up.
     */
    delete engine;
}


int main( int argc, char **argv )
{
    /* Make sure to initialize random numbers.
     */
    srand( (unsigned int)time(NULL) );

    char gameToRun[DEFAULT_STRING_SIZE];
    char moduleDir[DEFAULT_STRING_SIZE];
    char writeDir[DEFAULT_STRING_SIZE];

    /* Select default values for parameters not given.
     */
    if( argc<4 )
    {
        printf("Usage: %s gameToRun moduleDirectory writeDirectory\n", argv[0] );
        return 0;
    }

    strcpy( gameToRun, argv[1] );
    strcpy( moduleDir, argv[2] );
    strcpy( writeDir, argv[3] );

    runGame( gameToRun, moduleDir, writeDir );

    /* Return zero, everything went ok.
     */
    return 0;
};
