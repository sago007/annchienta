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

#include "StaticObject.h"

#include <Python.h>
#include "xml/irrXML.h"
using namespace irr;
using namespace io;
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
    /** A helping structure to hold a frame.
     */
    struct Frame
    {
        char number;
        int x1, y1, x2, y2;
    };

    /** A helping structure to hold an animation.
     */
    struct Animation
    {
        char name[DEFAULT_STRING_SIZE];
        char frames[SMALL_STRING_SIZE];
        int numberOfFrames;
        int speed;
    };
 
    StaticObject *activeObject=0, *passiveObject=0;

    StaticObject::StaticObject( const char *_name, const char *configfile ): Entity(_name), sprite(0), mask(0), tileStandingOn(0), currentFrame(0), passable(false), onInteractScript(0), onInteractCode(0)
    {
        /* We might need to log stuff here. */
        LogManager *logManager = getLogManager();

        /* Open up our file and store the filename for later use. */
        IrrXMLReader *xml = createIrrXMLReader( configfile );
        strcpy( xmlFile, configfile );

        /* Make sure the config file exists. */
        if( !xml )
            logManager->error( "Could not open config file '%s' for '%s'.", configfile, _name );

        /* Read through the entire file. */
        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmp("sprite", xml->getNodeName()) )
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
                    if( !strcmp("frame", xml->getNodeName()) )
                    {
                        Frame *frame = new Frame;

                        if( xml->getAttributeValue("number") )
                            frame->number = (int) (*xml->getAttributeValue("number"));
                        else
                            logManager->warning("Number not defined for frame in '%s'.", configfile);

                        if( xml->getAttributeValue("x1") && xml->getAttributeValue("y1") &&
                            xml->getAttributeValue("x2") && xml->getAttributeValue("y2") )
                        {
                            frame->x1 = xml->getAttributeValueAsInt("x1");
                            frame->y1 = xml->getAttributeValueAsInt("y1");
                            frame->x2 = xml->getAttributeValueAsInt("x2");
                            frame->y2 = xml->getAttributeValueAsInt("y2");
                        }
                        else
                        {
                            /* Default to complete sprite, if available. */
                            if( sprite )
                            {
                                frame->x1 = frame->y1 = 0;
                                frame->x2 = sprite->getWidth();
                                frame->y2 = sprite->getHeight();
                            }
                        }

                        frames.push_back( frame );
                    }
                    if( !strcmp("animation", xml->getNodeName()) )
                    {
                        Animation *animation = new Animation;
                        strcpy( animation->name, xml->getAttributeValue("name") );

                        strcpy( animation->frames, xml->getAttributeValue("frames") );
                        animation->numberOfFrames = strlen( animation->frames );

                        if( xml->getAttributeValue("speed") )
                            animation->speed = xml->getAttributeValueAsInt("speed");
                        else
                            animation->speed = 20;

                        animations.push_back( animation );
                    }
                    if( !strcmp("oninteract", xml->getNodeName()) )
                    {
                        if( xml->getAttributeValue("script") )
                        {
                            setOnInteractScript( xml->getAttributeValue("script") );
                            onInteractCode = 0;
                        }
                        else
                        {
                            xml->read();
                            setOnInteractCode( xml->getNodeData() );
                            xml->read();
                            onInteractScript = 0;
                        }
                    }
                    if( !strcmp("passable", xml->getNodeName()) )
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
            logManager->warning("StaticObject '%s' (loaded from '%s') does not provide the default 'stand' animation.", name, configfile );
        speedTimer = 0;
    }

    StaticObject::StaticObject( const char *_name, Surface *_surf, Mask *_mask ): Entity(_name), sprite(_surf), mask(_mask), tileStandingOn(0), currentFrame(0), passable(false), onInteractScript(0), onInteractCode(0)
    {
        /* Create a default frame. */
        Frame *frame = new Frame;
        frame->number = '1';
        frame->x1 = frame->y1 = 0;
        frame->x2 = sprite->getWidth();
        frame->y2 = sprite->getHeight();
        frames.push_back( frame );

        /* Create a default animation. */
        Animation *animation = new Animation;
        strcpy( animation->name, "stand" );
        strcpy( animation->frames, "1" );
        animation->numberOfFrames = strlen( animation->frames );
        animation->speed = 20;
        animations.push_back( animation );

        /* Set the default animation. */
        setAnimation( "stand" );
        speedTimer = 0;
    }

    StaticObject::~StaticObject()
    {
        for( unsigned int i=0; i<frames.size(); i++ )
            delete frames[i];

        for( unsigned int i=0; i<animations.size(); i++ )
            delete animations[i];

        if( onInteractCode )
            delete[] onInteractCode;
        if( onInteractScript )
            delete[] onInteractScript;
    }

    void StaticObject::calculateCollidingTiles()
    {
        /* Erase previous colliding tiles. */
        collidingTiles.clear();

        /* If there is no layer... */
        if( !layer )
            return;

        Point pos = this->getMaskPosition(), point;

        /* First we need to collect all colliding tiles.
         * loop though all of them and add them to collidingTiles
         * if needed. */
        for( int ty=0; ty<layer->getHeight(); ty++ )
        {
            for( int tx=0; tx<layer->getWidth(); tx++ )
            {
                Tile *tile = layer->getTile( tx, ty );
                point = tile->getMaskPosition();
                if( mask->collision( pos.x, pos.y, layer->getTileSet()->getMask(), point.x, point.y ) )
                    collidingTiles.push_back( tile );

                if( tile->hasPoint(position) )
                {
                    tileStandingOn = tile;
                }
            }

        }

        /* Do a depthsort on them. */
        collidingTiles.sort( DepthSortPredicate );
    }

    float StaticObject::getZFromCollidingTiles()
    {
        /* We need the MapManager. */
        MapManager *mapManager = getMapManager();

        /* Now, we set out Z to the highest one of the colliding tiles. */
        bool first = true;
        int newZ = 0;
        for( std::list<Tile*>::iterator i = collidingTiles.begin(); i!=collidingTiles.end(); i++ )
        {
            if( (*i)->getObstructionType() != NoObstruction )
            {
                for( int p=0; p<4; p++ )
                {
                    if( ((*i)->getZ(p) > newZ) || first )
                    {
                        newZ = (*i)->getZ(p);
                        first = false;
                    }
                }
            }
        }

        return newZ;
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
            if( speedTimer >= animations[currentAnimation]->speed )
            {
                currentFrame++;
                if( currentFrame >= animations[currentAnimation]->numberOfFrames )
                    currentFrame = 0;
                speedTimer = 0;
            }
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
        char frameNumber = animations[currentAnimation]->frames[currentFrame];
        for( unsigned int i=0; i<frames.size(); i++ )
        {
            if( frames[i]->number == frameNumber )
            {
                frame = frames[i];
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

    Mask *StaticObject::getMask() const
    {
        return mask;
    }

    void StaticObject::setPosition( Point _position )
    {
        position = _position.to( IsometricPoint );
        mapPosition = position.to( MapPoint );

        calculateCollidingTiles();
        mapPosition.z = position.z = getZFromCollidingTiles();
    }

    Point StaticObject::getPosition() const
    {
        return position;
    }

    Point StaticObject::getMaskPosition() const
    {
        return Point( MapPoint, mapPosition.x - (mask->getWidth()>>1), mapPosition.y - mask->getHeight(), mapPosition.z );
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
            if( !strcmp( aname, animations[i]->name ) )
            {
                currentAnimation = i;
                currentFrame %= animations[i]->numberOfFrames;
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
            return animations[currentAnimation]->name;
        }
        else
        {
            getLogManager()->warning( "StaticObject::getAnimation() called while there is no animation set." );
            return "none";
        }
    }

    void StaticObject::setPassable( bool value )
    {
        passable = value;
    }

    bool StaticObject::isPassable() const
    {
        return passable;
    }

    void StaticObject::setOnInteractScript( const char *script )
    {
        if( onInteractScript )
            delete[] onInteractScript;

        onInteractScript = new char[ strlen(script)+1 ];
        strcpy( onInteractScript, script );
    }

    void StaticObject::setOnInteractCode( const char *code )
    {
        if( onInteractCode )
            delete[] onInteractCode;

        onInteractCode = new char[ strlen(code)+1 ];
        strcpy( onInteractCode, code );
        getEngine()->toPythonCode( &onInteractCode );
    }

    bool StaticObject::canInteract() const
    {
        return (onInteractCode || onInteractScript);
    }

    void StaticObject::onInteract()
    {
        Engine *engine = getEngine();

        if( onInteractCode )
            engine->runPythonCode( onInteractCode );
        if( onInteractScript )
            engine->runPythonScript( onInteractScript );
    }

    void StaticObject::freeze( bool )
    {
        return;
    }

    bool StaticObject::stepTo( Point p )
    {
        getLogManager()->warning("Attempt to step static object '%s'. Warping.", this->getName(), p.x, p.y );
        setPosition( p );
        return false;
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
