/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_PERSON_H
#define ANNCHIENTA_PERSON_H

#include "StaticObject.h"

namespace Annchienta
{
    class PersonControl;

    class Person: public StaticObject
    {
        protected:
            PersonControl *control;
            bool frozen;
            int heading;

            #ifndef SWIG
                const static int squaredInteractDistance = 600;
            #endif

        public:
            Person( const char *name, const char *configfile );
            virtual ~Person();

            virtual EntityType getEntityType() const;

            virtual void update();

            virtual bool move( int x, int y, bool force=false );
            virtual bool stepTo( Point );

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