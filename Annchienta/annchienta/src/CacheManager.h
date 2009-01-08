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

#ifndef ANNCHIENTA_CACHEMANAGER_H
#define ANNCHIENTA_CACHEMANAGER_H

#include <list>
#include <cstdio>
#include <cstring>
#include "Engine.h"
#include "Cacheable.h"

namespace Annchienta
{

    class Surface;
    class Mask;
    class Sound;

    /** This describes a class which is used to create
	 *  an engine cache, so certain data objects can be
	 *  loaded quicker.
	 */
    class CacheManager
    {
        private:
            std::list< Cacheable* > cacheables;

        public:
            #ifndef SWIG
                CacheManager();
                ~CacheManager();
            #endif

            /** Fetches a Cacheable from the cache. It is better to use the
             *  getSurface(), getSound(), getMask()... functions when
             *  possible.
             *  \param fileName Filename of the sought cacheable.
             *  \param cacheableType CacheableType of the sought cacheable.
             *  \return The sought Cacheable.
             */
            Cacheable *getCacheable( const char *fileName, CacheableType cacheableType );

            /** Fetches a Surface from the cache. The Surface
             *  is loaded if it isn't found in the cache.
             *  \param fileName File to be loaded.
             *  \return The desired Surface.
             */
            Surface *getSurface( const char *fileName );

            /** Fetches a Mask from the cache. The Mask
             *  is loaded if it isn't found in the cache.
             *  \param fileName File to be loaded.
             *  \return The desired Mask.
             */
            Mask *getMask( const char *fileName );

            /** Fetches a Sound from the cache. The Sound
             *  is loaded if it isn't found in the cache.
             *  \param fileName File to be loaded.
             *  \return The desired Sound.
             */
            Sound *getSound( const char *fileName );

            /** Clears the cache. All objects are removed
             *  from the cache.
             */
            void clear();

    };

    /** \return An instance of the global CacheManager.
     */
    CacheManager *getCacheManager();

};

#endif
