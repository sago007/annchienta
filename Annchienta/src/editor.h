/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_EDITOR_H
#define ANNCHIENTA_EDITOR_H

#include <list>

namespace Annchienta
{

    class InputManager;
    class VideoManager;
    class MapManager;
    class Tile;
    class Font;
    class Surface;
    class Point;

    class Editor
    {
        private:
            InputManager *inputManager;
            VideoManager *videoManager;
            MapManager *mapManager;
            Font *font;
            char filename[256];

            int prevMouseX, prevMouseY;
            bool selectWholeTiles;

            std::list<Point*> selectedPoints;
            std::list<Surface**> selectedPointSurfaces;
            std::list<Tile*> affectedTiles;

        public:
            Editor( const char *map=0, int tw=64, int th=32, int w=20, int h=20, const char *tileset=0 );
            ~Editor();

            void run();

            #ifndef SWIG
                void input();
                void draw();

                void getSelectedPoints();
                void applyActions();
            #endif

    };
};

#endif
