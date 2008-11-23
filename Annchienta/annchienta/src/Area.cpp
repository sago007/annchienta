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

#include "Area.h"

#include <cstring>
#include <Python.h>
#include "Engine.h"

namespace Annchienta
{
    Area::Area( Point _p1, Point _p2 )
    {
        p1 = _p1.to( IsometricPoint );
        p2 = _p2.to( IsometricPoint );

        onCollisionCode = onCollisionScript = 0;
    }

    Area::~Area()
    {
    }

    void Area::setOnCollisionScript( const char *script )
    {
        if( onCollisionScript )
            delete[] onCollisionScript;
        onCollisionScript = new char[strlen(script)+1];
        strcpy( onCollisionScript, script );
    }

    void Area::setOnCollisionCode( const char *code )
    {
        if( onCollisionCode )
            delete[] onCollisionCode;
        onCollisionCode = new char[strlen(code)+1];
        strcpy( onCollisionCode, code );

        getEngine()->toPythonCode( &onCollisionCode );
    }

    bool Area::hasPoint( Point point )
    {
        point.convert( IsometricPoint );
        return point.isEnclosedBy( &p1, &p2 );
    }

    void Area::onCollision()
    {
        Engine *engine = getEngine();

        if( onCollisionCode )
            engine->runPythonCode( onCollisionCode );
        if( onCollisionScript )
            engine->runPythonScript( onCollisionScript );
    }

};
