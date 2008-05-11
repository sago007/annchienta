/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_ENTITY_H
#define ANNCHIENTA_ENTITY_H

#include "point.h"

namespace Annchienta
{
    class Layer;

    enum EntityType
    {
        TileEntity = 0,
        StaticObjectEntity,
        PersonEntity
    };

    class Entity
    {
        protected:
            bool drawn;
            char name[512];
            Layer *layer;

        public:

            /** Creates a new entity.
             *  \param name Give the entity a name.
             */
            Entity( const char *name="none" );
            virtual ~Entity();

            /** To find out which type of Entity this is.
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

            /** \return A Point describing where the Mask should be placed.
             */
            virtual Point getMaskPosition() const = 0;

            /** \param drawn Set this to true before drawing if you don't want this to be drawn.
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
