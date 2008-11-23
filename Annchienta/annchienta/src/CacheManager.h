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

namespace Annchienta
{

    class Surface;
    class Mask;
    class Sound;

    /** A class used internally by the CacheManager
     *  to store objects in it's cache.
     */
    template <class T> class CacheObject;
    /** This describes a class which is used to create
	 *  an engine cache, so certain data objects can be
	 *  loaded quicker.
	 */
    class CacheManager
    {
        private:
            std::list< CacheObject<Surface> > surfaces;
            std::list< CacheObject<Mask> > masks;
            std::list< CacheObject<Sound> > sounds;

        public:
            #ifndef SWIG
                CacheManager();
                ~CacheManager();
            #endif

            /** Fetches a Surface from the cache. The Surface
             *  is loaded if it isn't found in the cache.
             *  \param filename File to be loaded.
             *  \return The desired Surface.
             */
            Surface *getSurface( const char *filename );

            /** Fetches a Mask from the cache. The Mask
             *  is loaded if it isn't found in the cache.
             *  \param filename File to be loaded.
             *  \return The desired Mask.
             */
            Mask *getMask( const char *filename );

            /** Fetches a Sound from the cache. The Sound
             *  is loaded if it isn't found in the cache.
             *  \param filename File to be loaded.
             *  \return The desired Sound.
             */
            Sound *getSound( const char *filename );

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
