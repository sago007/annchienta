/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_LAYER_H
#define ANNCHIENTA_LAYER_H

#include <vector>
#include "editor.h"

namespace Annchienta
{
    class Tile;
    class Entity;

    class Layer
    {
        friend class Editor;

        private:
            /* Number of tiles.
             */
            int width, height;

            /* Z offset
             */
            int z;

            Tile **tiles;

            /* This is another list that holds ALL entities in the
             * layer. This even includes tiles.
             */
            std::vector<Entity*> entities;

        public:

            Layer( int width, int height, Tile **tiles=0, int z=0 );
            ~Layer();

            void draw() const;
            void depthSort();

            #ifndef SWIG
                void makeEmpty();
                Tile **getTilePointer( int x, int y );
            #endif
    };
};

#endif
