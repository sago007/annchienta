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

#ifndef ANNCHIENTA_CACHEABLE_H
#define ANNCHIENTA_CACHEABLE_H

#include "Engine.h"

namespace Annchienta
{
    enum CacheableType
    {
        UnknownCacheable = 0,
        SurfaceCacheable,
        MaskCacheable,
        SoundCacheable
    };

    /** Class used for objects that can be
     *  cached by the CacheManager.
     */
    class Cacheable
    {
        private:
            char fileName[DEFAULT_STRING_SIZE];

        public:
            Cacheable( const char *fileName );
            virtual ~Cacheable();

            virtual CacheableType getCacheableType() const;
            const char *getFileName() const;
    };
};

#endif
