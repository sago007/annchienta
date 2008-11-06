/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "TileSet.h"

#include <cstdio>
#include <cstring>
#include "Surface.h"
#include "Mask.h"
#include "Engine.h"
#include "MapManager.h"
#include "LogManager.h"

namespace Annchienta
{

    TileSet::TileSet( const char *_directory ): numberOfSurfaces(0), numberOfSideSurfaces(0)
    {
        Engine *engine = getEngine();

        /* Store directory where we search for later use. */
        strcpy( directory, _directory );

        /* A buffer for filename manipulation. */
        char buffer[ DEFAULT_STRING_SIZE ];

        /* Count the regular surfaces: try directory/n.png, starting
         * with n = 1, until it fails.
         */
        do
        {
            sprintf( buffer, "%s/%d.png", directory, ++numberOfSurfaces );
        }
        while( engine->isValidFile( buffer ) );

        /* Allocate room for (numberOfTiles) Surface pointers.
         */
        surfaces = new Surface*[numberOfSurfaces];

        /* Load the actual surfaces. The first surface does not
         * exist as it is a NullTile.
         */
        surfaces[0] = 0;

        for( int i=1; i<numberOfSurfaces; i++ )
        {
            sprintf( buffer, "%s/%d.png", directory, i );
            surfaces[i] = new Surface( buffer );
        }

        /* Repeat it all for the side surfaces. Start by counting...
         */
        do
        {
            sprintf( buffer, "%s/side%d.png", directory, ++numberOfSideSurfaces );
        }
        while( engine->isValidFile( buffer ) );

        /* Allocate room for (numberOfTiles) Surface pointers.
         */
        sideSurfaces = new Surface*[numberOfSideSurfaces];

        /* Load the actual surfaces. The first one is a NullTile, too.
         */
        sideSurfaces[0] = 0;

        for( int i=1; i<numberOfSideSurfaces; i++ )
        {
            sprintf( buffer, "%s/side%d.png", directory, i );
            sideSurfaces[i] = new Surface( buffer );
        }

        /* Create a new mask with the good size. Masks are tile-shaped
         * by default, so that's OK.
         */
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

    int TileSet::getNumberOfSurfaces() const
    {
        return numberOfSurfaces;
    }

    int TileSet::getNumberOfSideSurfaces() const
    {
        return numberOfSideSurfaces;
    }

};
