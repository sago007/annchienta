/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "point.h"

#include "mapmanager.h"

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

    PointType Point::getType() const
    {
        return type;
    }

    void Point::to( PointType newtype )
    {
        if( type==newtype )
            return;

        MapManager *mapMgr = getMapManager();
        if( !mapMgr )
            return;

        switch( type )
        {
            case TilePoint:
                switch( newtype )
                {
                    case IsometricPoint:
                        x *= mapMgr->getTileHeight();
                        y *= mapMgr->getTileHeight();
                        break;
                    case MapPoint: default:
                        x = x*mapMgr->getTileWidth()/2 - y*mapMgr->getTileWidth()/2;
                        y = x*mapMgr->getTileHeight()/2 + y*mapMgr->getTileHeight()/2 - z;
                        break;
                    case ScreenPoint:
                        this->to( MapPoint );
                        this->to( ScreenPoint );
                        break;
                }
                break;

            case IsometricPoint: default:
                switch( newtype )
                {
                    case TilePoint:
                        x /= mapMgr->getTileHeight();
                        y /= mapMgr->getTileHeight();
                        break;
                    case MapPoint: default:
                        x = x*2 - y*2;
                        y = x+y - z;
                        break;
                    case ScreenPoint:
                        this->to( MapPoint );
                        this->to( ScreenPoint );
                        break;
                }
                break;

            case MapPoint:
                switch( newtype )
                {
                    case ScreenPoint: default:
                        x -= mapMgr->getCameraX();
                        y -= mapMgr->getCameraY();
                        break;
                }
                break;

            case ScreenPoint:
                switch( newtype )
                {
                    case MapPoint: default:
                        x += mapMgr->getCameraX();
                        y += mapMgr->getCameraY();
                        break;
                }
                break;

        }

        type = newtype;

    }

};
