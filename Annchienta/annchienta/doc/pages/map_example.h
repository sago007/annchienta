/** \page map_example Example of a Map file
 *  \code
 *  <!-- Of course, we start with an xml version tag. -->
 *  <?xml version="1.0">
 *
 *  <!-- Our main document tag is the map tag, which contains a few parameters:
 *       width: The width of this map, in tiles. So this map would be 20 tiles wide.
 *       height: The height of this map, in tiles.
 *       tilewidth: The width of one tile image, in pixels.
 *       tileheight: The width of one tile image, in pixels. This should be half of tilewidth.
 *       tileset: a relative path to the TileSet directory for this map.
 *       -->
 *  <map width="20" height="20" tilewidth="32" tileheight="16" tileset="tiles/example">
 *
 *      <!-- Maps are built from different layers. Most map objects go into a layer node.
 *           z: The z offset for this layer. Should be 0 when there's only one layer.
 *           opacity: Might one day contain the opacity of a layer. Currently unsupported.
 *           -->
 *      <layer z="0" opacity="255">
 *
 *          <!-- Tiles contains codes corresponding to the tiles attributes, like this:
 *               {tile point1 height} {tile point1 surface}
 *               {tile point2 height} {tile point2 surface}
 *               {tile point3 height} {tile point3 surface}
 *               {tile point4 height} {tile point4 surface}
 *               {tile sidesurface offset} {tile sidesurface}
 *               More information about this can be found at the Tile class documentation.
 *               But you shouldn't worry about this too much, as you'd generally use a
 *               map editor to generate these.
 *               -->
 *          <tiles>
 *               0 1 0 1 0 1 0 1 15 2 ...
 *          </tiles>
 *
 *          <!-- Tile obstruction tells when you can enter a tile. There are three
 *               possibilities, documented in the Tile class documentation.
 *               Generally, you use a map editor to generate these.
 *               -->
 *          <obstruction>
 *              0 0 0 0 0 1 0 1 0 0 ...
 *          </obstruction>
 *
 *          <!-- Tiles will drawn slightly darker when they're shadowed. This is
 *               documented in the Tile class documentation as well. Generally,
 *               you use a map editor to generate these.
 *               -->
 *          <shadowed>
 *              0 0 1 0 0 0
 *          </shadowed>
 *
 *          <!-- Documentation unfinished. -->
 *
 *      </layer>
 *
 *  </map>
 *  \endcode
 */

