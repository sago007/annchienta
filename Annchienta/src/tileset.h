/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_TILESET_H
#define ANNCHIENTA_TILESET_H

namespace Annchienta
{

    class Surface;

    class TileSet
    {
        private:
            Surface **surfaces;
            int numberOfSurfaces;

        public:
            TileSet( const char *directory );
            ~TileSet();

            Surface *getSurface( int tileNumber ) const;

    };
};

#endif
