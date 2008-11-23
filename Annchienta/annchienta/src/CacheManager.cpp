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

#include "Surface.h"
#include "Mask.h"
#include "Sound.h"
#include "LogManager.h"

namespace Annchienta
{
    /* A class used internall by the cachemanager
     * to store objects. */
    template <class T>
    class CacheObject
    {
        public:
            char name[DEFAULT_STRING_SIZE];
            T *data;
            int references;

            CacheObject( const char *_name, T *_data ): data(_data), references(1)
            {
                if( _name )
                    strcpy( name, _name );
            };
    };

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

    /*void CacheManager::deleteSurface( Surface *surface )
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
    }*/

    Mask *CacheManager::getMask( const char *filename )
    {
        for( std::list< CacheObject<Mask> >::iterator i = masks.begin(); i!=masks.end(); i++ )
        {
            if( !strcmp( filename, (*i).name ) )
            {
                (*i).references++;
                return (*i).data;
            }
        }

        Mask *mask = new Mask( filename );
        masks.push_back( CacheObject<Mask>( filename, mask ) );
        return mask;
    }

    /*void CacheManager::deleteMask( Mask *mask )
    {
        for( std::list< CacheObject<Mask> >::iterator i = masks.begin(); i!=masks.end(); i++ )
        {
            if( mask == (*i).data )
            {
                (*i).references--;
                if( (*i).references <= 0 )
                {
                    delete (*i).data;
                    masks.erase( i );
                }
                return;
            }
        }
    }*/

    Sound *CacheManager::getSound( const char *filename )
    {
        for( std::list< CacheObject<Sound> >::iterator i = sounds.begin(); i!=sounds.end(); i++ )
        {
            if( !strcmp( filename, (*i).name ) )
            {
                (*i).references++;
                return (*i).data;
            }
        }

        Sound *sound = new Sound( filename );
        sounds.push_back( CacheObject<Sound>( filename, sound ) );
        return sound;
    }

    void CacheManager::clear()
    {
        for( std::list< CacheObject<Surface> >::iterator i = surfaces.begin(); i!=surfaces.end(); i++ )
            delete (*i).data;

        surfaces.clear();

        for( std::list< CacheObject<Mask> >::iterator i = masks.begin(); i!=masks.end(); i++ )
            delete (*i).data;

        masks.clear();

        for( std::list< CacheObject<Sound> >::iterator i = sounds.begin(); i!=sounds.end(); i++ )
            delete (*i).data;

        sounds.clear();
    }

    CacheManager *getCacheManager()
    {
        return cacheManager;
    }

};
