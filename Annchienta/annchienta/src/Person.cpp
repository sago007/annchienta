/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "Person.h"

#include "xml/irrXML.h"
using namespace irr;
using namespace io;
#include "GeneralFunctions.h"
#include "PersonControl.h"
#include "InputPersonControl.h"
#include "InputManager.h"
#include "SamplePersonControl.h"
#include "MapManager.h"
#include "Layer.h"
#include "Mask.h"
#include "InputManager.h"
#include "Area.h"
#include "Tile.h"
#include "LogManager.h"

namespace Annchienta
{

    Person::Person( const char *_name, const char *_configfile ): StaticObject(_name, _configfile), control(0), frozen(false)
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
                        if( !strcmp( "null", typestr ) )
                            control = 0;
                    }
                    break;
            }
        }

        delete xml;

        setAnimation( "stand" );
        heading = 0;
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

    void Person::update()
    {
        /* Let the control update this.
         */
        if( control )
            control->affect();

        /* Because persons are moving, we need to update
         * every turn.
         */
        needsUpdate = true;

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
        position.x += x;
        position.y += y;
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

        /* Always execute move under certain conditions. */
        if( force || !layer || (!x && !y) )
            return true;

        /* Keep a copy of our old tiles. As I said, we might
         * need to return to our old position. */
        std::list<Tile*> oldCollidingTiles = collidingTiles;

        /* Calculate the tiles we're colliding with and
         * our new Z. */
        calculateCollidingTiles();
        calculateZFromCollidingTiles();

        /* It is possible to move by default. Then, check
         * for some rejections... */
        bool possible = true;

        /* Reject if there are now colliding tiles.
         * (This means the player is probably outside the level.) */
        if( possible && collidingTiles.size() <= 0 )
            possible = false;

        /* Reject if the person ascents too high. */
        if( possible && oldPosition.z + getMapManager()->getMaxAscentHeight() < position.z )
            possible = false;

        /* Reject if the person descents too deep. */
        if( possible && (oldPosition.z - getMapManager()->getMaxDescentHeight() > position.z ) )
            possible = false;

        /* Reject if the person steps on a nulltile, or if that
         * tile is fully obstructed. */
        for( std::list<Tile*>::iterator i = collidingTiles.begin(); possible && i!=collidingTiles.end(); i++ )
        {
            if( (*i)->isNullTile() || ((*i)->getObstructionType() == FullObstruction) )
                possible = false;
        }

        /* Reject if the person collides with something else. */
        Point maskPosition = this->getMaskPosition();
        for( int i=0; possible && layer->getObject(i); i++ )
        {
            StaticObject *so = layer->getObject(i);
            if( (StaticObject*) this != so )
            {
                /* Check this only if they're both unpassable. */
                if( !so->isPassable() && !this->isPassable())
                {
                    Point otherMaskPosition( so->getMaskPosition() );
                    if( mask->collision( maskPosition.x, maskPosition.y, so->getMask(), otherMaskPosition.x, otherMaskPosition.y ) )
                        possible = false;
                }
            }
        }

        /* If the whole thing ended up not being possible,
         * revert everything to the original state before
         * we moved. */
        if( !possible )
        {
            position = oldPosition;
            mapPosition = position.to( MapPoint );
            collidingTiles = oldCollidingTiles;
            this->setStandAnimation();
            return false;
        }

        return true;
    }

    bool Person::stepTo( Point target )
    {
        target.convert( IsometricPoint );
        int tx = target.x, ty = target.y;

        /* We don't need to take a step if we're close enough.
        */
        if( squaredDistance( (float)position.x, (float)position.y, (float)tx, (float)ty ) <= 25 )
        {
            //printf("We're close enough.\n");
            this->setStandAnimation();
            return false;
        }

        for( int i=0; i<getMapManager()->getUpdatesNeeded(); i++ )
        {

            int x = tx-position.x>0?1:(tx-position.x<0?-1:0),
                y = ty-position.y>0?1:(ty-position.y<0?-1:0);

            if( x )
                this->move( x, 0, true );
            else
                this->move( 0, y, true );
        }

        //printf("Reached the end.\n");

        return true;
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

        if( absValue( xdiff ) > absValue( ydiff ) )
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
