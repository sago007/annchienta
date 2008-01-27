/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAPMANAGER_H
#define ANNCHIENTA_MAPMANAGER_H

namespace Annchienta
{
    class MapManager
    {
        private:
            int tileWidth, tileHeight;
            int cameraX, cameraY;

        public:
            #ifndef SWIG
                MapManager();
                ~MapManager();
            #endif

            void setTileWidth( int tileWidth );
            int getTileWidth() const;
            void setTileHeight( int tileHeight );
            int getTileHeight() const;

            int getCameraX() const;
            int getCameraY() const;
    };

    MapManager *getMapManager();

};

#endif
