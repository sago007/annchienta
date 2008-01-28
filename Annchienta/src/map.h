/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAP_H
#define ANNCHIENTA_MAP_H

namespace Annchienta
{

    class Tile;
    class TileSet;

    class Map
    {
        private:
            Tile **tiles;
            TileSet *tileSet;

        public:

            Map( const char *filename );
            ~Map();

            void draw();

    };
};

#endif
