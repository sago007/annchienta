/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_AREA_H
#define ANNCHIENTA_AREA_H

#include "Point.h"

namespace Annchienta
{

    class Area
    {
        private:
            Point p1, p2;

            char *onCollisionScript, *onCollisionCode;

        public:
            Area( Point p1, Point p2 );
            ~Area();

            void setOnCollisionScript( const char * );
            void setOnCollisionCode( const char * );

            bool hasPoint( Point point );

            void onCollision();
    };

};

#endif
