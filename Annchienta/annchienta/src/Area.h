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

#ifndef ANNCHIENTA_AREA_H
#define ANNCHIENTA_AREA_H

#include "Point.h"

namespace Annchienta
{

    /** An area is a rectangular field on a map.
     *  It is used to trigger code when the player
     *  walks into one of these areas, thus adding
     *  interactivity to maps.
     */
    class Area
    {
        private:
            Point p1, p2;

            char *onCollisionScript, *onCollisionCode;

        public:

            /** Create a new area.
             *  \param p1 The upper left corner of the area.
             *  \param p2 The bottom right corner of the area.
             */
            Area( Point p1, Point p2 );
            ~Area();

            /** Sets the script to be executed on collision
             *  with the player.
             *  \param filename Filename of the script you want to be executed.
             */
            void setOnCollisionScript( const char *filename );

            /** Sets the code to be executed on collision
             *  with the player.
             *  \param code The code you want to be executed.
             */
            void setOnCollisionCode( const char *code );

            /** Checks if the given Point lies in this area.
             */
            bool hasPoint( Point point );

            /** Trigger collision. This is done by the MapManager,
             *  but can also be emulated manually.
             */
            void onCollision();
    };

};

#endif
