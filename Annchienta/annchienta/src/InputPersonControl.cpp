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

#include "InputPersonControl.h"

#include "InputManager.h"
#include "MathManager.h"
#include "MapManager.h"
#include "Person.h"
#include "Point.h"
#include "Mask.h"
#include "Layer.h"
#include "Vector.h"

namespace Annchienta
{

    InputPersonControl::InputPersonControl( Person *_person ): PersonControl(_person)
    {
        inputManager = getInputManager();
        mathManager  = getMathManager();
    }

    InputPersonControl::~InputPersonControl()
    {
        if( person==inputManager->getInputControlledPerson() )
            inputManager->setInputControlledPerson(0);
    }

    void InputPersonControl::affect()
    {
        int x = 0, y = 0;

        if( inputManager->getInputMode()==InteractiveMode && person==inputManager->getInputControlledPerson() )
        {
            /* Mouse input. Listen to it.
             */
            if( inputManager->buttonDown(0) )
            {
                Point mouse = inputManager->getMousePoint();
                mouse.convert( MapPoint );

                Point pos = person->getPosition();
                pos.convert( MapPoint );

                /* Don't forget to take Z in account here.
                 */
                mouse.y += person->getLayer()->getZ();
                mouse.y += pos.z;

                mouse.convert( IsometricPoint );

                pos.convert( IsometricPoint );
    
                Vector deltaVector( mouse.x - pos.x, mouse.y - pos.y );
                if( deltaVector.lengthSquared() >= 200 )
                {
                    if( mathManager->abs(mouse.x-pos.x) > mathManager->abs(mouse.y-pos.y) )
                        x += mouse.x<pos.x?-1:1;
                    else
                        y += mouse.y<pos.y?-1:1;
                }
            }
            /* Keyboard input, second choice.
             */
            else
            {
                if( inputManager->keyDown(SDLK_UP) )
                    y--;
                else if( inputManager->keyDown(SDLK_RIGHT) )
                    x++;
                else if( inputManager->keyDown(SDLK_DOWN) )
                    y++;
                else if( inputManager->keyDown(SDLK_LEFT) )
                    x--;
            }

            person->move( x, y );

            if( inputManager->buttonTicked( 0 ) || inputManager->interactKeyTicked() )
                this->tryInteract();

        }

    }

    void InputPersonControl::tryInteract()
    {
        Layer *layer = person->getLayer();

        if( !layer )
            return;

        bool searching = true;

        /* We loop through the objects in the layer to see if we find
         * one where we might interact with.
         */
        for( int i=0; layer->getObject(i) && searching; i++ )
        {
            StaticObject *object = layer->getObject(i);

            /* Of course, we don't want to interact with ourselves.
             */
            if( object != (StaticObject*) person )
            {
    
                /* Check if the object is clicked.
                 */
                Point mp = object->getMaskPosition().to( ScreenPoint );
                bool clicked = ( inputManager->hover( mp.x, mp.y, mp.x+object->getMask()->getWidth(), mp.y+object->getMask()->getHeight() ) );
    
                mp.convert( MapPoint );
                Point p = person->getMaskPosition().to( MapPoint );
                bool boxCollision = person->getMask()->collision( p.x, p.y, object->getMask(), mp.x, mp.y, true );

                /* If the object is not clicked, but the default interact
                 * key is pressed, maybe we still want to interact.
                 */
                if( !clicked && inputManager->keyTicked( inputManager->getInteractKey() ) )
                    clicked = true;

                if( clicked && boxCollision )
                {
                    /* Make sure the Z difference isn't too large. Why: We don't
                     * want the player to be able to talk with eg. someone standing
                     * on a cliff when the player is standing on the ground etc.
                     */
                    if( mathManager->abs(p.z - object->getPosition().z) < getMapManager()->getMaxAscentHeight() )
                    {
                        /* We skip object with which can not be interacted.
                         */
                        if( object->canInteract() )
                        {
                            setActiveObject( person );
                            setPassiveObject( object );
                
                            object->onInteract();
                
                            setActiveObject( 0 );
                            setPassiveObject( 0 );
                            searching = false;
                        }
                    }
                }
            }
        }
    }

};
