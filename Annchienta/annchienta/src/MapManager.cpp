/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "MapManager.h"

#include <SDL.h>
#include <SDL_opengl.h>
#include <Python.h>
#include "InputManager.h"
#include "VideoManager.h"
#include "LogManager.h"
#include "Map.h"
#include "StaticObject.h"
#include "Mask.h"
#include "Layer.h"
#include "Engine.h"
#include "Vector.h"

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
                              onUpdateScript(0), onUpdateCode(0), m_running(false)
    {
        /* Set reference to single-instance class.
         */
        mapManager = this;

        updatesNeeded = updatesPerSecond;

        getLogManager()->message("Succesfully started MapManager.");
    }

    MapManager::~MapManager()
    {
        getLogManager()->message("Deleting MapManager...");

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

    StaticObject *MapManager::getCameraFollow() const
    {
        return cameraTarget;
    }

    void MapManager::cameraPeekAt( StaticObject *object, bool instantly )
    {
        VideoManager *videoManager = getVideoManager();

        Point targetPosition = object->getPosition();
        targetPosition.convert( MapPoint );

        /* Calculate destX and destY so that they represent the destination
         * camera coordinates. */
        int destX = targetPosition.x - videoManager->getScreenWidth()/2;
        int destY = targetPosition.y - targetPosition.z - object->getMask()->getHeight()/2 - videoManager->getScreenHeight()/2;

        /* Avoid segfaults: make sure this is a layer before we subtract
         * the Z offset from it... */
        if( object->getLayer() )
            destY -= object->getLayer()->getZ();

        /* If we're instantly looking at the target, just put our
         * camera over there. */
        if( instantly )
        {
            cameraX = destX;
            cameraY = destY;
        }
        /* If this is not the case, move our camera there a little. */
        else
        {
            Vector deltaVector( destX - cameraX, destY - cameraY );

            /* Only perform our move if we are moving properly, because
             * we don't want a 'jumpy' camera. */
            if( deltaVector.lengthSquared()>2 )
            {
                deltaVector.cap( -4.0, 4.0 );
                cameraX += (int)(deltaVector.x+0.5f);
                cameraY += (int)(deltaVector.y+0.5f);
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
        m_running = true;

        VideoManager *videoManager = getVideoManager();
        inputManager = getInputManager();

        /* unsigned int lastFpsUpdate = SDL_GetTicks();
         * unsigned int frames = 0;
         */

        SDL_TimerID timer = SDL_AddTimer( 1000/updatesPerSecond, incrementUpdatesNeeded, 0 );

        while( inputManager->running() && m_running )
        {
            this->update();

            if( m_running )
            {
                videoManager->begin();
                this->draw();
                videoManager->end();
            }

            /* frames++;
             * if( lastFpsUpdate+1000<=SDL_GetTicks() )
             * {
             *     char title[256];
             *     sprintf( title, "Annchienta FPS: %d", frames );
             *     SDL_WM_SetCaption( title, NULL );
             *
             *     lastFpsUpdate = SDL_GetTicks();
             *     frames = 0;
             * }
             */
        }

        SDL_RemoveTimer( timer );
    }

    bool MapManager::running() const
    {
        return m_running && inputManager->running();
    }

    void MapManager::stop()
    {
        m_running = false;
    }

    void MapManager::update( bool updateInput )
    {
        //printf("Updating %d times...\n", updatesNeeded );
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
            cameraPeekAt( cameraTarget, false );
        }

        if( onUpdateCode )
            getEngine()->runPythonCode( onUpdateCode );
        if( onUpdateScript )
            getEngine()->runPythonScript( onUpdateScript );
    }

    void MapManager::draw() const
    {
        this->renderFrame();
    }

    void MapManager::renderFrame() const
    {
        VideoManager *videoManager = getVideoManager();
        videoManager->pushMatrix();

        videoManager->translate( -cameraX, -cameraY );

        if( currentMap )
            currentMap->draw();

        videoManager->popMatrix();
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
