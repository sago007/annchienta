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
#include "mapmanager.h"
#include "layer.h"
#include "mask.h"

namespace Annchienta
{

    Person::Person( const char *_name, const char *_configfile ): StaticObject(_name, _configfile), control(0)
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
                            control = new InputPersonControl( this );
                    }
                    break;
            }
        }

        delete xml;

        setAnimation( "stand" );
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
            this->setAnimation("walknorth");
        if( x>0 )
            this->setAnimation("walksouth");
        if( y<0 )
            this->setAnimation("walkeast");
        if( y>0 )
            this->setAnimation("walkwest");
        if( !x && !y )
            this->stopAnimation();

        if( force || !layer || (!x && !y) )
            return true;

        std::list<Tile*> oldCollidingTiles = collidingTiles;

        setCollidingTiles();
        setZFromCollidingTiles();

        bool possible = true;

        /* Reject if the person ascents too high.
         */
        if( oldPosition.z + getMapManager()->getMaxAscentHeight() < position.z )
            possible = false;

        /* Reject if the person descents too deep.
         */
        if( possible && (oldPosition.z - getMapManager()->getMaxDescentHeight() > position.z ) )
            possible = false;

        /* Reject if the person collides with something else.
         */
        Point maskPosition = this->getMaskPosition();
        for( int i=0; possible && layer->getStaticObject(i); i++ )
        {
            StaticObject *so = layer->getStaticObject(i);
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

    void Person::setInputControl()
    {
        if( control )
            delete control;
        control = new InputPersonControl( this );
    }

    void Person::interact()
    {
        if( !layer )
            return;

        StaticObject *interactWith = 0;
        int closest = -1;
        Point maskPosition = this->getMaskPosition();
        for( int i=0; layer->getStaticObject(i); i++ )
        {
            StaticObject *so = layer->getStaticObject(i);

            int dist = (int)squaredDistance( this->getPosition().x, this->getPosition().y, so->getPosition().x, so->getPosition().y );

            Point otherMaskPosition = so->getMaskPosition();
            bool boxCollision = mask->collision( maskPosition.x, maskPosition.y, so->getMask(), otherMaskPosition.x, otherMaskPosition.y, true );

            if( dist < squaredInteractDistance || boxCollision )
            {
                if( absValue(this->getPosition().z - so->getPosition().z) < getMapManager()->getMaxAscentHeight() )
                {
                    if( (dist<=closest) || (closest<=0) || (!interactWith) )
                    {
                        closest = dist;
                        interactWith = so;
                    }
                    else
                    {
                        printf("Not interacting with %s because not closest.\n", so->getName() );
                    }
                }
                else
                {
                        printf("Not interacting with %s because Z not right.\n", so->getName() );
                }
            }
            else
            {
                printf("Not interacting with %s because distance too large.\n", so->getName() );
            }
        }

        if( interactWith )
        {
            setActiveObject( this );
            setPassiveObject( interactWith );
            interactWith->onInteract();
        }
    }
};
