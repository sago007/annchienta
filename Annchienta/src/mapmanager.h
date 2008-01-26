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

        public:
            #ifndef SWIG
                MapManager();
                ~MapManager();
            #endif

    };

    MapManager *getMapManager();

};

#endif
