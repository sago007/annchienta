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
    class StaticObject;

    class Map
    {

        private:
            TileSet *tileSet;

            int width, height;

            /* All layers in the level.
             */
            std::vector<Layer*> layers;
            Layer **sortedLayers;
            int currentLayer;


        public:

            Map( const char *filename );
            Map( int w, int h, const char *tileset );
            ~Map();

            Layer *getCurrentLayer() const;
            Layer *getLayer( int ) const;
            int getCurrentLayerIndex() const;
            void setCurrentLayer( int index );
            int getNumberOfLayers() const;

            int getWidth() const;
            int getHeight() const;

            void addNewLayer( int z );

            TileSet *getTileSet() const;

            StaticObject *getObject( const char *name );
            void removeObject( StaticObject *so );

            void update();
            void draw() const;
            void drawTerrain() const;
            void depthSort();

            void sortLayers();

    };
};

#endif
