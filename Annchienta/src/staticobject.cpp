/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "staticobject.h"

namespace Annchienta
{

    StaticObject::StaticObject(): Entity("sprite")
    {
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

};
