/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_TILE_H
#define ANNCHIENTA_TILE_H

#include <GL/gl.h>
#include "point.h"
#include "entity.h"

namespace Annchienta
{

    class Surface;

    class Tile: public Entity
    {
        private:
            Point points[4];
            Surface *surfaces[4];
            GLuint list;

            void getTexCoords( Surface*, float *xCenter, float *topYCenter, float *topYDown, float *wallYDown ) const;
            void makeList();

        public:
            Tile( Point, Surface*, Point, Surface*, Point, Surface*, Point, Surface* );
            ~Tile();

            virtual void draw() const;
            virtual int getDepthSortY() const;

    };
};

#endif
