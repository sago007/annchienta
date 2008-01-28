/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "tileset.h"

#include <stdio.h>
#include <string.h>
#include "surface.h"
#include "auxfunc.h"

namespace Annchienta
{

    TileSet::TileSet( const char *directory ): numberOfSurfaces(0)
    {
        char buffer[ strlen(directory)+10 ];

        do
        {
            sprintf( buffer, "%s/%d.png", directory, numberOfSurfaces++ );
        }
        while( isValidFile( buffer ) );

        numberOfSurfaces--;

        /* Allocate room for (numberOfTiles) Surface pointers.
         */
        surfaces = new Surface*[numberOfSurfaces];

        /* Load the actual surfaces.
         */
        for( int i=0; i<numberOfSurfaces; i++ )
        {
            sprintf( buffer, "%s/%d.png", directory, i );
            surfaces[i] = new Surface( buffer );
        }
    }

    TileSet::~TileSet()
    {
        for( int i=0; i<numberOfSurfaces; i++ )
            delete surfaces[i];

        delete[] surfaces;
    }

    Surface *TileSet::getSurface( int tileNumber ) const
    {
        return surfaces[ tileNumber ];
    }

};
