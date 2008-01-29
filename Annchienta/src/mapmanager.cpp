/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "mapmanager.h"
#include "map.h"
#include "inputmanager.h"
#include "videomanager.h"

namespace Annchienta
{
    MapManager *mapManager;

    MapManager::MapManager(): tileWidth(32), tileHeight(16), cameraX(0), cameraY(0), currentMap(0)
    {
        /* Set reference to single-instance class.
         */
        mapManager = this;
    }

    MapManager::~MapManager()
    {
    }

    void MapManager::setTileWidth( int tw )
    {
        tileWidth = tw;
    }

    int MapManager::getTileWidth() const
    {
        return tileWidth;
    }

    void MapManager::setTileHeight( int th )
    {
        tileHeight = th;
    }

    int MapManager::getTileHeight() const
    {
        return tileHeight;
    }

    int MapManager::getCameraX() const
    {
        return cameraX;
    }

    int MapManager::getCameraY() const
    {
        return cameraY;
    }

    void MapManager::setCurrentMap( Map *map )
    {
        currentMap = map;
    }

    void MapManager::run()
    {
        InputManager *inputManager = getInputManager();
        VideoManager *videoManager = getVideoManager();

        while( inputManager->running() )
        {
            inputManager->update();

            renderFrame();
            videoManager->flip();
        }
    }

    void MapManager::renderFrame() const
    {
        if( currentMap )
            currentMap->draw();
    }

    MapManager *getMapManager()
    {
        return mapManager;
    }

};
