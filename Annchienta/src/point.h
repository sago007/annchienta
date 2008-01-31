/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_POINT_H
#define ANNCHIENTA_POINT_H

namespace Annchienta
{
    enum PointType
    {
        TilePoint=0,
        IsometricPoint,
        MapPoint,
        ScreenPoint
    };

    class Point
    {
        private:
            PointType type;

        public:
            int x, y, z;

            Point( PointType type=TilePoint, int x=0, int y=0, int z=0 );
            Point( const Point &other );
            ~Point();

            #ifndef SWIG /* Gets ignored anyway. */
                Point &operator=(const Point &other);
                void setType( PointType type );
            #endif

            PointType getType() const;
            void to( PointType newtype );
            /* Kind of complicated, so gets a seperate one. */
            void MapToIsometric();

    };

};

#endif
