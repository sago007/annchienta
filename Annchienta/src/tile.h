/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_TILE_H
#define ANNCHIENTA_TILE_H

#include "point.h"

namespace Annchienta
{

    class Surface;

    class Tile
    {
        private:
            Point points[4];
            Surface *surfaces[4];

        public:
            Tile( Point, Surface*, Point, Surface*, Point, Surface*, Point, Surface* );
            ~Tile();

            void draw();

    };
};

#endif
