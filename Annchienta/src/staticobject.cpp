/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "staticobject.h"

#include "xml/irrXML.h"
using namespace irr;
using namespace io;
#include "auxfunc.h"
#include "cachemanager.h"
#include "videomanager.h"
#include "mapmanager.h"
#include "surface.h"
#include "tile.h"
#include "mask.h"
#include "layer.h"
#include "tileset.h"

bool DepthSortPredicate( Annchienta::Tile* tilep1, Annchienta::Tile* tilep2 )
{
    return tilep1->getDepthSortY() < tilep2->getDepthSortY();
}

namespace Annchienta
{

    void StaticObject::setCollidingTiles()
    {
        collidingTiles.clear();

        Point pos = this->getMaskPosition(), point;

        /* First we need to collect all colliding tiles.
            */
        for( int ty=0; ty<layer->getHeight(); ty++ )
        {
            for( int tx=0; tx<layer->getWidth(); tx++ )
            {
                Tile *tile = *layer->getTilePointer( tx, ty );
                point = tile->getMaskPosition();
                if( mask->collision( pos.x, pos.y, layer->getTileSet()->getMask(), point.x, point.y ) )
                    collidingTiles.push_back( tile );

                if( tile->hasPoint(position) )
                {
                    //printf("Standing on ( %d, %d )\n", tx, ty );
                    tileStandingOn = tile;
                }
            }

        }
    }

    void StaticObject::setZFromCollidingTiles()
    {
        /* Now, we set out Z to the highest one of the colliding tiles.
            */
        position.z = 0;
        for( std::list<Tile*>::iterator i = collidingTiles.begin(); i!=collidingTiles.end(); i++ )
        {
            //if( tileStandingOn )
            //{
            for( int p=0; p<4; p++ )
            {
                if( (*i)->getZ(p) > position.z )
                {
                    position.z = (*i)->getZ(p);
                }
            }
            //}
        }
    }

    StaticObject::StaticObject( const char *_name, const char *configfile ): Entity(_name), sprite(0), mask(0), tileStandingOn(0), currentFrame(0), needsUpdate(true)
    {
        IrrXMLReader *xml = createIrrXMLReader( configfile );

        if( !xml )
            printf("Could not open config file %s for %s\n", configfile, _name );

        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmpCaseInsensitive("sprite", xml->getNodeName()) )
                    {
                        sprite = getCacheManager()->getSurface( xml->getAttributeValue("image") );
                        mask = getCacheManager()->getMask( xml->getAttributeValue("mask") );
                    }
                    if( !strcmpCaseInsensitive("frame", xml->getNodeName()) )
                    {
                        Frame frame;

                        if( xml->getAttributeValue("number") )
                            frame.number = xml->getAttributeValueAsInt("number");
                        else
                            printf("Warning - number not defined for frame in %s\n", configfile);

                        frame.x1 = xml->getAttributeValueAsInt("x1");
                        frame.y1 = xml->getAttributeValueAsInt("y1");
                        frame.x2 = xml->getAttributeValueAsInt("x2");
                        frame.y2 = xml->getAttributeValueAsInt("y2");
                        frames.push_back( frame );
                    }
                    if( !strcmpCaseInsensitive("animation", xml->getNodeName()) )
                    {
                        Animation animation;
                        strcpy( animation.name, xml->getAttributeValue("name") );
                        strcpy( animation.frames, xml->getAttributeValue("frames") );
                        animation.numberOfFrames = strlen( animation.frames );
                        animation.speed = xml->getAttributeValueAsInt("speed");
                        animations.push_back( animation );
                    }
                    break;
            }
        }

        delete xml;

        setAnimation( "stand" );
    }

    StaticObject::~StaticObject()
    {
    }

    EntityType StaticObject::getEntityType() const
    {
        return StaticObjectEntity;
    }

    void StaticObject::update()
    {
        if( currentAnimation>=0 )
        {
            speedTimer++;
            if( speedTimer >= animations[currentAnimation].speed )
            {
                currentFrame++;
                if( currentFrame >= animations[currentAnimation].numberOfFrames )
                    currentFrame = 0;
                speedTimer = 0;
            }
        }

        if( needsUpdate && layer )
        {
            setCollidingTiles();

            /* Do a depthsort on them.
             */
            collidingTiles.sort( DepthSortPredicate );

            setZFromCollidingTiles();

            needsUpdate = false;
        }

        mapPosition = position.to( MapPoint );
    }

    void StaticObject::draw()
    {
        if( this->isDrawn() )
            return;

        for( std::list<Tile*>::iterator i = collidingTiles.begin(); i!=collidingTiles.end(); i++ )
        {
            (*i)->draw();

            /*glColor4f(1.0f,0.0f,0.0f,0.5f);
            glBindTexture( GL_TEXTURE_2D, 0 );
            glBegin( GL_QUADS );
                for( int p=0; p<4; p++ )
                    glVertex2f( (*i)->getPoint(p).x, (*i)->getPoint(p).y );
            glEnd();
            glColor3f(1.0f,1.0f,1.0f);*/
        }

        this->setDrawn( true );

        if( currentAnimation<0 )
            return;

        /* Select the right frame.
         */
        Frame *frame;
        int frameNumber = animations[currentAnimation].frames[currentFrame] - '0';
        for( unsigned int i=0; i<frames.size(); i++ )
        {
            if( frames[i].number == frameNumber )
            {
                frame = &frames[i];
                i = frames.size();
            }
        }

        Point pos = this->getMaskPosition();

        getVideoManager()->drawSurface( sprite, pos.x, pos.y-pos.z, frame->x1, frame->y1, frame->x2, frame->y2 );

    }

    int StaticObject::getDepthSortY()
    {
        int dsy = mapPosition.y;
        for( std::list<Tile*>::iterator i = collidingTiles.begin(); i!=collidingTiles.end(); i++ )
            if( (*i)->getDepthSortY() > dsy )
                dsy = (*i)->getDepthSortY();

        /* The -1 will ensure that this gets drawn BEFORE tiles
         * at the same y. Yes, this is a hack. Sorry, Sanne.
         * But no, this won't hurt. :)
         */
        return dsy-1;
    }

    void StaticObject::setPosition( Point _position )
    {
        position = _position.to( IsometricPoint );
        mapPosition = _position.to( MapPoint );
        needsUpdate = true;
    }

    Point StaticObject::getPosition() const
    {
        return position;
    }

    Point StaticObject::getMaskPosition() const
    {
        return Point( MapPoint, mapPosition.x - (mask->getWidth()>>1), mapPosition.y - mask->getHeight(), mapPosition.z );
    }

    Mask *StaticObject::getMask() const
    {
        return mask;
    }

    void StaticObject::setAnimation( const char *aname )
    {
        for( unsigned int i=0; i<animations.size(); i++ )
        {
            if( !strcmpCaseInsensitive( aname, animations[i].name ) )
            {
                currentAnimation = i;
                currentFrame %= animations[i].numberOfFrames;
                return;
            }
        }

        printf( "There is no animation called %s for entity %s\n", aname, name );
        currentAnimation = -1;
    }

};
