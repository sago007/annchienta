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

#include "Cacheable.h"

#include <cstdio>
#include <cstring>

namespace Annchienta
{

    Cacheable::Cacheable( const char *_fileName )
    {
        if( _fileName )
            strcpy( fileName, _fileName );
    }

    Cacheable::~Cacheable()
    {
    }

    CacheableType Cacheable::getCacheableType() const
    {
        return UnknownCacheable;
    }

    const char *Cacheable::getFileName() const
    {
        return fileName;
    }
};
