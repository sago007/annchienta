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
            Surface *sideSurface;
            GLuint list;

            bool nullTile;

            void makeList();

        public:
            Tile( Point, Surface*, Point, Surface*, Point, Surface*, Point, Surface*, Surface *side=0 );
            ~Tile();

            virtual void update();
            virtual void draw();
            virtual int getDepthSortY();
            bool hasPoint( Point point ) const;

            #ifndef SWIG
                virtual Point getMaskPosition() const;
                int getZ( int point ) const;
                Point getPoint( int i ) const;
            #endif

    };
};

#endif
