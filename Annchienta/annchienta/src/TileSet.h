/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_TILESET_H
#define ANNCHIENTA_TILESET_H

#include "Engine.h"

namespace Annchienta
{

    class Surface;
    class Mask;

    /** A TileSet is simply a collection of tiles. A Map
     *  always has a TileSet attached to it.
     */
    class TileSet
    {
        private:
            char directory[DEFAULT_STRING_SIZE];

            Surface **surfaces;
            int numberOfSurfaces;

            Surface **sideSurfaces;
            int numberOfSideSurfaces;

            Mask *mask;

        public:

            /** Load a TileSet from a directory. The directory should
             *  be formed like this:
             *
             *  There should be tile images, png files with dimensions
             *  as set in MapManager::setTileWidth(). These images should
             *  be named: 1.png, 2.png, 3.png...
             *
             *  There can also be side tiles. These should be named:
             *  side1.png, side2.png, side3.png...
             *
             *  Automatically, a transparent tile and side tile will
             *  be generated. These both have the number '0'.
             */
            TileSet( const char *directory );
            ~TileSet();

            /** Returns the tile image corresponding with the given
             *  tileNumber.
             */
            Surface *getSurface( int tileNumber ) const;

            /** Returns the tile image corresponding with the given
             *  tileNumber.
             */
            Surface *getSideSurface( int sideNumber ) const;

            /** Gets a reference to a Mask that has the form of
             *  a simple isometric tile, in the correct size.
             *  This can be handy for collision detection.
             */
            Mask *getMask() const;

            /** \return The path to the directory where the tiles were found.
             */
            const char *getDirectory() const;

            /** \return the number of tile surfaces.
             */
            int getNumberOfSurfaces() const;

            /** \return the number of side surfaces
             */
            int getNumberOfSideSurfaces() const;
    };
};

#endif
