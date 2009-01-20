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

    /** A StaticObject is an Entity in the Map that
     *  has a sprite, animations, a position...
     *  but it cannot move. Use a Person for that.
     */
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

            char *onInteractScript, *onInteractCode;

            char xmlFile[DEFAULT_STRING_SIZE];

        public:

            /** Create a new StaticObject.
             *  \param name Name for this StaticObject.
             *  \param configfile XML File where animations, sprite etc. should be loaded from.
             */
            StaticObject( const char *name, const char *configfile );

            /** Create a new StaticObject without a config file.
             *  This is used to create simple objects which do not
             *  have animations.
             *  \param name Name for this StaticObject.
             *  \param surf Sprite for this StaticObject.
             *  \param mask Collision mask for this StaticObject.
             */
            StaticObject( const char *name, Surface *surf, Mask *mask );
            virtual ~StaticObject();

            /** This function calculates which tiles the StaticObject
             *  is colliding with and stores them internally.
             *  \warning This function should only be used internally.
             */
            void calculateCollidingTiles();

            /** This function calculates the current Z coordinate
             *  of this StaticObject and returns it.
             *  \warning This function should only be used internally.
             *  \return The new Z coordinate.
             */
            float getZFromCollidingTiles();

            /** \return The EntityType of this StaticObject.
             */
            virtual EntityType getEntityType() const;

            /** Updates this Entity. This is called when updating the Map
             *  this Entity is in.
             */
            virtual void update();

            /** Draws this StaticObject to the screen.
             */
            virtual void draw();

            /** \return The depth this StaticObject should be sorted on.
             */
            virtual int getDepth();

            /** \return The Mask for this StaticObject.
             */
            virtual Mask *getMask() const;

            /** Sets the position for this StaticObject.
             *  \param position The new position.
             */
            virtual void setPosition( Point position );

            /** \return The position of this StaticObject.
             */
            virtual Point getPosition() const;

            /** \return The position where the Mask of this StaticObject should be placed to calculate collisions.
             */
            virtual Point getMaskPosition() const;

            /** \return The XML file this StaticObject was loaded from, otherwise 0.
             */
            const char *getXmlFile() const;

            /** Should be used with care, because the frame settings
             *  stay the same. 
             *  \warning Make sure the new sprite has the same dimensions and frames.
             *  \param filename Filename of the new sprite.
             */
            virtual void setSprite( const char *filename );

            /** \return The current sprite used.
             */
            Surface *getSprite() const;

            /** Set the animation for this StaticObject. Animations
             *  should be declared in it's XML file.
             *  \param animationName Name of the to be set animation.
             *  \return If the animation set was succesful.
             */
            bool setAnimation( const char *animationName );

            /** Get the name of the currently playing animation.
             *  \return The name of the currently playing animation.
             */
            const char *getAnimation() const;

            /** If this object is passable, other objects can
             *  "walk through" it.
             *  \param passable If this object should be passable.
             */
            virtual void setPassable( bool passable );

            /** If this object is passable, other objects can
             *  "walk through" it.
             *  \return If this object is passable.
             */
            virtual bool isPassable() const;

            /** Sets this object's interact script. This script
             *  will be executed when the object is interacted with.
             *  \param script Filename of the script.
             */
            virtual void setOnInteractScript( const char *script );

            /** Sets this object's interact code. This code
             *  will be executed when the object is interacted with.
             *  \param code Code to be executed.
             */
            virtual void setOnInteractCode( const char *code );

            /** \return If this object has an interact script or interact code.
             */
            virtual bool canInteract() const;

            /** When you call this function, this object's interact
             *  script and/or code will be executed if they exist.
             */
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

    /** A function for use in scenes. When you call this
     *  function, it will return the object that most recently
     *  started interacting with another object.
     *  \return The object that started interacting.
     */
    StaticObject *getActiveObject();

    /** A function for use in scenes. When you call this
     *  function, it will return the object that most recently
     *  started being interacting with.
     *  \return The object that started being interacting with.
     */
    StaticObject *getPassiveObject();
};

#endif
