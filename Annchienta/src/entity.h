/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_ENTITY_H
#define ANNCHIENTA_ENTITY_H

#include "point.h"

namespace Annchienta
{
    class Layer;

    class Entity
    {
        protected:
            bool drawn;
            char name[512];
            Layer *layer;

        public:
            Entity( const char *name="none" );
            virtual ~Entity();

            virtual void draw() = 0;
            virtual void update() = 0;
            virtual int getDepthSortY() const = 0;
            virtual Point getMaskPosition() const = 0;

            void setDrawn( bool drawn );
            bool isDrawn() const;

            void setName( const char *name );
            const char *getName() const;

            void setLayer( Layer *layer );
            Layer *getLayer() const;
    };

};

#endif
