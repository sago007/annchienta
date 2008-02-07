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
#include "surface.h"
#include "tile.h"
#include "mask.h"
#include "layer.h"
#include "tileset.h"

namespace Annchienta
{

    StaticObject::StaticObject( const char *_name, const char *configfile ): Entity(_name), sprite(0), mask(0), currentFrame(0), needsUpdate(true)
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
        getCacheManager()->deleteSurface( sprite );
        getCacheManager()->deleteMask( mask );
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
            collidingTiles.clear();

            Point point;

            for( int ty=0; ty<layer->getHeight(); ty++ )
            {
                for( int tx=0; tx<layer->getWidth(); tx++ )
                {
                    Tile *tile = *layer->getTilePointer( tx, ty );
                    point = tile->getMaskPosition();
                    if( mask->collision( mapPosition.x, mapPosition.y, layer->getTileSet()->getMask(), point.x, point.y ) )
                        collidingTiles.push_back( tile );
                }
            }

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
            //(*i)->setDrawn(true);
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
        getVideoManager()->drawSurface( sprite, mapPosition.x, mapPosition.y, frame->x1, frame->y1, frame->x2, frame->y2 );
        //printf("Drawing area: %d, %d, %d, %d\n", frame->x1, frame->y1, frame->x2, frame->y2 );

    }

    int StaticObject::getDepthSortY() const
    {
        return mapPosition.y + sprite->getHeight();
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

    void StaticObject::setAnimation( const char *aname )
    {
        for( unsigned int i=0; i<animations.size(); i++ )
        {
            if( !strcmpCaseInsensitive( aname, animations[i].name ) )
            {
                currentAnimation = i;
                currentFrame = speedTimer = 0;
                return;
            }
        }

        printf( "There is no animation called %s for entity %s\n", aname, name );
        currentAnimation = -1;
    }

};
