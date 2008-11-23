/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef ANNCHIENTA_LAYER_H
#define ANNCHIENTA_LAYER_H

#include <vector>

namespace Annchienta
{
    class Tile;
    class Entity;
    class TileSet;
    class StaticObject;
    class Area;

    class Layer
    {

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
            std::vector<StaticObject*> staticObjects;
            std::vector<Area*> areas;

            TileSet *tileSet;

        public:

            /* Do not use this constructor. It's a fake one to keep
             * SWIG satisfied.
             */
            Layer();

            #ifndef SWIG
                /* Layer::setTiles MUST, I repeat, MUST be called right
                 * after this.
                 */
                Layer( TileSet *tileSet, int width, int height, int opacity, int z );
                ~Layer();

                /** Sets the tiles to be used for this Layer. This function
                 *  is mainly internally used.
                 *  \param tiles 2D-array of Tile objects.
                 *  \warning This function might mess up the engine when not properly used.
                 */
                void setTiles( Tile **tiles=0 );

                /** \return If there are tiles in this Layer. (There should be, nothing to worry about.)
                 */
                bool hasTiles() const;
            #endif


            /** Sets the opacity of the Layer. This currently does not
             *  work correct, and opacities lower than 255 will cause
             *  the Layer to be invisible.
             *  \param opacity The new opacity for this Layer.
             */
            void setOpacity( int opacity=255 );

            /** \return The opacity of this Layer.
             */
            int getOpacity() const;

            /** Sets the Z offset for this Layer.
             *  \param z The new Z offset.
             */
            void setZ( int z );

            /** \return The Z offset of this Layer.
             */
            int getZ() const;

            /** Updates this layer and everything in it: Tiles, Entities...
             */
            void update();

            /** Draws this Layer to the screen.
             */
            void draw() const;

            /** Sorts all objects in this Layer based on their
             *  depth into the screen, so they will be drawn in
             *  the correct order.
             */
            void depthSort();

            /** Adds an Entity to this Layer.
             *  \param entity Entity to be added.
             */
            void addEntity( Entity *entity );

            /** Adds an Area to this Layer.
             *  \param area Area to be added.
             */
            void addArea( Area *area );

            /** Makes this Layer empty: removes all
             *  Tiles, objects, etc.
             */
            void makeEmpty();

            /** Associates a TileSet with this Layer.
             *  \param tileSet TileSet to be used.
             *  \note It is probably a better idea to call Map::setTileSet().
             */
            void setTileSet( TileSet *tileSet );

            /** \return The TileSet used in this Layer.
             *  \note It is probably a better idea to call Map::setTileSet().
             */
            TileSet *getTileSet() const;

            /** \return The width of this Layer.
             */
            int getWidth() const;

            /** \return The height of this Layer.
             */
            int getHeight() const;

            /** Get a Tile from this Layer.
             *  \param x X coord of the Tile.
             *  \param y Y coord of the Tile.
             *  \return The Tile asked, or 0 if it doesn't exist.
             */
            Tile *getTile( int x, int y );

            /** Get an object from this Layer.
             *  \param num Id of the object.
             *  \return The requested object, or 0 if it doesn't exist.
             */
            StaticObject *getObject( int num ) const;

            /** Get an object from this Layer by name.
             *  \param name Name of the object.
             *  \return The requested object, or 0 if it doesn't exist.
             */
            StaticObject *getObject( const char *name ) const;

            /** \return The number of objects in this Layer.
             */
            int getNumberOfObjects() const;

            /** Remove an object from this Layer.
             *  \param staticObject The object to remove.
             */ 
            void removeObject( StaticObject *staticObject );

            /** Get an area from this Layer.
             *  \param num Id of the Area you want.
             *  \return The requested Area, or 0 if it doesn't exist.
             */ 
            Area *getArea( int num ) const;

            /** \return The number of Areas in this Layer.
             */
            int getNumberOfAreas() const;
    };
};

#endif
