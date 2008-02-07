/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_STATICOBJECT_H
#define ANNCHIENTA_STATICOBJECT_H

#include "entity.h"

#include <vector>
#include <list>
#include "point.h"

namespace Annchienta
{
    class Surface;
    class Tile;
    class Mask;

    #ifndef SWIG
        struct Frame
        {
            int number;
            int x1, y1, x2, y2;
        };

        struct Animation
        {
            char name[512];
            char frames[128];
            int numberOfFrames;
            int speed;
        };
    #endif

    class StaticObject: public Entity
    {
        protected:
            Point position;
            Point mapPosition;
            Surface *sprite;
            Mask *mask;

            std::vector<Frame> frames;
            std::vector<Animation> animations;
            std::list<Tile*> collidingTiles;

            int currentAnimation, currentFrame, speedTimer;

            bool needsUpdate;

        public:
            StaticObject( const char *name, const char *configfile );
            virtual ~StaticObject();

            virtual void update();
            virtual void draw();
            virtual int getDepthSortY() const;

            virtual void setPosition( Point );
            virtual Point getPosition() const;

            virtual void setAnimation( const char *animationName );
    };
};

#endif
