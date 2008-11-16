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

            /** Freeze or unfreeze this Person. When a Person is
             *  frozen, he will not be able to move, this can be
             *  useful in cutscenes.
             *  \param value True to freeze, false to unfreeze.
             */
            virtual void freeze( bool value );

            /** \return If thie Person is frozen, see freeze().
             */
            virtual bool isFrozen() const;

            /** Create an InputPersonControl instance for this
             *  Person and let it control this Person.
             */
            virtual void setInputControl();

            /** Create an SamplePersonControl instance for this
             *  Person and let it control this Person.
             */
            virtual void setSampleControl();

            /** Deletes the PersonControl instance associated
             *  with this Person. The Person will now halt.
             */
            virtual void setNullControl();

            /** Set the default standing animation for this Person.
             *  \param forceFromHeading When set to true, the "stand{north,south,east,west}" will always be used.
             */
            virtual void setStandAnimation( bool forceFromHeading=false );

            /** Set the "stand{north,east,south,west}" animation,
             *  depending where the other object is.
             *  \param object Object to look at.
             */
            virtual void lookAt( StaticObject *object );

            /** Checks if this Person collides with any Area
             *  in this Layer and executes the associated scipts
             *  if needed.
             */
            virtual void collisionWithLayerAreas();
    };

};

#endif
