/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
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
