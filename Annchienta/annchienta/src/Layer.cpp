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

#include "Layer.h"

#include "Entity.h"
#include "Tile.h"
#include "VideoManager.h"
#include "TileSet.h"
#include "StaticObject.h"
#include "Area.h"
#include "LogManager.h"
#include "InputManager.h"

namespace Annchienta
{

    Layer::Layer()
    {
    }

    Layer::Layer( TileSet *ts, int w, int h, int o, int _z ): width(w), height(h), opacity(o), z(_z), tileSet(ts)
    {
    }

    Layer::~Layer()
    {
        for( unsigned int i=0; i<entities.size(); i++ )
            delete entities[i];

        for( unsigned int i=0; i<areas.size(); i++ )
            delete areas[i];

        delete[] tiles;
    }

    void Layer::setTiles( Tile **_tiles )
    {
        /* Create some extra space.
         */
        entities.resize( width*height );

        if( _tiles )
            tiles = _tiles;
        else
            makeEmpty();

        for( int i=0; i<width*height; i++ )
            entities[i] = tiles[i];
    }

    bool Layer::hasTiles() const
    {
        return (bool) tiles;
    }

    void Layer::setOpacity( int o )
    {
        opacity = o;
    }

    int Layer::getOpacity() const
    {
        return opacity;
    }

    void Layer::setZ( int _z )
    {
        z = _z;
    }

    int Layer::getZ() const
    {
        return z;
    }

    void Layer::update()
    {
        for( unsigned int i=0; i<entities.size(); i++ )
        {
            entities[i]->update();
        }

        this->depthSort();
    }

    void Layer::draw() const
    {
        glPushMatrix();

        glTranslatef( 0.0f, (GLfloat)-z, 0.0f );

        if( opacity >= 0xff )
        {
            for( unsigned int i=0; i<entities.size(); i++ )
                entities[i]->setDrawn( false );

            for( unsigned int i=0; i<entities.size(); i++ )
                entities[i]->draw();
        }

        glPopMatrix();
    }

    void Layer::depthSort()
    {
        /* The layer should be more or less sorted already, that's
         * why we use a form of gnome sort.
         */
        unsigned int i=1, c=1;
        while( i<entities.size() )
        {
            if( entities[i-1]->getDepth() > entities[i]->getDepth() )
            {
                Entity *temp = entities[i-1];
                entities[i-1] = entities[i];
                entities[i] = temp;
                if( i>1 )
                    i--;
            }
            else
            {
                /* Exception rule for StaticObjects. They might be on the same Tile, so we have to make sure
                 * and check Y values as well.
                 */
                if( (entities[i-1]->getEntityType()!=TileEntity) && (entities[i]->getEntityType()!=TileEntity) && ( entities[i-1]->getDepth() == entities[i]->getDepth() ) )
                {
                    StaticObject *so1 = (StaticObject*) entities[i-1],
                                 *so2 = (StaticObject*) entities[i];

                    Point p1 = so1->getPosition().to( MapPoint ),
                          p2 = so2->getPosition().to( MapPoint );

                    if( p1.y > p2.y )
                    {
                        Entity *temp = entities[i-1];
                        entities[i-1] = entities[i];
                        entities[i] = temp;
                        if( i>1 )
                            i--;
                    }
                    else
                    {
                        c = i = i>=c?i+1:c;
                    }
                }
                else
                {
                    c = i = i>=c?i+1:c;
                }
            }
        }
    }

    void Layer::addEntity( Entity *entity )
    {
        entities.push_back( entity );
        entity->setLayer( this );

        if( entity->getEntityType() == StaticObjectEntity || entity->getEntityType() == PersonEntity )
            staticObjects.push_back( (StaticObject*) entity );

        /* Entity needs to go in the right place. Depthsort is of course
         * nessecary, but we also need to do an update to the entity has
         * has the right colliding tiles et cetera. We also set inputMode
         * to cinematic because we don't want to trigger collision areas
         * yet.
         */
        InputManager *inputManager = getInputManager();
        InputMode mode = inputManager->getInputMode();
        inputManager->setInputMode( CinematicMode );
        entity->update();
        inputManager->setInputMode( mode );
        this->depthSort();
    }

    void Layer::addArea( Area *area )
    {
        areas.push_back( area );
    }

    void Layer::makeEmpty()
    {
        tiles = new Tile*[width*height];

        for( int y=0; y<height; y++ )
        {
            for( int x=0; x<width; x++ )
            {
                Point points[4];
                points[0].x = points[1].x = x;
                points[2].x = points[3].x = x+1;
                points[0].y = points[3].y = y;
                points[1].y = points[2].y = y+1;

                for( int i=0; i<4; i++ )
                {
                    points[i].setType( TilePoint );
                    points[i].z = 0;
                }

                tiles[y*width+x] = new Tile( tileSet, points[0], 0, points[1], 0, points[2], 0, points[3], 0, 0, 0 );
            }
        }
    }

    void Layer::setTileSet( TileSet *_tileSet )
    {
        tileSet = _tileSet;
    }

    TileSet *Layer::getTileSet() const
    {
        return tileSet;
    }

    int Layer::getWidth() const
    {
        return width;
    }

    int Layer::getHeight() const
    {
        return height;
    }

    Tile *Layer::getTile( int x, int y )
    {
        if( x>=0 && x<getWidth() && x>=0 && y<getHeight() )
            return tiles[ y*width+x ];
        else
            return 0;
    }

    StaticObject *Layer::getObject( int num ) const
    {
        if( (unsigned int)num >= staticObjects.size() )
            return 0;
        return staticObjects[num];
    }

    StaticObject *Layer::getObject( const char *name ) const
    {
        for( int i=0; getObject(i); i++ )
            if( !strcmp( getObject(i)->getName(), name ) )
                return getObject(i);
        return 0;
    }

    int Layer::getNumberOfObjects() const
    {
        return (int)staticObjects.size();
    }

    void Layer::removeObject( StaticObject *so )
    {
        for( unsigned int i=0; i<staticObjects.size(); i++ )
        {
            if( staticObjects[i] == so )
            {
                staticObjects.erase( staticObjects.begin()+i );
            }
        }

        for( unsigned int i=0; i<entities.size(); i++ )
        {
            if( (StaticObject*) entities[i] == so )
            {
                entities.erase( entities.begin()+i );
            }
        }
    }

    Area *Layer::getArea( int num ) const
    {
        if( (unsigned int)num >= areas.size() )
            return 0;
        return areas[num];
    }

    int Layer::getNumberOfAreas() const
    {
        return (int)areas.size();
    }

};
