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

    /** \brief Holds a Point.
     *
     *  This class is used for holding Points. You can
     *  manipulate the coordinates directly.
     *
     *  \section point_example1 Example:
     *  \code
     * import annchienta
     * point = annchienta.Point( annchienta.TilePoint, 2, 2 )
     * point.x = point.y = point.z = 0
     *  \endcode
     *
     *  Their are different types of point, I therefore
     *  recommend you read the \ref PointType documentation.
     *
     *  Converting between types is easy, just use the to() and
     *  convert() functions.
     *
     *  \section point_example2 Example:
     *  \code
     * import annchienta
     * videoManager = annchienta.getVideoManager()
     * point = annchienta.Point( annchienta.TilePoint, 2, 2 )
     * point.convert( ScreenPoint )
     * videoManager.drawLine( point.x, point.y, 0, 0 )
     *  \endcode
     */
    class Point
    {
        private:
            PointType type;

        public:
            int x, y, z;

            /** Creates a new Point with the given coordinates.
             *  The Z coordinate is not used most of the time.
             *  For more information, see \ref PointType
             */
            Point( PointType type=TilePoint, int x=0, int y=0, int z=0 );

            /** A copy constructor that creates a new Point
             *  based on a Point that already exists.
             */
            Point( const Point &other );

            ~Point();

            #ifndef SWIG
                /** \note Not available in Python.
                 */
                Point &operator=(const Point &other);

                /** \note Not available in Python.
                 */
                void setType( PointType type );
            #endif

            /** \return The \ref PointType for this Point.
             */
            PointType getType() const;

            /** This function converts this Point to a Point
             *  of another type.
             */
            void convert( PointType newtype );

            /** This function is similar to the convert function,
             *  but this one will make no changes to this Point,
             *  returning a new Point instead.
             */
            Point to( PointType newtype ) const;

            /** Returns True if this Point lies in the rectangular
             *  area defined by leftTop and rightBottom.
             */
            bool isEnclosedBy( Point *leftTop, Point *rightBottom );

            /** Returns the distance to another Point.
             */
            int distance( Point other ) const;

    };

};

#endif
