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

    void Person::move( int x, int y, bool force )
    {
        position.x += x;
        position.y += y;

        
    }

};
