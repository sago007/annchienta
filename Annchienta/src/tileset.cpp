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

    TileSet::TileSet( const char *directory ): numberOfSurfaces(0), numberOfSideSurfaces(0)
    {
        char buffer[ strlen(directory)+16 ];

        /* Count the regular surfaces.
         */
        do
        {
            sprintf( buffer, "%s/%d.png", directory, ++numberOfSurfaces );
        }
        while( isValidFile( buffer ) );

        /* Allocate room for (numberOfTiles) Surface pointers.
         */
        surfaces = new Surface*[numberOfSurfaces];

        /* Load the actual surfaces.
         */
        surfaces[0] = 0;

        for( int i=1; i<numberOfSurfaces; i++ )
        {
            sprintf( buffer, "%s/%d.png", directory, i );
            surfaces[i] = new Surface( buffer );
        }

        /* Repeat it all for the side surfaces.
         */
        do
        {
            sprintf( buffer, "%s/side%d.png", directory, ++numberOfSideSurfaces );
        }
        while( isValidFile( buffer ) );

        /* Allocate room for (numberOfTiles) Surface pointers.
         */
        sideSurfaces = new Surface*[numberOfSideSurfaces];

        /* Load the actual surfaces.
         */
        sideSurfaces[0] = 0;

        for( int i=1; i<numberOfSideSurfaces; i++ )
        {
            sprintf( buffer, "%s/side%d.png", directory, i );
            sideSurfaces[i] = new Surface( buffer );
        }
    }

    TileSet::~TileSet()
    {
        for( int i=1; i<numberOfSurfaces; i++ )
            delete surfaces[i];

        delete[] surfaces;

        for( int i=1; i<numberOfSideSurfaces; i++ )
            delete sideSurfaces[i];

        delete[] sideSurfaces;
    }

    Surface *TileSet::getSurface( int tileNumber ) const
    {
        return surfaces[ tileNumber ];
    }

    Surface *TileSet::getSideSurface( int tileNumber ) const
    {
        return sideSurfaces[ tileNumber ];
    }

};
