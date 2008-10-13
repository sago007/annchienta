/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_MAPMANAGER_H
#define ANNCHIENTA_MAPMANAGER_H

namespace Annchienta
{
    class Map;
    class StaticObject;
    class InputManager;
    class Person;

    class MapManager
    {
        private:
            InputManager *inputManager;

            int tileWidth, tileHeight;
            int cameraX, cameraY;
            int updatesPerSecond;
            Map *currentMap;
            StaticObject *cameraTarget;

            int maxAscentHeight, maxDescentHeight;

            char *onUpdateScript, *onUpdateCode;

            bool m_running;

        public:
            #ifndef SWIG
                MapManager();
                ~MapManager();

                int getUpdatesNeeded() const;
            #endif

            /** Sets the tilewidth. You should call this
             *  before actually using the MapManager.
             *  Typically, you would use (64,32) or (32,16)
             *  for tileWidth and tileHeight.
             *  \param tileWidth The new Tile width.
             */
            void setTileWidth( int tileWidth );

            /** \return The current Tile width.
             */
            int getTileWidth() const;

            /** Sets the tileheight. You should call this
             *  before actually using the MapManager.
             *  \param tileHeight The new Tile height.
             */
            void setTileHeight( int tileHeight );

            /** \return The current Tile height.
             */
            int getTileHeight() const;

            /** Sets the camera X offset. This can also be
             *  handled automatically by using cameraFollow()
             *  or cameraPeekAt().
             */
            void setCameraX( int x );

            /** \return The current camera X offset.
             */
            int getCameraX() const;

            /** Sets the camera Y offset.
             */
            void setCameraY( int y );

            /** \return The current camera Y offset.
             */
            int getCameraY() const;

            /** Makes the camera smoothly follow object,
             *  until another object is set. If you don't
             *  want to follow any objects anymore, use
             *  cameraFollow(0).
             */
            void cameraFollow( StaticObject *object );

            /** \return The object followed by the camera, see cameraFollow().
             */
            StaticObject *getCameraFollow() const;

            /** Makes the camera have a quick peek at the
             *  provided object. Usually, this means the camera
             *  will move one step in the directioin of object.
             *  If you want to instantly peek at object, set
             *  instantly to true.
             */
            void cameraPeekAt( StaticObject *object, bool instantly=false );

            /** Sets the number of times updateOnce() will be called per
             *  second. You usually do this before actually using
             *  the MapManager.
             */
            void setUpdatesPerSecond( int );

            /** Sets the current Map to be displayed, updated...
             */
            void setCurrentMap( Map *map );

            /** Sets a NullMap, which simply means no Map.
             *  I don't think anyone needs this, actually?
             */
            void setNullMap();

            /** \return A reference to the current Map.
             */
            Map *getCurrentMap() const;

            /** Sets the maximum height the player can ascent
             *  during one step. If the height difference is
             *  larger than this value, the player will not be
             *  able to enter the Tile.
             */
            void setMaxAscentHeight( int maxAscentHeight );

            /** \return The max ascent height. See setMaxAscentHeight().
             */
            int getMaxAscentHeight() const;

            /** Sets the maximum height the player can descent
             *  during one step. If the height difference is
             *  larger than this value, the player will not be
             *  able to enter the Tile.
             */
            void setMaxDescentHeight( int maxDescentHeight );

            /** \return The max descent height. See setMaxDescentHeight().
             */
            int getMaxDescentHeight() const;

            /** Searches the current Map for a StaticObject
             *  with the given name. This basically calls to
             *  Map::getObject().
             */
            StaticObject *getObject( const char *name );

            /** Sets a script that will be run every time
             *  updateOnce() is called.
             */
            void setOnUpdateScript( const char *filename );

            /** Sets a piece of code that will be run every time
             *  updateOnce() is called.
             */
            void setOnUpdateCode( const char *code );

            /** This function runs the MapManager. It should
             *  basically run your game. It does not return
             *  until the player quits the game.
             */
            void run();

            /** Polls if the game is running.
             */
            bool running() const;

            /** Stops the MapManager from running. You should
             *  call this on game over, when the player
             *  quits your game...
             */
            void stop();

            /** Updates the MapManager. This calls to updateOnce
             *  a number of times, this number depends on the
             *  amount set by setUpdatesPerSecond() and the time
             *  passed since the last update.
             *  \param updateInput If we should update the InputManager as well.
             */
            void update( bool updateInput=true );

            /** Updates the MapManager a single time. This is
             *  mostly used internally. See update().
             */
            void updateOnce( bool updateInput=true );

            /** Draws the current Map to the screen.
             */
            void draw() const;

            /** The same as draw()... both are kept for
             *  comptability issues.
             */
            void renderFrame() const;

            /** Resynchronizes the timing. Some explanation:
             *  
             *  Every time update() is called, the MapManager
             *  calls updateOnce() a number of times. When more
             *  time has passed since the last update, updateOnce()
             *  will be called more.
             *
             *  When, for example, you use a blocking function
             *  you wrote yourself that displays a text window,
             *  a lot of time will pass. This would mean that
             *  updateOnce() would be called hundreds of times.
             *
             *  In order to prevent this, call this function at
             *  the end of your function. That way, the number
             *  of updates will be reduced to a more fitting number.
             */
            void resync();
    };

    MapManager *getMapManager();

};

#endif
