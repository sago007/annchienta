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

        if( force || !layer )
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

};
