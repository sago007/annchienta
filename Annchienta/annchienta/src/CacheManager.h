/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_CACHEMANAGER_H
#define ANNCHIENTA_CACHEMANAGER_H

#include <list>
#include <stdio.h>
#include <string.h>
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

            Surface *getSurface( const char *filename );
            //void deleteSurface( Surface *surface );

            Mask *getMask( const char *filename );
            //void deleteMask( Mask *mask );

            Sound *getSound( const char *filename );

            void clear();

    };

    CacheManager *getCacheManager();

};

#endif
