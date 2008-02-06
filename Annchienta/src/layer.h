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
    struct LayerInfo;

    #ifndef SWIG
        struct LayerInfo
        {
            int width, height, opacity, z;
        };
    #endif

    class Layer
    {
        friend class Editor;

        private:
            /* Number of tiles.
             */
            int width, height;
            int opacity;

            /* Z offset
             */
            int z;

            Tile **tiles;

            /* This is another list that holds ALL entities in the
             * layer. This even includes tiles.
             */
            std::vector<Entity*> entities;

        public:

            Layer( LayerInfo *info, Tile **tiles=0 );
            ~Layer();

            void setOpacity( int opacity=0xff );
            int getOpacity() const;

            void update();
            void draw() const;
            void depthSort();

            void addEntity( Entity *entity );

            #ifndef SWIG
                void makeEmpty();
                Tile **getTilePointer( int x, int y );
            #endif
    };
};

#endif
