/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_ENTITY_H
#define ANNCHIENTA_ENTITY_H

#include "Point.h"
#include "Engine.h"

namespace Annchienta
{
    class Layer;

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

            /** Use this when you want to know where you should
             *  place the Mask for this Entity if you want to
             *  check collision with other Entities.
             *  \return A Point describing where the Mask should be placed.
             */
            virtual Point getMaskPosition() const = 0;

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
