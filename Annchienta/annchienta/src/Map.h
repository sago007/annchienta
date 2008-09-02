/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAP_H
#define ANNCHIENTA_MAP_H

#include <vector>
#include "Engine.h"

namespace Annchienta
{

    class TileSet;
    class Layer;
    class StaticObject;

    /** A Map is probably one of the most important
     *  classes in the engine. It holds a game map
     *  and everything in it.
     */
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

            char filename[DEFAULT_STRING_SIZE];

            char *onPreRenderScript, *onPreRenderCode;
            char *onPostRenderScript, *onPostRenderCode;

        public:

            /** Load a new map.
             *  \param filename XML file where the Map should be loaded from.
             */
            Map( const char *filename );
            
            /** Creates a new, empty Map.
             *  \param w The new map width.
             *  \param h The new map height.
             *  \param tileset Directory where the Map TileSet should be loaded from.
             */
            Map( int w, int h, const char *tileset );
            ~Map();

            /** \return A reference to the current Layer in this Map.
             */
            Layer *getCurrentLayer() const;
            
            /** \param index The index of Layer you want to retrieve.
             *  \return A reference to the desired Layer.
             */
            Layer *getLayer( int index ) const;
            
            /** \return The index of the current Layer.
             */
            int getCurrentLayerIndex() const;
            
            /** Sets a new current Layer.
             *  \param index The index of the new current Layer.
             */
            void setCurrentLayer( int index );
            
            /** \return The number of layers in the current Map.
             */
            int getNumberOfLayers() const;

            const char *getFileName() const;

            int getWidth() const;
            int getHeight() const;

            void addNewLayer( int z );

            TileSet *getTileSet() const;

            StaticObject *getObject( const char *name );
            void addObject( StaticObject *so );
            void removeObject( StaticObject *so );

            void update();
            void draw() const;
            void drawTerrain() const;
            void depthSort();

            void sortLayers();

            void onPreRender() const;
            void onPostRender() const;

    };
};

#endif
