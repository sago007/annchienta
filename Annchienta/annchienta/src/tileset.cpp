/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "tileset.h"

#include <stdio.h>
#include <string.h>
#include "surface.h"
#include "mask.h"
#include "auxfunc.h"
#include "mapmanager.h"
#include "logmanager.h"

namespace Annchienta
{

    TileSet::TileSet( const char *_directory ): numberOfSurfaces(0), numberOfSideSurfaces(0)
    {
        strcpy( directory, _directory );

        char buffer[ DEFAULT_STRING_SIZE ];

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

        mask = new Mask( getMapManager()->getTileWidth(), getMapManager()->getTileHeight() );
    }

    TileSet::~TileSet()
    {
        for( int i=1; i<numberOfSurfaces; i++ )
            delete surfaces[i];

        delete[] surfaces;

        for( int i=1; i<numberOfSideSurfaces; i++ )
            delete sideSurfaces[i];

        delete[] sideSurfaces;

        delete mask;
    }

    Surface *TileSet::getSurface( int tileNumber ) const
    {
        if( tileNumber>=0 && tileNumber<numberOfSurfaces )
            return surfaces[ tileNumber ];
        else
            getLogManager()->warning( "Tile '%d' does not exist in tileset '%s'.", tileNumber, directory );
        return 0;
    }

    Surface *TileSet::getSideSurface( int tileNumber ) const
    {
        if( tileNumber>=0 && tileNumber<numberOfSideSurfaces )
            return sideSurfaces[ tileNumber ];
        else
            getLogManager()->warning( "Side tile '%d' does not exist in tileset '%s'.", tileNumber, directory );
        return 0;
    }

    Mask *TileSet::getMask() const
    {
        return mask;
    }

    const char *TileSet::getDirectory() const
    {
        return directory;
    }

};
