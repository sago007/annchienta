/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_PERSON_H
#define ANNCHIENTA_PERSON_H

#include "StaticObject.h"

namespace Annchienta
{
    class PersonControl;

    /** A Person is a class derived from StaticObject,
     *  meaning it is an object in the Map. The main
     *  thing about a Person is that he is able to move.
     */
    class Person: public StaticObject
    {
        protected:
            PersonControl *control;
            bool frozen;
            int heading;

            #ifndef SWIG
                /* Gives an error when parsed through swig? */
                const static int squaredInteractDistance = 600;
            #endif

        public:

            /** Create a new Person.
             *  \param name Name for this Person.
             *  \param configFile XML configuration file for the Person.
             */ 
            Person( const char *name, const char *configFile );

            /** Just another destructor.
             */
            virtual ~Person();

            /** \return The EntityType for this Person.
             */
            virtual EntityType getEntityType() const;

            /** Update this Person.
             */
            virtual void update();

            /** Relatively move this Person. This function might
             *  not move the Person, for example when there's
             *  something in the way. To make sure the Person moves,
             *  set the force flag to true.
             *  \param x Distance to move over X axis.
             *  \param y Distance to move over Y axis.
             *  \param force Ignore all obstructions and move.
             *  \return If the Person was able to move.
             */
            virtual bool move( int x, int y, bool force=false );

            /** This function calls move() to move this Person in
             *  the direction of the given point. It does nothing
             *  when this Person is close enough to the given Point.
             *  \param point Point to step to.
             *  \param force See move().
             *  \return If the Person was able to move.
             */
            virtual bool stepTo( Point point, bool force=true );

            virtual void freeze( bool );
            virtual bool isFrozen() const;

            virtual void setInputControl();
            virtual void setSampleControl();
            virtual void setNullControl();

            virtual void setStandAnimation( bool forceFromHeading=false );
            virtual void lookAt( StaticObject *object );

            virtual void collisionWithLayerAreas();
    };

};

#endif
