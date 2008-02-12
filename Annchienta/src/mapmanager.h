/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAPMANAGER_H
#define ANNCHIENTA_MAPMANAGER_H

namespace Annchienta
{
    class Map;
    class StaticObject;

    class MapManager
    {
        private:
            int tileWidth, tileHeight;
            int cameraX, cameraY;
            int updatesPerSecond;
            Map *currentMap;
            StaticObject *cameraTarget;

            int maxAscentHeight, maxDescentHeight;

        public:
            #ifndef SWIG
                MapManager();
                ~MapManager();
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

            void setUpdatesPerSecond( int );

            void setCurrentMap( Map *map );
            Map *getCurrentMap() const;

            void setMaxAscentHeight( int maxAscentHeight );
            int getMaxAscentHeight() const;
            void setMaxDescentHeight( int maxDescentHeight );
            int getMaxDescentHeight() const;

            /* This function should basically run the game.
             */
            void run();

            void update();
            void renderFrame() const;
    };

    MapManager *getMapManager();

};

#endif
