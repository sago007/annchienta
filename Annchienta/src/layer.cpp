/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "layer.h"

#include "entity.h"
#include "auxfunc.h"
#include "tile.h"

namespace Annchienta
{

    Layer::Layer( int w, int h, Tile **_tiles ): width(w), height(h)
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

    Layer::~Layer()
    {
        for( int i=0; i<width*height; i++ )
        {
            delete tiles[i];
        }
        delete[] tiles;
    }

    void Layer::draw() const
    {
        glPushMatrix();

        for( unsigned int i=0; i<entities.size(); i++ )
            entities[i]->setDrawn( false );

        for( unsigned int i=0; i<entities.size(); i++ )
            entities[i]->draw();

        glColor4f( 1.0f, 1.0f, 1.0f, 1.0f );

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

                tiles[y*width+x] = new Tile( points[0], 0, points[1], 0, points[2], 0, points[3], 0 );
            }
        }
    }

    Tile **Layer::getTilePointer( int x, int y )
    {
        return &tiles[ x*width+y ];
    }

};
