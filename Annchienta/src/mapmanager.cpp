/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "mapmanager.h"

namespace Annchienta
{
    MapManager *mapManager;

    MapManager::MapManager()
    {
        /* Set reference to single-instance class.
         */
        mapManager = this;
    }

    MapManager::~MapManager()
    {
    }

    MapManager *getMapManager()
    {
        return mapManager;
    }

};
