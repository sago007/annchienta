/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
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
