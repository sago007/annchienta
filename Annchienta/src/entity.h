/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_ENTITY_H
#define ANNCHIENTA_ENTITY_H

namespace Annchienta
{
    class Entity
    {
        private:

        public:
            virtual void draw() const = 0;
            virtual int getDepthSortY() const = 0;

    };
};

#endif
