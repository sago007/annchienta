/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "StaticObject.h"

#include <Python.h>
#include "xml/irrXML.h"
using namespace irr;
using namespace io;
#include "GeneralFunctions.h"
#include "CacheManager.h"
#include "VideoManager.h"
#include "MapManager.h"
#include "Surface.h"
#include "Tile.h"
#include "Mask.h"
#include "Layer.h"
#include "TileSet.h"
#include "Engine.h"
#include "LogManager.h"

/* Used for quickly sorting Entities based on depth.
 */
bool DepthSortPredicate( Annchienta::Tile* tilep1, Annchienta::Tile* tilep2 )
{
    return tilep1->getDepth() < tilep2->getDepth();
}

namespace Annchienta
{
    StaticObject *activeObject=0, *passiveObject=0;

    StaticObject::StaticObject( const char *_name, const char *configfile ): Entity(_name), sprite(0), mask(0), tileStandingOn(0), currentFrame(0), passable(false), needsUpdate(true), onInteractScript(0), onInteractCode(0)
    {
        LogManager *logManager = getLogManager();

        IrrXMLReader *xml = createIrrXMLReader( configfile );

        strcpy( xmlFile, configfile );

        if( !xml )
            logManager->warning( "Could not open config file '%s' for '%s'.", configfile, _name );

        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmpCaseInsensitive("sprite", xml->getNodeName()) )
                    {
                        if( xml->getAttributeValue("image") )
                            sprite = getCacheManager()->getSurface( xml->getAttributeValue("image") );
                        else
                            logManager->warning( "No sprite defined in '%s'.", configfile);

                        if( xml->getAttributeValue("mask") )
                            mask = getCacheManager()->getMask( xml->getAttributeValue("mask") );
                        else
                            logManager->warning( "No mask defined in '%s'.", configfile);
                    }
                    if( !strcmpCaseInsensitive("frame", xml->getNodeName()) )
                    {
                        Frame frame;

                        if( xml->getAttributeValue("number") )
                            frame.number = (int) (*xml->getAttributeValue("number"));
                        else
                            logManager->warning("Number not defined for frame in '%s'.", configfile);

                        if( xml->getAttributeValue("x1") )
                        {
                            frame.x1 = xml->getAttributeValueAsInt("x1");
                            frame.y1 = xml->getAttributeValueAsInt("y1");
                            frame.x2 = xml->getAttributeValueAsInt("x2");
                            frame.y2 = xml->getAttributeValueAsInt("y2");
                        }
                        else
                        {
                            /* Default to complete sprite, if available.
                             */
                            if( sprite )
                            {
                                frame.x1 = frame.y1 = 0;
                                frame.x2 = sprite->getWidth();
                                frame.y2 = sprite->getHeight();
                            }
                        }

                        frames.push_back( frame );
                    }
                    if( !strcmpCaseInsensitive("animation", xml->getNodeName()) )
                    {
                        Animation animation;
                        strcpy( animation.name, xml->getAttributeValue("name") );

                        strcpy( animation.frames, xml->getAttributeValue("frames") );
                        animation.numberOfFrames = strlen( animation.frames );

                        if( xml->getAttributeValue("speed") )
                            animation.speed = xml->getAttributeValueAsInt("speed");
                        else
                            animation.speed = 20;

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

                            getEngine()->toPythonCode( &onInteractCode );
                        }
                    }
                    if( !strcmpCaseInsensitive("passable", xml->getNodeName()) )
                    {
                        if( xml->getAttributeValue("value") )
                        {
                            passable = (bool)xml->getAttributeValueAsInt("value");
                        }
                    }
                    break;
            }
        }

        delete xml;

        if( !setAnimation( "stand" ) )
            logManager->warning("StaticObject '%s' does not provide the default 'stand' animation.", configfile );
        speedTimer = 0;
    }

    StaticObject::StaticObject( const char *_name, Surface *_surf, Mask *_mask ): Entity(_name), sprite(_surf), mask(_mask), tileStandingOn(0), currentFrame(0), passable(false), needsUpdate(true), onInteractScript(0), onInteractCode(0)
    {
        /* Create a default frame.
         */
        Frame frame;
        frame.number = 1;
        frame.x1 = frame.y1 = 0;
        frame.x2 = sprite->getWidth();
        frame.y2 = sprite->getHeight();
        frames.push_back( frame );

        /* Create a default animation.
         */
        Animation animation;
        strcpy( animation.name, "stand" );
        strcpy( animation.frames, "1" );
        animation.numberOfFrames = strlen( animation.frames );
        animation.speed = 20;
        animations.push_back( animation );

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

        /* If there is no layer...
         */
        if( !layer )
            return;

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
        bool first = true;
        position.z = 0;
        for( std::list<Tile*>::iterator i = collidingTiles.begin(); i!=collidingTiles.end(); i++ )
        {
            if( (*i)->getObstructionType() != NoObstruction )
            {
                for( int p=0; p<4; p++ )
                {
                    if( ((*i)->getZ(p) > position.z) || first )
                    {
                        position.z = (*i)->getZ(p);
                        first = false;
                    }
                }
            }
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
        char frameNumber = animations[currentAnimation].frames[currentFrame];
        for( unsigned int i=0; i<frames.size(); i++ )
        {
            if( frames[i].number == frameNumber )
            {
                frame = &frames[i];
                i = frames.size();
            }
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

    void StaticObject::setSprite( const char *filename )
    {
        Surface *s = getCacheManager()->getSurface( filename );
        if( s )
            sprite = s;
    }

    Surface *StaticObject::getSprite() const
    {
        return sprite;
    }

    bool StaticObject::setAnimation( const char *aname )
    {

        for( unsigned int i=0; i<animations.size(); i++ )
        {
            if( !strcmpCaseInsensitive( aname, animations[i].name ) )
            {
                currentAnimation = i;
                currentFrame %= animations[i].numberOfFrames;
                animationRunning = true;
                return true;
            }
        }

        currentAnimation = -1;
        return false;
    }

    const char *StaticObject::getAnimation() const
    {
        if( currentAnimation >= 0 )
        {
            return animations[currentAnimation].name;
        }
        else
        {
            getLogManager()->warning( "StaticObject::getAnimation() called while there is no animation set." );
            return "none";
        }
    }

    /*void StaticObject::stopAnimation()
    {
        animationRunning = false;
    }

    void StaticObject::startAnimation()
    {
        animationRunning = true;
    }*/

    void StaticObject::setPassable( bool value )
    {
        passable = value;
    }

    bool StaticObject::isPassable() const
    {
        return passable;
    }

    bool StaticObject::canInteract() const
    {
        return (onInteractCode || onInteractScript);
    }

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

    bool StaticObject::stepTo( Point p )
    {
        getLogManager()->warning("Attempt to step static object '%s'. Warping.\n", this->getName(), p.x, p.y );
        position = p.to(IsometricPoint);
        needsUpdate = true;
        return true;
    }

    void StaticObject::setStandAnimation( bool )
    {
        return;
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