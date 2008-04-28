/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAPMANAGER_H
#define ANNCHIENTA_MAPMANAGER_H

namespace Annchienta
{
    class Map;
    class StaticObject;
    class InputManager;
    class Person;

    class MapManager
    {
        private:
            InputManager *inputManager;

            int tileWidth, tileHeight;
            int cameraX, cameraY;
            int updatesPerSecond;
            Map *currentMap;
            StaticObject *cameraTarget;

            int maxAscentHeight, maxDescentHeight;

            char *onUpdateScript, *onUpdateCode;

            bool running;

        public:
            #ifndef SWIG
                MapManager();
                ~MapManager();

                int getUpdatesNeeded() const;
            #endif

            void setTileWidth( int tileWidth );
            int getTileWidth() const;
            void setTileHeight( int tileHeight );
            int getTileHeight() const;

            void setCameraX( int );
            int getCameraX() const;
            void setCameraY( int );
            int getCameraY() const;

            void cameraFollow( StaticObject *object );
            void cameraPeekAt( StaticObject *object, bool instantly=false );

            void setUpdatesPerSecond( int );

            void setCurrentMap( Map *map );
            void setNullMap();
            Map *getCurrentMap() const;

            void setMaxAscentHeight( int maxAscentHeight );
            int getMaxAscentHeight() const;
            void setMaxDescentHeight( int maxDescentHeight );
            int getMaxDescentHeight() const;

            StaticObject *getObject( const char *name );

            void setOnUpdateScript( const char * );
            void setOnUpdateCode( const char * );

            /* This function should basically run the game.
             */
            void run();
            void stop();

            void update( bool updateInput=true );
            void updateOnce( bool updateInput=true );

            void renderFrame() const;
            void renderTerrain() const;

            void resync();
    };

    MapManager *getMapManager();

};

#endif
