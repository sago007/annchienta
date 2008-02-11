#include <Python.h>
#include <SDL.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

#include "engine.h"
#include "editor.h"

extern "C" void init_annchienta(void);

Annchienta::Engine *engine;

void runGame( const char *filename )
{

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
sys.path.append( os.path.dirname( \"%s\" ) )\n\
os.chdir( os.path.dirname( \"%s\" ) )\n\
execfile( os.path.basename( \"%s\" ) )\n\
",
    filename, filename, filename );

    PyRun_SimpleString( initScript );

    /* Run our game.
     */
    //engine->runPythonScript( filename );
}

void runEditor( int argc, char **argv )
{
    Annchienta::Editor *editor;
    if( (argc != 3) && (argc != 8) )
    {
        printf("Usage: ./annchienta -e [filename]\nor\n./annchienta -e [filename] [tilewidth] [tileheight] [mapwidth] [mapheight] [tileset]\n");
        return;
    }
    else
    {
        if( argc==3 )
            editor = new Annchienta::Editor( argv[2] );
        else
            editor = new Annchienta::Editor( argv[2], atoi(argv[3]), atoi(argv[4]), atoi(argv[5]), atoi(argv[6]), argv[7] );
    }

    editor->run();

    delete editor;
}

int main( int argc, char **argv )
{
    srand( time(NULL) );

    engine = new Annchienta::Engine();

    char gameToRun[512];

    if( argc>=2 && !strcmp("-e", argv[1]) )
    {
        runEditor( argc, argv );
    }
    else
    {
        if( argc<2 )
            strcpy( gameToRun, "../games/default.py" );
        else
            strcpy( gameToRun, argv[1] );
    
        runGame( gameToRun );
    }

    delete engine;

};
