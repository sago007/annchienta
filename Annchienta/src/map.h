/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAP_H
#define ANNCHIENTA_MAP_H

#include <vector>
#include "editor.h"

namespace Annchienta
{

    class TileSet;
    class Layer;

    class Map
    {
        friend class Editor;

        private:
            TileSet *tileSet;

            int width, height;

            /* All layers in the level.
             */
            std::vector<Layer*> layers;
            int currentLayer;


        public:

            Map( const char *filename );
            ~Map();

            Layer *getCurrentLayer() const;
            void setCurrentLayer( int index );

            void draw() const;
            void depthSort();

    };
};

#endif
