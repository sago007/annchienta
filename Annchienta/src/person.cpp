/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "person.h"

#include "xml/irrXML.h"
using namespace irr;
using namespace io;
#include "auxfunc.h"
#include "personcontrol.h"
#include "inputpersoncontrol.h"
#include "inputmanager.h"
#include "samplepersoncontrol.h"
#include "mapmanager.h"
#include "layer.h"
#include "mask.h"

namespace Annchienta
{

    Person::Person( const char *_name, const char *_configfile ): StaticObject(_name, _configfile), control(0), frozen(false)
    {
        IrrXMLReader *xml = createIrrXMLReader( _configfile );

        if( !xml )
            printf("Could not open config file %s for %s\n", _configfile, _name );

        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    if( !strcmpCaseInsensitive( "control", xml->getNodeName() ) )
                    {
                        const char *typestr = xml->getAttributeValue("type");
                        if( !strcmpCaseInsensitive( "input", typestr ) )
                        {
                            control = new InputPersonControl( this );
                            getInputManager()->setInputControlledPerson( this );
                        }
                        if( !strcmpCaseInsensitive( "sample", typestr ) )
                            control = new SamplePersonControl( this );
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
        control->affect();

        /* Because persons are moving, we need to update
         * every turn.
         */
        needsUpdate = true;

        /* First call the superclass update() method,
         * because we also need to switch frames etc.
         * here.
         */
        StaticObject::update();
    }

    bool Person::move( int x, int y, bool force )
    {
        Point oldPosition = position;

        position.x += x;
        position.y += y;
        mapPosition = position.to( MapPoint );

        /* Adjust animation.
         */
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

        if( force || !layer || (!x && !y) )
            return true;

        std::list<Tile*> oldCollidingTiles = collidingTiles;

        setCollidingTiles();
        setZFromCollidingTiles();

        bool possible = true;

        /* Reject if there are now colliding tiles.
         * (This means the player is probably outside the level.)
         */
        if( possible && collidingTiles.size() <= 0 )
            possible = false;

        /* Reject if the person ascents too high.
         */
        if( possible && oldPosition.z + getMapManager()->getMaxAscentHeight() < position.z )
            possible = false;

        /* Reject if the person descents too deep.
         */
        if( possible && (oldPosition.z - getMapManager()->getMaxDescentHeight() > position.z ) )
            possible = false;

        /* Reject if the person collides with something else.
         */
        Point maskPosition = this->getMaskPosition();
        for( int i=0; possible && layer->getObject(i); i++ )
        {
            StaticObject *so = layer->getObject(i);
            if( (StaticObject*) this != so )
            {
                Point otherMaskPosition( so->getMaskPosition() );
                if( mask->collision( maskPosition.x, maskPosition.y, so->getMask(), otherMaskPosition.x, otherMaskPosition.y ) )
                    possible = false;
            }
        }

        if( !possible )
        {
            position = oldPosition;
            mapPosition = position.to( MapPoint );
            collidingTiles = oldCollidingTiles;
            return false;
        }

        return true;
    }

    bool Person::stepTo( int tx, int ty )
    {
        /* We don't need to take a step if we're close enough.
        */
        if( squaredDistance( position.x, position.y, tx, ty ) <= 25 )
        {
            this->setStandAnimation();
            return false;
        }

        for( int i=0; i<getMapManager()->getUpdatesNeeded(); i++ )
        {

            int x = tx-position.x>0?1:(tx-position.x<0?-1:0),
                y = ty-position.y>0?1:(ty-position.y<0?-1:0);

            bool result;

            if( x )
            {
                if( this->move( x, 0, false ) )
                    return true;
                else
                    if( y )
                        if( this->move( 0, y, false ) )
                            return true;
                        else
                            this->move( x, 0, true );
            }
            else
            {
                this->move( 0, y, true );
            }
        }

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

    void Person::interact()
    {
        if( !layer )
            return;

        StaticObject *interactWith = 0;
        int closest = 0xffffffff;
        Point maskPosition = this->getMaskPosition();

        /* We loop through the objects in the layer to see if we find
         * one where we might interact with.
         */
        for( int i=0; layer->getObject(i); i++ )
        {
            StaticObject *so = layer->getObject(i);

            /* Of course, we don't want to interact with ourselves.
             */
            if( so != (StaticObject*) this )
            {
                /* Find the distance between the objects.
                 */
                int dist = (int)squaredDistance( this->getPosition().x, this->getPosition().y, so->getPosition().x, so->getPosition().y );
    
                /* Check for bounding box collision.
                 */
                Point otherMaskPosition = so->getMaskPosition();
                bool boxCollision = mask->collision( maskPosition.x, maskPosition.y, so->getMask(), otherMaskPosition.x, otherMaskPosition.y, true );
    
                /* If this person collides with an object...
                 */
                if( boxCollision )
                {
                    /* Make sure the Z difference isn't too large. Why: We don't
                     * want the player to be able to talk with eg. someone standing
                     * on a cliff when the player is standing on the ground etc.
                     */
                    if( absValue(this->getPosition().z - so->getPosition().z) < getMapManager()->getMaxAscentHeight() )
                    {
                        /* From all the objects this person collides with, we
                         * only want the one closest to the person.
                         */
                        if( (dist<=closest) || (!interactWith) )
                        {
                            closest = dist;
                            interactWith = so;
                        }
                    }
                }
            }
        }

        if( interactWith )
        {
            setActiveObject( this );
            setPassiveObject( interactWith );
            interactWith->onInteract();
        }
    }

    void Person::setStandAnimation()
    {
        bool setAnimationResult;

        //if( !strcmpCaseInsensitive("aelaan", getName() ) )
          //  printf("Setting stand animation %d.\n", heading);

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
            //printf("Could not find animation.\n");
            this->setAnimation("stand");
        }

        //printf("Animations is now: %s\n", animations[currentAnimation].name );
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

        setStandAnimation();
    }

};
