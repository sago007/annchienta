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
