/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_STATICOBJECT_H
#define ANNCHIENTA_STATICOBJECT_H

#include "entity.h"

#include <vector>
#include "point.h"

namespace Annchienta
{
    #ifndef SWIG
        struct SpriteArea
        {
            int number;
            int x1, y1, x2, y2;
        };

        struct SpriteAnimation
        {
            char name[512];
            char array[128];
        };
    #endif

    class StaticObject: public Entity
    {
        protected:
            Point position;

            std::vector<SpriteArea*> spriteAreas;
            std::vector<SpriteAnimation*> spriteAnimations;

        public:
            StaticObject( const char *name, const char *configfile );
            ~StaticObject();

            virtual void draw();
            virtual int getDepthSortY() const;

            virtual void setPosition( Point );
            virtual Point getPosition() const;
    };
};

#endif
