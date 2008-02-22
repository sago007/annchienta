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

namespace Annchienta
{

    Layer::Layer( LayerInfo *info, Tile **_tiles ): width(info->width), height(info->height), z(info->z), opacity(info->opacity), tileSet(0)
    {
        /* Create some extra space.
         */
        //printf("Creating layer: %d x %d\n", width, height);
        entities.resize( width*height );

        if( _tiles )
            tiles = _tiles;
        else
            makeEmpty();

        for( int i=0; i<width*height; i++ )
            entities[i] = tiles[i];
    }

    Layer::~Layer()
    {
        for( unsigned int i=0; i<entities.size(); i++ )
        {
            delete entities[i];
        }

        delete[] tiles;
    }

    void Layer::setOpacity( int o )
    {
        opacity = o;
    }

    int Layer::getOpacity() const
    {
        return opacity;
    }

    void Layer::update()
    {
        for( unsigned int i=0; i<entities.size(); i++ )
            entities[i]->update();

        this->depthSort();
    }

    void Layer::draw() const
    {
        glPushMatrix();

        glTranslatef( 0.0f, -z, 0.0f );

        if( opacity < 0xff )
            return;

        for( unsigned int i=0; i<entities.size(); i++ )
            entities[i]->setDrawn( false );

        for( unsigned int i=0; i<entities.size(); i++ )
            entities[i]->draw();

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
            if( entities[i-1]->getDepthSortY() > entities[i]->getDepthSortY() )
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
    }

    void Layer::addEntity( Entity *entity )
    {
        entities.push_back( entity );
        entity->setLayer( this );

        if( entity->getEntityType() == StaticObjectEntity || entity->getEntityType() == PersonEntity )
            staticObjects.push_back( (StaticObject*) entity );
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

                tiles[y*width+x] = new Tile( points[0], 0, points[1], 0, points[2], 0, points[3], 0, 0 );
            }
        }
    }

    Tile **Layer::getTilePointer( int x, int y )
    {
        return &tiles[ x*width+y ];
    }

    void Layer::setTileSet( TileSet *_tileSet )
    {
        tileSet = _tileSet;
    }

    TileSet *Layer::getTileSet() const
    {
        return tileSet;
    }

    StaticObject *Layer::getStaticObject( int num )
    {
        if( (unsigned int)num >= staticObjects.size() )
            return 0;
        return staticObjects[num];
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
        return tiles[ x*width+y ];
    }

    StaticObject *Layer::getObject( const char *name )
    {
        for( int i=0; getStaticObject(i); i++ )
            if( !strcmpCaseInsensitive( getStaticObject(i)->getName(), name ) )
                return getStaticObject(i);
        return 0;
    }

};
