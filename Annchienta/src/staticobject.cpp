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

namespace Annchienta
{

    StaticObject::StaticObject( const char *_name, const char *configfile ): Entity(_name), sprite(0), currentFrame(0)
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
                        sprite = getCacheManager()->getSurface( xml->getAttributeValue("filename") );
                    }
                    if( !strcmpCaseInsensitive("frame", xml->getNodeName()) )
                    {
                        Frame frame;
                        frame.number = xml->getAttributeValueAsInt("number");
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
    }

    void StaticObject::update()
    {
        if( currentAnimation>=0 )
        {
            currentFrame++;
            if( currentFrame >= animations[currentAnimation].numberOfFrames )
                currentFrame = 0;
        }
    }

    void StaticObject::draw()
    {
        if( this->isDrawn() )
            return;

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
        getVideoManager()->drawSurface( sprite, 0, 0, frame->x1, frame->y1, frame->x2, frame->y2 );
        //printf("Drawing area: %d, %d, %d, %d\n", frame->x1, frame->y1, frame->x2, frame->y2 );

    }

    int StaticObject::getDepthSortY() const
    {
        return 200;
    }

    void StaticObject::setPosition( Point _position )
    {
        position = _position;
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
                currentFrame = 0;
                return;
            }
        }

        printf( "There is no animation called %s for entity %s\n", aname, name );
        currentAnimation = -1;
    }

};
