/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "device.h"

#include <SDL.h>
#include <GL/gl.h>
#include <Python.h>

#include "videomanager.h"
#include "inputmanager.h"

namespace Annchienta
{
    Device *device;

    Device::Device()
    {
        /* Set global device...
         */
        device = this;

        /* Init some things...
         */
        Py_Initialize();
        SDL_Init( SDL_INIT_EVERYTHING );

        /* Init other Single-Instance classes.
         */
        videoManager = new VideoManager();
        inputManager = new InputManager();
    }

    Device::~Device()
    {

        /* Free up other Single-Instance classes.
         */
        delete videoManager;
        delete inputManager;

        /* Quit our libraries.
         */
        Py_Finalize();
        SDL_Quit();
    }

    void Device::runPythonScript( const char *filename ) const
    {
        char buffer[ strlen(filename)+32 ];
        sprintf( buffer, "execfile(\"%s\")\n", filename );

        PyRun_SimpleString( buffer );
    }

    void Device::write( const char *text ) const
    {
        printf( text );
    }

    Device *getDevice()
    {
        return device;
    }

};
