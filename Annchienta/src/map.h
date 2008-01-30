/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAP_H
#define ANNCHIENTA_MAP_H

#include <vector>

namespace Annchienta
{

    class TileSet;
    class Layer;

    class Map
    {
        private:
            TileSet *tileSet;

            /* All layers in the level.
             */
            std::vector<Layer*> layers;


        public:

            Map( const char *filename );
            ~Map();

            void draw() const;
            void depthSort();

    };
};

#endif
