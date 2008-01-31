/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "editor.h"

#include "inputmanager.h"
#include "videomanager.h"
#include "mapmanager.h"
#include "map.h"
#include "tile.h"
#include "font.h"
#include "surface.h"
#include "point.h"
#include "layer.h"
#include "auxfunc.h"

namespace Annchienta
{

    Editor::Editor( const char *fname ): selectWholeTiles( true )
    {
        sprintf( filename, fname );

        inputManager = getInputManager();
        videoManager = getVideoManager();
        mapManager = getMapManager();

        videoManager->setVideoMode( 800, 600, "Annchienta Map Editor" );

        Map *map = new Map( filename );
        mapManager->setCurrentMap( map );

        inputManager->update();
        prevMouseX = inputManager->getMouseX();
        prevMouseY = inputManager->getMouseY();

        font = new Font("editor/font.ttf", 16);
    }

    Editor::~Editor()
    {
        delete font;
    }

    void Editor::run()
    {
        while( inputManager->running() )
        {
            input();
            draw();
        }
    }

    void Editor::input()
    {
        inputManager->update();

        if( inputManager->buttonTicked(0) )
        {
            getSelectedPoints();
            printf("Selected points...\n");
            applyActions();
            printf("Took actions...\n");
        }

        /* Scroll if right mouse button is pressed.
         */
        if( inputManager->buttonDown(1) )
        {
            int cx = mapManager->getCameraX(), cy = mapManager->getCameraY();
            cx += ( prevMouseX - inputManager->getMouseX() );
            cy += ( prevMouseY - inputManager->getMouseY() );
            mapManager->setCameraX( cx );
            mapManager->setCameraY( cy );
        }

        prevMouseX = inputManager->getMouseX();
        prevMouseY = inputManager->getMouseY();
    }

    void Editor::draw()
    {

        mapManager->renderFrame();

        videoManager->setColor( 220, 220, 220 );
        videoManager->drawRectangle( 0, 0, 800, 20 );
        videoManager->setColor( 180, 180, 180 );
        videoManager->drawRectangle( 600, 20, 800, 600 );

        videoManager->setColor( 0, 0, 0 );

        if( selectWholeTiles )
            videoManager->drawString( font, "Select whole tiles.", 2, 2 );
        else
            videoManager->drawString( font, "Select points.", 2, 2 );

        videoManager->flip();

    }

    void Editor::getSelectedPoints()
    {
        Tile **tiles = mapManager->getCurrentMap()->getCurrentLayer()->tiles;
        int w = mapManager->getCurrentMap()->getCurrentLayer()->width,
            h = mapManager->getCurrentMap()->getCurrentLayer()->height;

        Point mousePoint( ScreenPoint, inputManager->getMouseX(), inputManager->getMouseY() );
        mousePoint.to( MapPoint );

        float smallest = 8000.0f;
        Tile *tile;

        for( int i=0; i<w*h; i++ )
        {
            float dist = squaredDistance( mousePoint.x, mousePoint.y, tiles[i]->points[0].x, tiles[i]->points[0].y + tiles[i]->points[0].z );
            if( smallest > dist )
            {
                smallest = dist;
                tile = tiles[i];
            }
        }

        for( int i=0; i<4; i++ )
        {
            selectedPoints.push_back( &tile->points[i] );
            selectedPointSurfaces.push_back( &tile->surfaces[i] );
        }

        affectedTiles.push_back( tile );

    }

    void Editor::applyActions()
    {

        for( std::list<Point*>::iterator it = selectedPoints.begin(); it!=selectedPoints.end(); it++ )
        {
            (*it)->z += 10;
            (*it)->y -= 10;
        }

        selectedPoints.clear();

        selectedPointSurfaces.clear();

        for( std::list<Tile*>::iterator it = affectedTiles.begin(); it!= affectedTiles.end(); it++ )
            (*it)->makeList();

        affectedTiles.clear();

        mapManager->getCurrentMap()->depthSort();
    }

};
