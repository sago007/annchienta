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
    class Person;

    /** A Map is probably one of the most important
     *  classes in the engine. It holds a game map
     *  and everything in it. For an example map XML
     *  file, see \ref map_example
     */
    class Map
    {

        private:

            /* We need to draw some shit. */
            VideoManager *videoManager;

            /* TileSet used in this map. */
            TileSet *tileSet;

            int width, height;

            /* All layers in the level. */
            std::vector<Layer*> layers;
            Layer **sortedLayers;
            int currentLayer;

            char fileName[DEFAULT_STRING_SIZE];

            char *onPreRenderScript, *onPreRenderCode;
            char *onPostRenderScript, *onPostRenderCode;

        public:

            /** Load a new map.
             *  \param fileName XML file where the Map should be loaded from.
             *  \param scripts If the onload scripts should be executed. This also means all \<if> tags will evaluate to true.
             */
            Map( const char *fileName, bool scripts=true );
            
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
            
            /** \return The number of layers in this Map.
             */
            int getNumberOfLayers() const;

            /** \return The fileName from which this Map was loaded.
             */
            const char *getFileName() const;

            /** \return The width of this Map.
             */
            int getWidth() const;

            /** \return The height of this Map.
             */
            int getHeight() const;

            /** Adds a new, empty Layer to this Map.
             *  \param z Initial Z offset of the new Layer.
             */
            void addNewLayer( int z=0 );

            /** \return The TileSet used in this Map.
             */
            TileSet *getTileSet() const;

            /** Finds an object in this Map. This function starts
             *  searching in the current Layer, when not found in
             *  continues to search the other Layers.
             *  \param name Name of the StaticObject to be found.
             *  \return The found object.
             */
            StaticObject *getObject( const char *name );

            /** The same as getObject(), but returns a Person.
             *  \param name Name of the Person to be found.
             *  \return The found person.
             */
            Person *getPerson( const char *name );

            /** Adds a StaticObject to this Map. The object is
             *  placed in the current Layer.
             *  \param so StaticObject to be added.
             */
            void addObject( StaticObject *so );

            /** Removes an object from this Map. If you don't have
             *  a pointer to it, only the name, use getObject() first.
             *  \param so StaticObject to be removed.
             */
            void removeObject( StaticObject *so );

            /** Updates this Map, all Layers and all objects in
             *  those Layers.
             */
            void update();

            /** Draws the Map to the screen.
             *  \param scripts If the onPreRender and onPostRender scripts should be executed.
             */
            void draw( bool scripts=true ) const;

            /** Depthsorts this Map. Calls Layer::depthSort() for all Layers.
             */
            void depthSort();

            /** Sorts Layers by their respective Z offset.
             */
            void sortLayers();

            /** Executes onPreRender code. Automatically called
             *  by draw().
             */
            void onPreRender() const;

            /** Executes onPostRender code. Automatically called
             *  by draw().
             */
            void onPostRender() const;

    };
};

#endif

