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
            /* The position indicates the bottom center, like
             *      ___________
             *      |         |
             *      |         |
             *      |         |
             *      |__(pos)__|
             *
             * This almost equals the "depth sort y".
             */
            Point position;
            Point mapPosition;
            Surface *sprite;
            Mask *mask;

            std::vector<Frame> frames;
            std::vector<Animation> animations;
            std::list<Tile*> collidingTiles;
            Tile *tileStandingOn;

            int currentAnimation, currentFrame, speedTimer;
            bool animationRunning;

            bool needsUpdate;

            char *onInteractScript, *onInteractCode;

            char xmlFile[512];

        public:
            StaticObject( const char *name, const char *configfile );
            StaticObject( const char *name, Surface *surf, Mask *mask );
            virtual ~StaticObject();

            void setCollidingTiles();
            void setZFromCollidingTiles();

            virtual EntityType getEntityType() const;

            virtual void update();
            virtual void draw();
            virtual int getDepth();

            virtual void setPosition( Point );
            virtual Point getPosition() const;
            virtual Point getMaskPosition() const;
            virtual Mask *getMask() const;

            const char *getXmlFile() const;

            virtual bool setAnimation( const char *animationName );
            virtual const char *getAnimation() const;
            //virtual void stopAnimation();
            //virtual void startAnimation();

            virtual bool canInteract() const;
            virtual void onInteract();

            /* Should only be used for Persons, but this is needed because of
             * abstracting to Python scripts. Always returns true.
             */
            virtual void freeze( bool );
            virtual bool stepTo( int x, int y);
            virtual void lookAt( StaticObject *other );
    };

    #ifndef SWIG
        void setActiveObject( StaticObject *object );
        void setPassiveObject( StaticObject *object );
    #endif

    /* Used in scenes: active->interactor
     *                 passive->interacted with
     */
    StaticObject *getActiveObject();
    StaticObject *getPassiveObject();
};

#endif
