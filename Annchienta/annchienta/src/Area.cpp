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
#include "VideoManager.h"
#include "Tile.h"

namespace Annchienta
{
    Area::Area( Point _p1, Point _p2, bool visible )
    {
        p1 = _p1.to( IsometricPoint );
        p2 = _p2.to( IsometricPoint );
        this->visible = visible;

        mp1 = Point( IsometricPoint, p1.x, p1.y );
        mp2 = Point( IsometricPoint, p1.x, p2.y );
        mp3 = Point( IsometricPoint, p2.x, p2.y );
        mp4 = Point( IsometricPoint, p2.x, p1.y );
        mp1.convert( MapPoint );
        mp2.convert( MapPoint );
        mp3.convert( MapPoint );
        mp4.convert( MapPoint );

        onCollisionCode = onCollisionScript = 0;
    }

    Area::~Area()
    {
    }

    void Area::setVisible( bool visible )
    {
        this->visible = visible;
    }

    bool Area::isVisible() const
    {
        return visible;
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
        /* Remove any previous code. */
        if( onCollisionCode )
            delete[] onCollisionCode;

        /* Store the new code. */
        onCollisionCode = new char[strlen(code)+1];
        strcpy( onCollisionCode, code );

        /* Connvert it to python code. */
        getEngine()->toPythonCode( &onCollisionCode );
    }

    bool Area::hasPoint( Point point )
    {
        /* Make sure we have the right kind of point. */
        point.convert( IsometricPoint );
        return point.isEnclosedBy( &p1, &p2 );
    }

    bool Area::hasTile( Tile *tile )
    {
        for( int i=0; i<4; i++ )
            if( !hasPoint( tile->getPoint(i) ) )
                return false;
        return true;
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
