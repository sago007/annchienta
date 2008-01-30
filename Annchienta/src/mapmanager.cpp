/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "mapmanager.h"

#include <SDL.h>
#include <GL/gl.h>
#include "map.h"
#include "inputmanager.h"
#include "videomanager.h"

namespace Annchienta
{
    MapManager *mapManager;

    MapManager::MapManager(): tileWidth(32), tileHeight(16), cameraX(-150), cameraY(120), currentMap(0)
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

        unsigned int lastFpsUpdate = SDL_GetTicks();
        unsigned int frames = 0;

        while( inputManager->running() )
        {

            inputManager->update();

            renderFrame();
            videoManager->flip();

            frames++;
            if( lastFpsUpdate+1000<=SDL_GetTicks() )
            {
                char title[256];
                sprintf( title, "Annchienta FPS: %d", frames );
                SDL_WM_SetCaption( title, NULL );

                lastFpsUpdate = SDL_GetTicks();
                frames = 0;
            }
        }
    }

    void MapManager::renderFrame() const
    {
        glLoadIdentity();
        glTranslatef( -cameraX, -cameraY, 0.0f );

        if( currentMap )
            currentMap->draw();
    }

    MapManager *getMapManager()
    {
        return mapManager;
    }

};
