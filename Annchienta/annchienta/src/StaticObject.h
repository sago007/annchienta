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

#ifndef ANNCHIENTA_STATICOBJECT_H
#define ANNCHIENTA_STATICOBJECT_H

#include "Entity.h"

#include <vector>
#include <list>
#include "Point.h"
#include "Engine.h"

namespace Annchienta
{
    class Surface;
    class Tile;
    class Mask;
    class Frame;
    class Animation;

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

            std::vector<Frame*> frames;
            std::vector<Animation*> animations;
            std::list<Tile*> collidingTiles;
            Tile *tileStandingOn;

            int currentAnimation, currentFrame, speedTimer;

            bool passable;

            bool needsUpdate;

            char *onInteractScript, *onInteractCode;

            char xmlFile[DEFAULT_STRING_SIZE];

        public:
            StaticObject( const char *name, const char *configfile );
            StaticObject( const char *name, Surface *surf, Mask *mask );
            virtual ~StaticObject();

            void calculateCollidingTiles();
            void calculateZFromCollidingTiles();

            virtual EntityType getEntityType() const;

            virtual void update();
            virtual void draw();
            virtual int getDepth();

            virtual void setPosition( Point );
            virtual Point getPosition() const;
            virtual Point getMaskPosition() const;
            Mask *getMask() const;

            const char *getXmlFile() const;

            /** Should be used with care, because the frame settings
             *  stay the same.
             *  \param filename Filename of the new sprite.
             */
            virtual void setSprite( const char *filename );

            /** \return return the current sprite used.
             */
            Surface *getSprite() const;

            bool setAnimation( const char *animationName );
            const char *getAnimation() const;

            virtual void setPassable( bool value );
            virtual bool isPassable() const;

            virtual void setOnInteractScript( const char * );
            virtual void setOnInteractCode( const char * );
            virtual bool canInteract() const;
            virtual void onInteract();

            /* Should only be used for Persons, but this is needed because of
             * abstracting to Python scripts. Always returns true.
             */
            virtual void freeze( bool );
            virtual bool stepTo( Point );
            virtual void setStandAnimation( bool b=false);
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
