/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "tile.h"

namespace Annchienta
{

    Tile::Tile( Point p1, Surface *s1, Point p2, Surface *s2, Point p3, Surface *s3, Point p4, Surface *s4 )
    {
        points[1] = p1;
        surfaces[1] = s1;
        points[2] = p2;
        surfaces[2] = s2;
        points[3] = p3;
        surfaces[3] = s3;
        points[4] = p4;
        surfaces[4] = s4;
    }

    Tile::~Tile()
    {
    }

};
