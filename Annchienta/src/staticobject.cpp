/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "staticobject.h"

#include <Python.h>
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
#include "engine.h"

bool DepthSortPredicate( Annchienta::Tile* tilep1, Annchienta::Tile* tilep2 )
{
    return tilep1->getDepth() < tilep2->getDepth();
}

namespace Annchienta
{

    StaticObject *activeObject, *passiveObject;

    StaticObject::StaticObject( const char *_name, const char *configfile ): Entity(_name), sprite(0), mask(0), tileStandingOn(0), currentFrame(0), needsUpdate(true), onInteractScript(0), onInteractCode(0)
    {
        IrrXMLReader *xml = createIrrXMLReader( configfile );

        strcpy( xmlFile, configfile );

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
                    if( !strcmpCaseInsensitive("oninteract", xml->getNodeName()) )
                    {
                        if( xml->getAttributeValue("script") )
                        {
                            onInteractScript = new char[ strlen(xml->getAttributeValue("script"))+1 ];
                            strcpy( onInteractScript, xml->getAttributeValue("script") );
                            onInteractCode = 0;
                        }
                        else
                        {
                            xml->read();
                            onInteractCode = new char[ strlen(xml->getNodeData())+1 ];
                            strcpy( onInteractCode, xml->getNodeData() );
                            xml->read();
                            onInteractScript = 0;
                        }
                    }
                    break;
            }
        }

        delete xml;

        setAnimation( "stand" );
        speedTimer = 0;
    }

    StaticObject::~StaticObject()
    {
        if( onInteractCode )
            delete[] onInteractCode;
        if( onInteractScript )
            delete[] onInteractScript;
    }

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
        /* Do a depthsort on them.
            */
        collidingTiles.sort( DepthSortPredicate );
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

        mapPosition = position.to( MapPoint );
    }

    EntityType StaticObject::getEntityType() const
    {
        return StaticObjectEntity;
    }

    void StaticObject::update()
    {
        if( /*animationRunning &&*/ currentAnimation>=0 )
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

        if( !strcmpCaseInsensitive("aelaan", getName()) )
        {
            //printf("Drawing frame %d of %s\n", frameNumber, animations[currentAnimation].name );
        }

        Point pos = this->getMaskPosition();

        glColor4f( 1.0f, 1.0f, 1.0f, 1.0f );
        getVideoManager()->drawSurface( sprite, pos.x, pos.y-pos.z, frame->x1, frame->y1, frame->x2, frame->y2 );

    }

    int StaticObject::getDepth()
    {
        int dsy = mapPosition.y;
        for( std::list<Tile*>::iterator i = collidingTiles.begin(); i!=collidingTiles.end(); i++ )
            if( (*i)->getDepth() > dsy )
                dsy = (*i)->getDepth();

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

    const char *StaticObject::getXmlFile() const
    {
        return xmlFile;
    }

    bool StaticObject::setAnimation( const char *aname )
    {

        for( unsigned int i=0; i<animations.size(); i++ )
        {
            if( !strcmpCaseInsensitive( aname, animations[i].name ) )
            {
                //printf("Set %s to %s or %s\n", getName(), aname, animations[i].name );
                currentAnimation = i;
                currentFrame %= animations[i].numberOfFrames;
                animationRunning = true;
                return true;
            }
        }

        currentAnimation = -1;
        return false;
    }

    /*void StaticObject::stopAnimation()
    {
        animationRunning = false;
    }

    void StaticObject::startAnimation()
    {
        animationRunning = true;
    }*/

    void StaticObject::onInteract()
    {
        if( onInteractCode )
            PyRun_SimpleString( onInteractCode );
        if( onInteractScript )
            getEngine()->runPythonScript( onInteractScript );
    }

    void StaticObject::freeze( bool )
    {
        return;
    }

    bool StaticObject::stepTo( int x, int y )
    {
        printf("Warning - attempt to step static object %s to %d, %d. Warping.\n", this->getName(), x, y );
        position.x = x;
        position.y = y;
        needsUpdate = true;
        return true;
    }

    void StaticObject::lookAt( StaticObject *other )
    {
        return;
    }

    void setActiveObject( StaticObject *o )
    {
        activeObject = o;
    }

    void setPassiveObject( StaticObject *o )
    {
        passiveObject = o;
    }

    StaticObject *getActiveObject()
    {
        return activeObject;
    }

    StaticObject *getPassiveObject()
    {
        return passiveObject;
    }

};
