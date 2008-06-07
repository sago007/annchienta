/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "layer.h"

#include "entity.h"
#include "auxfunc.h"
#include "tile.h"
#include "videomanager.h"
#include "tileset.h"
#include "staticobject.h"
#include "area.h"
#include "logmanager.h"

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

        glTranslatef( 0.0f, -z, 0.0f );

        if( opacity >= 0xff )
        {
            for( unsigned int i=0; i<entities.size(); i++ )
                entities[i]->setDrawn( false );

            for( unsigned int i=0; i<entities.size(); i++ )
                entities[i]->draw();
        }

        glPopMatrix();
    }

    void Layer::drawTerrain() const
    {
        glPushMatrix();

        glTranslatef( 0.0f, -z, 0.0f );

        if( opacity < 0xff )
            return;

        for( unsigned int i=0; i<entities.size(); i++ )
        {
            if( entities[i]->getEntityType() != PersonEntity )
                entities[i]->setDrawn( false );
            else
                entities[i]->setDrawn( true );
        }

        for( unsigned int i=0; i<entities.size(); i++ )
            entities[i]->draw();

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
                swap<Entity*>( entities[i-1], entities[i] );
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
                        swap<Entity*>( entities[i-1], entities[i] );
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

        /* Entity needs to go in the right place.
         */
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

    Tile **Layer::getTilePointer( int x, int y )
    {
        return &tiles[ y*width+x ];
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
        return tiles[ y*width+x ];
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
            if( !strcmpCaseInsensitive( getObject(i)->getName(), name ) )
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

};
