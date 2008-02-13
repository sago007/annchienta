/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "mapmanager.h"

#include <SDL.h>
#include <GL/gl.h>
#include "map.h"
#include "inputmanager.h"
#include "videomanager.h"
#include "staticobject.h"

namespace Annchienta
{
    MapManager *mapManager;

    long int updatesNeeded = 0;

    /* Timer function. Increments updatesNeeded by the int
     * pointed to by param.
     */
    Uint32 incrementUpdatesNeeded( Uint32 interval, void *param )
    {
        updatesNeeded += 1;
        return interval;
    }

    MapManager::MapManager(): tileWidth(32), tileHeight(16), cameraX(0), cameraY(0), updatesPerSecond(60), currentMap(0), cameraTarget(0), maxAscentHeight(16), maxDescentHeight(32)
    {
        /* Set reference to single-instance class.
         */
        mapManager = this;

        updatesNeeded = updatesPerSecond;
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

    void MapManager::setCameraX( int x )
    {
        cameraX = x;
    }

    int MapManager::getCameraX() const
    {
        return cameraX;
    }

    void MapManager::setCameraY( int y )
    {
        cameraY = y;
    }

    int MapManager::getCameraY() const
    {
        return cameraY;
    }

    void MapManager::cameraFollow( StaticObject *object )
    {
        cameraTarget = object;
    }

    void MapManager::setCurrentMap( Map *map )
    {
        currentMap = map;
    }

    void MapManager::setUpdatesPerSecond( int u )
    {
        updatesPerSecond = u;
    }

    Map *MapManager::getCurrentMap() const
    {
        return currentMap;
    }

    void MapManager::setMaxAscentHeight( int _maxAscentHeight )
    {
        maxAscentHeight = _maxAscentHeight;
    }

    int MapManager::getMaxAscentHeight() const
    {
        return maxAscentHeight;
    }

    void MapManager::setMaxDescentHeight( int _maxDescentHeight )
    {
        maxDescentHeight = _maxDescentHeight;
    }

    int MapManager::getMaxDescentHeight() const
    {
        return maxDescentHeight;
    }

    void MapManager::run()
    {
        InputManager *inputManager = getInputManager();
        VideoManager *videoManager = getVideoManager();

        unsigned int lastFpsUpdate = SDL_GetTicks();
        unsigned int frames = 0;

        SDL_AddTimer( 1000/updatesPerSecond, incrementUpdatesNeeded, 0 );

        while( inputManager->running() )
        {
            while( updatesNeeded>0 )
            {
                inputManager->update();
                this->update();
                updatesNeeded--;
            }

            videoManager->begin();
            renderFrame();
            videoManager->end();

            frames++;
            if( lastFpsUpdate+1000<=SDL_GetTicks() )
            {
                char title[256];
                sprintf( title, "MapManager FPS: %d", frames );
                SDL_WM_SetCaption( title, NULL );

                lastFpsUpdate = SDL_GetTicks();
                frames = 0;
            }
        }
    }

    void MapManager::update()
    {
        if( currentMap )
            currentMap->update();

        if( cameraTarget )
        {
            VideoManager *videoManager = getVideoManager();

            Point targetPosition = cameraTarget->getPosition();
            targetPosition.convert( MapPoint );

            cameraX = targetPosition.x - videoManager->getScreenWidth()/2;
            cameraY = targetPosition.y - videoManager->getScreenHeight()/2;

        }
    }

    void MapManager::renderFrame() const
    {
        glLoadIdentity();

        glTranslatef( -cameraX, -cameraY, 0.0f );

        if( currentMap )
            currentMap->draw();

        glLoadIdentity();
    }

    MapManager *getMapManager()
    {
        return mapManager;
    }

};
