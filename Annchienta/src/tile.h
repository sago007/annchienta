/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_TILE_H
#define ANNCHIENTA_TILE_H

#include <GL/gl.h>
#include "point.h"
#include "entity.h"
#include "editor.h"

namespace Annchienta
{

    class Surface;

    class Tile: public Entity
    {
        friend class Editor;

        private:
            Point points[4];
            Point isoPoints[4];
            Surface *surfaces[4];
            GLuint list;

            bool nullTile;

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
