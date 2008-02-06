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
                (*i).references++;
                return (*i).data;
            }
        }

        Surface *surface = new Surface( filename );
        surfaces.push_back( CacheObject<Surface>( filename, surface ) );
        return surface;
    }

    void CacheManager::deleteSurface( Surface *surface )
    {
        for( std::list< CacheObject<Surface> >::iterator i = surfaces.begin(); i!=surfaces.end(); i++ )
        {
            if( surface == (*i).data )
            {
                (*i).references--;
                if( (*i).references <= 0 )
                {
                    delete (*i).data;
                    surfaces.erase( i );
                }
                return;
            }
        }
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
