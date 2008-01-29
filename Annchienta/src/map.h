/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAP_H
#define ANNCHIENTA_MAP_H

#include <vector>

namespace Annchienta
{

    class Tile;
    class TileSet;
    class Entity;

    class Map
    {
        private:
            /* Number of tiles.
             */
            int width, height;

            Tile **tiles;
            TileSet *tileSet;

            /* This is another list that holds ALL entities in the
             * level. This even includes tiles.
             */
            std::vector<Entity*> entities;

        public:

            Map( const char *filename );
            ~Map();

            void draw() const;
            void depthSort();

    };
};

#endif
