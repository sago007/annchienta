/* This file is part of the Annchienta Project
 * Please consult the license and copyright details in Annchienta/license.txt
 */

#include "inputpersoncontrol.h"

#include "inputmanager.h"
#include "mapmanager.h"
#include "person.h"

namespace Annchienta
{

    InputPersonControl::InputPersonControl( Person *_person ): PersonControl(_person)
    {
        inputManager = getInputManager();
    }

    InputPersonControl::~InputPersonControl()
    {
        if( person==inputManager->getInputControlledPerson() )
            inputManager->setInputControlledPerson(0);
    }

    void InputPersonControl::affect()
    {
        int x = 0, y = 0;

        if( person->isFrozen() )
            return;

        if( inputManager->personInputIsEnabled() && person==inputManager->getInputControlledPerson() )
        {
            if( inputManager->keyDown( SDLK_LEFT ) )
                x--;
            else if( inputManager->keyDown( SDLK_RIGHT ) )
                x++;
            else if( inputManager->keyDown( SDLK_UP ) )
                y--;
            else if( inputManager->keyDown( SDLK_DOWN ) )
                y++;
    
            if( inputManager->keyTicked( inputManager->getInteractKey() ) )
                person->interact();

            person->move( x, y );
        }
    }

};
