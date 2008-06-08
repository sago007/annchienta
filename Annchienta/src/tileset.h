/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_TILESET_H
#define ANNCHIENTA_TILESET_H

#include "engine.h"

namespace Annchienta
{

    class Surface;
    class Mask;

    class TileSet
    {
        private:
            char directory[DEFAULT_STRING_SIZE];

            Surface **surfaces;
            int numberOfSurfaces;

            Surface **sideSurfaces;
            int numberOfSideSurfaces;

            Mask *mask;

        public:
            TileSet( const char *directory );
            ~TileSet();

            Surface *getSurface( int tileNumber ) const;
            Surface *getSideSurface( int sideNumber ) const;
            Mask *getMask() const;

            const char *getDirectory() const;

    };
};

#endif
