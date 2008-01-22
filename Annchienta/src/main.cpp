#include <Python.h>
#include <SDL.h>

extern "C" void init_annchienta(void);

int main( int argc, char **argv )
{
    /* Init various things.
     */
    Py_Initialize();
    SDL_Init( SDL_INIT_EVERYTHING );

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

    /* Open the file for reading.
     */
    FILE *f = fopen( gameToRun, "r" );

    /* Run it...
     */
    PyRun_SimpleFile( f, gameToRun );

    /* Make sure we close the file we opened.
     */
    fclose( f );

    /* Quit the things we initialized.
     */
    Py_Finalize();
    SDL_Quit();

};
