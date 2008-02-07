/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_CACHEMANAGER_H
#define ANNCHIENTA_CACHEMANAGER_H

#include <list>
#include <stdio.h>

namespace Annchienta
{

    class Surface;
    class Mask;

    #ifndef SWIG
        template <class T>
        struct CacheObject
        {
            public:
                char name[512];
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

        public:
            #ifndef SWIG
                CacheManager();
                ~CacheManager();
            #endif

            Surface *getSurface( const char *filename );
            void deleteSurface( Surface *surface );

            Mask *getMask( const char *filename );
            void deleteMask( Mask *mask );

            void clear();

    };

    CacheManager *getCacheManager();

};

#endif
