/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_ENTITY_H
#define ANNCHIENTA_ENTITY_H

#include <string>

namespace Annchienta
{
    class Entity
    {
        protected:
            bool drawn;
            char name[512];

        public:
            Entity( const char *name="none" );

            virtual void draw() = 0;
            virtual int getDepthSortY() const = 0;

            void setDrawn( bool drawn );
            bool isDrawn() const;

            void setName( const char *name );
            const char *getName() const;

    };
};

#endif
