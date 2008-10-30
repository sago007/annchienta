/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
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

                void setTiles( Tile **tiles=0 );
                bool hasTiles() const;
            #endif

            void setOpacity( int opacity=0xff );
            int getOpacity() const;

            void setZ( int );
            int getZ() const;

            void update();
            void draw() const;
            void depthSort();

            void addEntity( Entity *entity );
            void addArea( Area *area );

            #ifndef SWIG
                void makeEmpty();
                void setTileSet( TileSet *tileSet );
                TileSet *getTileSet() const;
            #endif

            int getWidth() const;
            int getHeight() const;
            Tile *getTile( int x, int y );

            StaticObject *getObject( int num ) const;
            StaticObject *getObject( const char *name ) const;
            int getNumberOfObjects() const;
            void removeObject( StaticObject *so );

            Area *getArea( int num ) const;
    };
};

#endif
