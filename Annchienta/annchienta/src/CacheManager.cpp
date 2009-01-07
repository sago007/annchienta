/*  This file is part of Annchienta.
 *  Copyright 2008 (C) Jasper Van der Jeugt
 *
 *  Annchienta is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Annchienta is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 * 
 *  You should have received a copy of the GNU General Public License
 *  along with Annchienta.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "CacheManager.h"

#include "Cacheable.h"
#include "Surface.h"
#include "Mask.h"
#include "Sound.h"
#include "LogManager.h"

namespace Annchienta
{
    CacheManager *cacheManager;

    CacheManager::CacheManager()
    {
        /* Set reference to single-instance class.
         */
        cacheManager = this;

        getLogManager()->message("Succesfully started CacheManager.");
    }

    CacheManager::~CacheManager()
    {
        getLogManager()->message("Deleting CacheManager...");
        this->clear();
    }

    Cacheable *CacheManager::getCacheable( const char *fileName, CacheableType cacheableType )
    {
        /* Check to see if it is in the list. */
        for( std::list< Cacheable* >:: iterator i = cacheables.begin(); i!=cacheables.end(); i++ )
        {
            if( (*i)->getCacheableType() == cacheableType )
            {
                if( !strcmp( (*i)->getFileName(), fileName ) )
                {
                    return (*i);
                }
            }
        }

        /* Load it. */
        Cacheable *cacheable;
        switch( cacheableType )
        {
            case SurfaceCacheable:
                cacheable = new Surface( fileName );
                break;
            case MaskCacheable:
                cacheable = new Mask( fileName );
                break;
            case SoundCacheable:
                cacheable = new Sound( fileName );
                break;
            case UnknownCacheable: default:
                cacheable = new Cacheable( fileName );
                break;
        }
        cacheables.push_back( cacheable );
        return cacheable;
    }

    Surface *CacheManager::getSurface( const char *fileName )
    {
        return (Surface*) getCacheable( fileName, SurfaceCacheable );
    }

    Mask *CacheManager::getMask( const char *fileName )
    {
        return (Mask*) getCacheable( fileName, MaskCacheable );
    }

    Sound *CacheManager::getSound( const char *fileName )
    {
        return (Sound*) getCacheable( fileName, SoundCacheable );
    }

    void CacheManager::clear()
    {
        for( std::list< Cacheable* >::iterator i = cacheables.begin(); i!=cacheables.end(); i++ )
            delete (*i);

        cacheables.clear();
    }

    CacheManager *getCacheManager()
    {
        return cacheManager;
    }

};
