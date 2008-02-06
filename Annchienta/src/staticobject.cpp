/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "staticobject.h"

#include "xml/irrXML.h"
using namespace irr;
using namespace io;

namespace Annchienta
{

    StaticObject::StaticObject( const char *_name, const char *configfile ): Entity(_name)
    {
        IrrXMLReader *xml = createIrrXMLReader( configfile );

        if( !xml )
            printf("Could not open config file %s for %s\n", configfile, _name );

        while( xml && xml->read() )
        {
            switch( xml->getNodeType() )
            {
                case EXN_ELEMENT:
                    break;
            }
        }

        delete xml;
    }

    StaticObject::~StaticObject()
    {
    }

    void StaticObject::draw()
    {
        if( this->isDrawn() )
            return;

        this->setDrawn( true );
    }

    int StaticObject::getDepthSortY() const
    {
        return 20;
    }

    void StaticObject::setPosition( Point _position )
    {
        position = _position;
    }

    Point StaticObject::getPosition() const
    {
        return position;
    }

};
