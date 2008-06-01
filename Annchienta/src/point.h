/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_POINT_H
#define ANNCHIENTA_POINT_H

namespace Annchienta
{
    /** These enums are used for indicating types of Points we
     *  can be dealing with.
     */
    enum PointType
    {
        /** A Point defined by an x, y (and z) coordinate. The x and
         *  y coordinates indicate which tile this point is situated
         *  on. The most northern point of the Map is considered to
         *  be (0,0).
         *  \image html point_tilepoints.png
         */
        TilePoint=0,

        /** A Point defined by an x, y (and z) coordinate. The x and
         *  y coordinates indicate a point in an isometric axis system.
         *  The most northern point of the Map is considered to be (0,0)
         *  \image html point_isometricpoints.png
         */
        IsometricPoint,

        /** A Point defined by an x, y (and z) coordinate. The x and
         *  y coordinates indicate a point in an orthogonal axis system
         *  where the most northern point of the Map is (0,0).
         *  \image html point_mappoints.png
         */
        MapPoint,

        /** A Point defined by an x and y coordinate. This indicates
         *  a point on the screen. The top-left corner of the window
         *  is considered (0,0).
         *  \image html point_screenpoints.png
         */
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
            //void to( PointType newtype );
            void convert( PointType newtype );
            Point to( PointType newtype ) const;

            bool isEnclosedBy( Point *leftTop, Point *rightBottom );
            int distance( Point other ) const;

    };

};

#endif
