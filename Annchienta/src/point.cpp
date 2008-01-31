/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "point.h"

#include <stdio.h>
#include <math.h>
#include "mapmanager.h"
#include "auxfunc.h"

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

    void Point::to( PointType newtype )
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
                        x *= mapMgr->getTileHeight();
                        y *= mapMgr->getTileHeight();
                        break;
                    case MapPoint: default:
                        nx = x*mapMgr->getTileWidth()/2 - y*mapMgr->getTileWidth()/2;
                        ny = x*mapMgr->getTileHeight()/2 + y*mapMgr->getTileHeight()/2 - z;
                        x = nx;
                        y = ny;
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
                        nx = x*2 - y*2;
                        ny = x+y - z;
                        x = nx;
                        y = ny;
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
                    case TilePoint:
                        this->MapToIsometric();
                        this->to( TilePoint );
                        break;
                    case IsometricPoint:
                        this->MapToIsometric();
                        break;
                    case ScreenPoint: default:
                        x -= mapMgr->getCameraX();
                        y -= mapMgr->getCameraY();
                        break;
                }
                break;

            case ScreenPoint:
                switch( newtype )
                {
                    case TilePoint:
                        this->to( MapPoint );
                        this->to( IsometricPoint );
                        this->to( TilePoint );
                        break;
                    case IsometricPoint:
                        this->to( MapPoint );
                        this->to( IsometricPoint );
                        break;
                    case MapPoint: default:
                        x += mapMgr->getCameraX();
                        y += mapMgr->getCameraY();
                        break;
                }
                break;

        }

        type = newtype;

    }

    void Point::MapToIsometric()
    {
        /* Calculate the distance to the map origin.
         */
        float originDist = distance( 0, 0, x, y );

        /* Calculate the angle to the map point.
         */
        float angle = atan2( (float)y, (float)x );

        /* Subtract iso angle from the angle.
         */
        angle -= 0.4636476f;
        angle /= 1.41f;

        /* Calculate the x and y coordinate
         */
        x = (int) (cos( angle ) * originDist );
        y = (int) (sin( angle ) * originDist );
    }

};
