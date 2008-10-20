/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
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

    #ifndef SWIG
        template <class T>
        struct CacheObject
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
    #endif

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
