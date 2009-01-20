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

#ifndef ANNCHIENTA_ENTITY_H
#define ANNCHIENTA_ENTITY_H

#include "Point.h"
#include "Engine.h"

namespace Annchienta
{
    class Layer;
    class Mask;

    enum EntityType
    {
        TileEntity = 0,
        StaticObjectEntity,
        PersonEntity
    };

    /** This represents an entity in the Map. This can
     *  be about anything, a Tile, a StaticObject,
     *  a Person...
     */
    class Entity
    {
        protected:
            bool drawn;
            char name[DEFAULT_STRING_SIZE];
            Layer *layer;

        public:

            /** Creates a new entity.
             *  \param name Give the entity a name.
             */
            Entity( const char *name="none" );
            virtual ~Entity();

            /** Get the type of this Entity.
             *  \return The type of this entity.
             */
            virtual EntityType getEntityType() const = 0;

            /** Draws the entity to the screen.
             */
            virtual void draw() = 0;

            /** Updates the entity, eg. update sprite, position, ...
             */
            virtual void update() = 0;

            /** \return Depth to be used for depthsorting.
             */
            virtual int getDepth() = 0;

            /** \return The collision mask for this entity.
             */
            virtual Mask *getMask() const = 0;

            /** Use this when you want to know where you should
             *  place the Mask for this Entity if you want to
             *  check collision with other Entities.
             *  \return A Point describing where the Mask should be placed.
             */
            virtual Point getMaskPosition() const = 0;

            /** Check if this Entity collides with another Entity.
             *  \return If they collide.
             */
            virtual bool collidesWith( Entity *other ) const;

            /** This is used to keep track of which Entities have
             *  been drawn already this frame and which aren't.
             *  \param drawn Set this to true before drawing if you don't want this to be drawn.
             */
            void setDrawn( bool drawn );

            /** \return Is this Entity already drawn this frame?
             */
            bool isDrawn() const;
  
            /** \param name New name for the Entity.
             */
            void setName( const char *name );

            /** \return The name of this entity.
             */
            const char *getName() const;

            /** Sets the layer to which this Entity belongs.
             *  This is automatically done when using Layer::addObject,
             *  please us that instead.
             *  \param layer Layer to which this Entity should be added.
             */
            void setLayer( Layer *layer );

            /** \return The layer to which this entity belongs.
             */
            Layer *getLayer() const;
    };

};

#endif
