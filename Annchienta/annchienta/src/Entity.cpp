/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "Entity.h"

#include <cstdio>
#include <cstring>

namespace Annchienta
{

    Entity::Entity( const char *_name ): layer(0)
    {
        if( _name )
            strcpy( name, _name );
    }

    Entity::~Entity()
    {
    }

    void Entity::setDrawn( bool d )
    {
        drawn = d;
    }

    bool Entity::isDrawn() const
    {
        return drawn;
    }

    void Entity::setName( const char *_name )
    {
        strcpy( name, _name );
    }

    const char *Entity::getName() const
    {
        return name;
    }

    void Entity::setLayer( Layer *_layer )
    {
        layer = _layer;
    }

    Layer *Entity::getLayer() const
    {
        return layer;
    }

};
