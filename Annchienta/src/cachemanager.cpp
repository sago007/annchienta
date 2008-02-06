/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "cachemanager.h"

#include "surface.h"

namespace Annchienta
{
    CacheManager *cacheManager;

    CacheManager::CacheManager()
    {
        /* Set reference to single-instance class.
         */
        cacheManager = this;

    }

    CacheManager::~CacheManager()
    {
        this->clear();
    }

    Surface *CacheManager::getSurface( const char *filename )
    {
        for( std::list< CacheObject<Surface> >::iterator i = surfaces.begin(); i!=surfaces.end(); i++ )
        {
            if( !strcmp( filename, (*i).name ) )
            {
                return (*i).data;
            }
        }

        Surface *surface = new Surface( filename );
        surfaces.push_back( CacheObject<Surface>( filename, surface ) );
        return surface;
    }

    void CacheManager::clear()
    {
        for( std::list< CacheObject<Surface> >::iterator i = surfaces.begin(); i!=surfaces.end(); i++ )
        {
            delete (*i).data;
        }

        surfaces.clear();

    }

    CacheManager *getCacheManager()
    {
        return cacheManager;
    }

};
