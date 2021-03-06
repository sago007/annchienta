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

#include "Person.h"

#include "xml/irrXML.h"
using namespace irr;
using namespace io;
#include "PersonControl.h"
#include "InputPersonControl.h"
#include "InputManager.h"
#include "SamplePersonControl.h"
#include "FollowPathPersonControl.h"
#include "MapManager.h"
#include "MathManager.h"
#include "Layer.h"
#include "Mask.h"
#include "InputManager.h"
#include "Area.h"
#include "Tile.h"
#include "LogManager.h"
#include "Vector.h"

namespace Annchienta
{

    Person::Person( const char *_name, const char *_configfile ): StaticObject(_name, _configfile), control(0)
    {
        LogManager *logManager = getLogManager();

        IrrXMLReader *xml = createIrrXMLReader( _configfile );

        if( !xml )
            logManager->warning("Could not open config file '%s' for '%s'.", _configfile, _name );

        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmp( "control", xml->getNodeName() ) )
                    {
                        const char *typestr = xml->getAttributeValue("type");
                        if( !strcmp( "input", typestr ) )
                        {
                            control = new InputPersonControl( this );
                            getInputManager()->setInputControlledPerson( this );
                        }
                        if( !strcmp( "sample", typestr ) )
                            control = new SamplePersonControl( this );
                        if( !strcmp( "followpath", typestr ) )
                        {
                            FollowPathPersonControl *followPathPersonControl = new FollowPathPersonControl( this );

                            /* Read in all path points. */
                            while( xml->read() && strcmp("control", xml->getNodeName()) )
                            {
                                if( xml->getNodeType()==EXN_ELEMENT && !strcmp( xml->getNodeName(), "point" ) )
                                {
                                    Point point;

                                    if( xml->getAttributeValue("isox") )
                                    {
                                        point = Point( IsometricPoint, xml->getAttributeValueAsInt("isox"), xml->getAttributeValueAsInt("isoy"), 0 );
                                    }
                                    else if( xml->getAttributeValue("mapx") )
                                    {
                                        point = Point( MapPoint, xml->getAttributeValueAsInt("mapx"), xml->getAttributeValueAsInt("mapy"), 0 );
                                    }
                                    else if( xml->getAttributeValue("tilex") )
                                    {
                                        point = Point( TilePoint, xml->getAttributeValueAsInt("tilex"), xml->getAttributeValueAsInt("tiley"), 0 );
                                    }
                                    
                                    followPathPersonControl->addPoint( point );
                                }
                            }

                            control = followPathPersonControl;
                        }
                        if( !strcmp( "null", typestr ) )
                            control = 0;
                    }
                    break;
                default:
                    break;
            }
        }

        delete xml;

        setAnimation( "stand" );
        frozen = false;
        heading = 0;
        speed = 1.0;
    }

    Person::~Person()
    {
        if( control )
            delete control;
    }

    EntityType Person::getEntityType() const
    {
        return PersonEntity;
    }

    void Person::setSpeed( float speed )
    {
        this->speed = speed;
    }

    float Person::getSpeed() const
    {
        return speed;
    }

    void Person::update()
    {
        /* Let the control update this.
         */
        if( control && !frozen )
        {
            control->affect();
        }

        /* Check for collisions with areas. Only not check in InteractiveMode.
         */
        if( this==getInputManager()->getInputControlledPerson() && getInputManager()->getInputMode()==InteractiveMode )
            collisionWithLayerAreas();

        /* First call the superclass update() method,
         * because we also need to switch frames etc.
         * here.
         */
        StaticObject::update();
    }

    bool Person::move( int x, int y, bool force )
    {
        /* Do nothing when frozen. */
        if( !force && this->isFrozen() )
            return false;

        /* Store our old position, as we might need to
         * return there if this move gets not accepted. */
        Point oldPosition = position;

        /* Calculate the new position. */
        position.x += x*speed;
        position.y += y*speed;
        mapPosition = position.to( MapPoint );

        /* Adjust animation based on the direction our
         * Person is heading now. */
        if( x<0 )
        {
            heading = 0;
            this->setAnimation("walknorth");
        }
        if( y<0 )
        {
            heading = 1;
            this->setAnimation("walkeast");
        }
        if( x>0 )
        {
            heading = 2;
            this->setAnimation("walksouth");
        }
        if( y>0 )
        {
            heading = 3;
            this->setAnimation("walkwest");
        }
        if( !x && !y )
        {
            this->setStandAnimation();
        }

        /* Keep a copy of our old tiles. As I said, we might
         * need to return to our old position. */
        std::list<Tile*> oldCollidingTiles = collidingTiles;

        /* Calculate the tiles we're colliding with and
         * our new Z. */
        calculateCollidingTiles();
        position.z = getZFromCollidingTiles();

        /* Always execute move under certain conditions. */
        if( force || !layer || (!x && !y) )
            return true;

        /* It is possible to move by default. Then, check
         * for some rejections... */
        bool possible = true;

        /* Reject if there are no colliding tiles.
         * (This means the player is probably outside the level.) */
        if( collidingTiles.size() <= 0 )
            possible = false;

        /* Reject if the person ascents too high. */
        else if( possible && oldPosition.z + getMapManager()->getMaxAscentHeight() < position.z )
            possible = false;

        /* Reject if the person descents too deep. */
        else if( possible && (oldPosition.z - getMapManager()->getMaxDescentHeight() > position.z ) )
            possible = false;

        /* Reject if the person steps on a nulltile, or if that
         * tile is fully obstructed. */
        for( std::list<Tile*>::iterator i = collidingTiles.begin(); possible && i!=collidingTiles.end(); i++ )
        {
            if( (*i)->isNullTile() || ((*i)->getObstructionType() == FullObstruction) )
                possible = false;
        }

        /* Reject if the person collides with something else. */
        if( possible && collidesWithOtherObjects() )
            possible = false;

        /* If the whole thing ended up not being possible,
         * revert everything to the original state before
         * we moved. */
        if( !possible )
        {
            position = oldPosition;
            mapPosition = position.to( MapPoint );
            collidingTiles = oldCollidingTiles;
            this->setStandAnimation();
        }
        else
        {
            MathManager *mathManager = getMathManager();

            /* Now, we update the Z coordinate seperately to
             * "smooth out" going up and down. */
            if( mathManager->abs( position.z - oldPosition.z ) > 2*speed )
            {
                if( position.z > oldPosition.z )
                    position.z = oldPosition.z + 2*speed;
                else
                    position.z = oldPosition.z - 2*speed;
            }
        }

        return possible;
    }

    bool Person::stepTo( Point target, bool force )
    {
        target.convert( IsometricPoint );
        int tx = target.x, ty = target.y;

        /* We don't need to take a step if we're close enough. Use
         * a vector to calculate the distance. */
        Vector diffVector( position.x-tx, position.y-ty );
        if( diffVector.lengthSquared() <= 25 )
        {
            this->setStandAnimation();
            return false;
        }

        /* If we were able to move. */
        bool result = true;

        /* Move just enough as necessary. */
        for( int i=0; i<getMapManager()->getUpdatesNeeded(); i++ )
        {

            int x = tx-position.x>0?1:(tx-position.x<0?-1:0),
                y = ty-position.y>0?1:(ty-position.y<0?-1:0);

            if( x )
                result = move( x, 0, force );
            else
                result = move( 0, y, force );
        }

        return result;
    }

    void Person::freeze( bool f )
    {
        frozen = f;
        if( frozen )
            this->setStandAnimation();
    }

    bool Person::isFrozen() const
    {
        return frozen;
    }

    void Person::setControl( PersonControl *personControl )
    {
        if( control )
            delete control;
        control = personControl;
    }

    void Person::setInputControl()
    {
        if( control )
            delete control;
        control = new InputPersonControl( this );
        getInputManager()->setInputControlledPerson( this );
    }

    void Person::setSampleControl()
    {
        if( control )
            delete control;
        control = new SamplePersonControl( this );
    }

    void Person::setNullControl()
    {
        if( control )
            delete control;
        control = 0;
    }

    void Person::setStandAnimation( bool forceFromHeading )
    {
        bool setAnimationResult;

        /* Already stand animation, return.
         */
        if( !forceFromHeading && strstr(getAnimation(), "stand") )
            return;

        switch( heading )
        {
            case 0:
                setAnimationResult = this->setAnimation("standnorth");
                break;
            case 1:
                setAnimationResult = this->setAnimation("standeast");
                break;
            case 2:
                setAnimationResult = this->setAnimation("standsouth");
                break;
            case 3: default:
                setAnimationResult = this->setAnimation("standwest");
                break;
        }
        if( !setAnimationResult )
        {
            this->setAnimation("stand");
        }
    }

    void Person::lookAt( StaticObject *other )
    {
        int xdiff = this->getPosition().x - other->getPosition().x,
            ydiff = this->getPosition().y - other->getPosition().y;

        MathManager *mathManager = getMathManager();

        if( mathManager->abs( xdiff ) > mathManager->abs( ydiff ) )
        {
            if( xdiff < 0 )
                heading = 2;
            else
                heading = 0;
        }
        else
        {
            if( ydiff < 0 )
                heading = 3;
            else
                heading = 1;
        }

        setStandAnimation(true);
    }

    void Person::collisionWithLayerAreas()
    {
        setActiveObject( this );
        Area *area;
        for( int i=0; area = layer->getArea(i); i++ )
        {
            if( area->hasPoint( position ) )
                area->onCollision();
        }
    }

};
