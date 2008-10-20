/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "Point.h"

#include <cmath>
#include "MapManager.h"
#include "GeneralFunctions.h"

namespace Annchienta
{

    Point::Point( PointType _type, int _x, int _y, int _z ): type(_type), x(_x), y(_y), z(_z)
    {
    }

    Point::Point( const Point &o ): type( o.type ), x( o.x ), y( o.y ), z (o.z )
    {
    }

    Point::~Point()
    {
    }

    Point &Point::operator=( const Point &other )
    {
        type = other.type;
        x = other.x;
        y = other.y;
        z = other.z;
        return *this;
    }

    void Point::setType( PointType _type )
    {
        type = _type;
    }

    PointType Point::getType() const
    {
        return type;
    }

    void Point::convert( PointType newtype )
    {
        if( type==newtype )
            return;

        MapManager *mapMgr = getMapManager();
        if( !mapMgr )
            return;

        int nx, ny;

        switch( type )
        {
            case TilePoint:
                switch( newtype )
                {
                    case IsometricPoint:
                        x *= (mapMgr->getTileHeight()>>1);
                        y *= (mapMgr->getTileHeight()>>1);
                        break;
                    case MapPoint: default:
                        nx = x*mapMgr->getTileWidth()/2 - y*mapMgr->getTileWidth()/2;
                        ny = x*mapMgr->getTileHeight()/2 + y*mapMgr->getTileHeight()/2;
                        x = nx;
                        y = ny;
                        break;
                    case ScreenPoint:
                        this->convert( MapPoint );
                        this->convert( ScreenPoint );
                        break;
                }
                break;

            case IsometricPoint: default:
                switch( newtype )
                {
                    case TilePoint:
                        x /= (mapMgr->getTileHeight()>>1);
                        y /= (mapMgr->getTileHeight()>>1);
                        break;
                    case MapPoint: default:
                        nx = x*2 - y*2;
                        ny = x+y;
                        x = nx;
                        y = ny;
                        break;
                    case ScreenPoint:
                        this->convert( MapPoint );
                        this->convert( ScreenPoint );
                        break;
                }
                break;

            case MapPoint:
                switch( newtype )
                {
                    case TilePoint:
                        this->convert( IsometricPoint );
                        this->convert( TilePoint );
                        break;
                    case IsometricPoint:
                        nx = y/2 + x/4;
                        ny = y/2 - x/4;
                        x = nx;
                        y = ny;
                        break;
                    case ScreenPoint: default:
                        x -= mapMgr->getCameraX();
                        y -= (mapMgr->getCameraY()+z);
                        break;
                }
                break;

            case ScreenPoint:
                switch( newtype )
                {
                    case TilePoint:
                        this->convert( MapPoint );
                        this->convert( IsometricPoint );
                        this->convert( TilePoint );
                        break;
                    case IsometricPoint:
                        this->convert( MapPoint );
                        this->convert( IsometricPoint );
                        break;
                    case MapPoint: default:
                        x += mapMgr->getCameraX();
                        y += mapMgr->getCameraY()+z;
                        break;
                }
                break;

        }

        type = newtype;

    }

    Point Point::to( PointType newtype ) const
    {
        Point temp( *this );
        temp.convert( newtype );
        return temp;
    }

    bool Point::isEnclosedBy( Point *leftTopp, Point *rightBottomp )
    {
        Point leftTop = leftTopp->to(type),
              rightBottom = rightBottomp->to(type);
        return ( leftTop.x<=x && leftTop.y<=y && rightBottom.x>=x && rightBottom.y>=y );
    }

    int Point::distance( Point other ) const
    {
        Point tmp = other.to( type );
        return (int) sqrt( double(square(x-tmp.x) + square(y-tmp.y) + square(z-tmp.z)) );
    }

};
