/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#ifndef ANNCHIENTA_PERSON_H
#define ANNCHIENTA_PERSON_H

#include "staticobject.h"

namespace Annchienta
{
    class PersonControl;

    class Person: public StaticObject
    {
        protected:
            PersonControl *control;
            bool frozen;
            int heading;

            const static int squaredInteractDistance = 600;

        public:
            Person( const char *name, const char *configfile );
            virtual ~Person();

            virtual EntityType getEntityType() const;

            virtual void update();

            virtual bool move( int x, int y, bool force=false );
            virtual bool stepTo( int x, int y );

            virtual void freeze( bool );
            virtual bool isFrozen() const;

            virtual void setInputControl();

            virtual void interact();

            virtual void setStandAnimation();
            virtual void lookAt( StaticObject *object );
    };

};

#endif
