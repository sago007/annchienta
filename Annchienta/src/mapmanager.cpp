/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "mapmanager.h"

#include <SDL.h>
#include <GL/gl.h>
#include <Python.h>
#include "map.h"
#include "inputmanager.h"
#include "videomanager.h"
#include "staticobject.h"
#include "mask.h"
#include "layer.h"
#include "auxfunc.h"
#include "engine.h"

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

    MapManager::MapManager(): tileWidth(32), tileHeight(16), cameraX(0), cameraY(0),
                              updatesPerSecond(60), currentMap(0), cameraTarget(0),
                              maxAscentHeight(16), maxDescentHeight(32),
                              onUpdateScript(0), onUpdateCode(0)
    {
        /* Set reference to single-instance class.
         */
        mapManager = this;

        updatesNeeded = updatesPerSecond;
    }

    MapManager::~MapManager()
    {
        if( onUpdateScript )
            delete[] onUpdateScript;
        if( onUpdateCode )
            delete[] onUpdateCode;
    }

    int MapManager::getUpdatesNeeded() const
    {
        return updatesNeeded;
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

    void MapManager::cameraPeekAt( StaticObject *object, bool instantly )
    {
        VideoManager *videoManager = getVideoManager();

        Point targetPosition = object->getPosition();
        targetPosition.convert( MapPoint );

        int destX = targetPosition.x - videoManager->getScreenWidth()/2;
        int destY = targetPosition.y - targetPosition.z - object->getMask()->getHeight()/2 - videoManager->getScreenHeight()/2 - object->getLayer()->getZ();

        if( instantly )
        {
            cameraX = destX;
            cameraY = destY;
        }
        else
        {
            int s = 4;
            while( squaredDistance( cameraX, cameraY, destX, destY )>2500 && --s )
            {
                cameraX += sign( destX - cameraX );
                cameraY += sign( destY - cameraY );
            }
        }
    }

    void MapManager::setUpdatesPerSecond( int u )
    {
        updatesPerSecond = u;
    }

    void MapManager::setCurrentMap( Map *map )
    {
        currentMap = map;
    }

    void MapManager::setNullMap()
    {
        currentMap = 0;
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

    StaticObject *MapManager::getObject( const char *name )
    {
        if( currentMap )
            return currentMap->getObject( name );
        return 0;
    }

    void MapManager::setOnUpdateScript( const char *script )
    {
        if( onUpdateScript )
            delete[] onUpdateScript;

        onUpdateScript = new char[strlen(script)+1];
        strcpy( onUpdateScript, script );
    }

    void MapManager::setOnUpdateCode( const char *code )
    {
        if( onUpdateCode )
            delete[] onUpdateCode;

        onUpdateCode = new char[strlen(code)+1];
        strcpy( onUpdateCode, code );
    }

    void MapManager::run()
    {
        running = true;

        VideoManager *videoManager = getVideoManager();
        inputManager = getInputManager();

        unsigned int lastFpsUpdate = SDL_GetTicks();
        unsigned int frames = 0;

        SDL_TimerID timer = SDL_AddTimer( 1000/updatesPerSecond, incrementUpdatesNeeded, 0 );

        while( inputManager->running() && running )
        {
            this->update();

            if( running )
            {
                videoManager->begin();
                this->renderFrame();
                videoManager->end();
            }

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

        SDL_RemoveTimer( timer );
    }

    void MapManager::stop()
    {
        running = false;
    }

    void MapManager::update( bool updateInput )
    {
        while( updatesNeeded>0 )
        {
            this->updateOnce( updateInput );
            updatesNeeded--;
        }
    }

    void MapManager::updateOnce( bool updateInput )
    {
        if( updateInput )
            inputManager->update();

        if( currentMap )
            currentMap->update();

        if( cameraTarget )
        {
            cameraPeekAt( cameraTarget );
        }

        if( onUpdateCode )
            PyRun_SimpleString( onUpdateCode );
        if( onUpdateScript )
            getEngine()->runPythonScript( onUpdateScript );
    }

    void MapManager::renderFrame() const
    {
        glLoadIdentity();

        glTranslatef( -cameraX, -cameraY, 0.0f );

        if( currentMap )
            currentMap->draw();

        glLoadIdentity();
    }

    void MapManager::renderTerrain() const
    {
        glLoadIdentity();

        glTranslatef( -cameraX, -cameraY, 0.0f );

        if( currentMap )
            currentMap->drawTerrain();

        glLoadIdentity();
    }

    void MapManager::resync()
    {
        updatesNeeded = 0;
    }

    MapManager *getMapManager()
    {
        return mapManager;
    }

};
