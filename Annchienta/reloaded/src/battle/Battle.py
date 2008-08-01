import annchienta
import SceneManager

## Holds a battle...
#
class Battle:

    def __init__( self, combatants ):
    
        # Set variables
        self.combatants = combatants
        self.running = True
        self.background = None
    
        # Get references
        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.cacheManager = annchienta.getCacheManager()
        self.sceneManager = SceneManager.getSceneManager()
        
        # Lines for the 'console' window
        self.lines = [ "An enemy appeared!", "Omg!" ]
        
    def run( self ):
    
        # Reset combatants
        for c in self.combatants:
            c.reset()
    
        # Update the lists
        self.updateCombatantLists()
        self.positionCombatants()
    
        self.lastUpdate = None
        
        # If there is currently a menu open
        self.menuOpen = False
    
        # Reset action que [ (action, combatant, target) ]
        self.actionQueue = []
        self.actionInProgress = False

        while self.running:
        
            self.update()
            
            self.videoManager.begin()
            self.draw()
            self.videoManager.end()
    
    def updateCombatantLists( self ):
    
        self.allies = filter( lambda q: q.ally, self.combatants )
        self.enemies = filter( lambda q: not q.ally, self.combatants )
        self.readyEnemies = filter( lambda q: q.timer >= 100.0, self.enemies )
        self.readyAllies = filter( lambda q: q.timer >= 100.0, self.allies )
    
    def positionCombatants( self ):
    
        # Align them and stuff
        for i in range(len(self.allies)):
            self.allies[i].position = annchienta.Vector( 80, 40+(i+1)*70 )
            
        for i in range(len(self.enemies)):
            self.enemies[i].position = annchienta.Vector( self.videoManager.getScreenWidth()-80, 40+(i+1)*70 )
    
    # We have to be very careful in this function because it
    # might very well recurse. That's why we need booleans to
    # ensure some things are not executed in the same time,
    # for example two animations or two open menu's.
    def update( self, updateInputManagerToo=True ):
    
        if updateInputManagerToo:
            self.inputManager.update()
        
        if not self.inputManager.running():
            self.running = False
            return
        
        # Remove unnecessary lines
        while len(self.lines)>2:
            self.lines.pop(0)
        
        # Calculate number of ms passed
        ms = 0.0
        if self.lastUpdate is not None:
            ms = self.engine.getTicks() - self.lastUpdate
        
        self.lastUpdate = self.engine.getTicks()
        
        # Update combatants
        for c in self.combatants:
            c.update( ms )
        
        # Update lists
        self.updateCombatantLists()
        
        # Let allies take actions
        if (not self.menuOpen) and len(self.readyAllies) and not self.actionInProgress:
            self.menuOpen = True
            actor = self.readyAllies.pop(0)
            action, target = actor.selectAction( self )
            if action is None or target is None:
                # Put this ready ally in the back
                self.readyAllies += [actor]
            else:
                self.actionQueue += [ (action, actor, target) ]
                # Make sure to reset time
                actor.timer = 0.0
            self.menuOpen = False
        
        # Let enemies take actions
        if len(self.readyEnemies):
            actor = self.readyEnemies.pop(0)
            action, target = actor.selectAction( self )
            self.actionQueue += [ (action, actor, target) ]
            # Make sure to reset timer
            actor.timer = 0.0

        # Update actionqueue
        if len(self.actionQueue) and not self.actionInProgress and not self.menuOpen:
            self.actionInProgress = True
            action, actor, target = self.actionQueue.pop()
            self.takeAction( action, actor, target )
            self.actionInProgress = False
        
        print "Queue length: "+str(len(self.actionQueue))

    def draw( self ):
    
        # Start with background
        self.videoManager.drawSurface( self.background, 0, 0 )

        # Draw the console and lines
        self.videoManager.setColor( 0, 0, 0, 100 )
        self.videoManager.drawRectangle( 0, 0, self.videoManager.getScreenWidth(), self.sceneManager.margin*2+self.sceneManager.defaultFont.getLineHeight()*2 )
        self.sceneManager.inactiveColor()
        for i in range(len(self.lines))[:2]:
            self.videoManager.drawString( self.sceneManager.defaultFont, self.lines[i], self.sceneManager.margin, self.sceneManager.margin+self.sceneManager.defaultFont.getLineHeight()*i )
        self.videoManager.setColor()
        
        # Draw the combatants
        for c in self.combatants:
            c.draw()
            
        # Draw the allies info
        self.videoManager.pushMatrix()
        self.videoManager.translate( 0, self.videoManager.getScreenHeight()-20*len(self.allies) )
        for a in self.allies:
            a.drawInfo()
            self.videoManager.translate( 0, 20 )
        self.videoManager.popMatrix()

    ## Make an combatant do an action
    #
    def takeAction( self, action, combatant, target ):
            
        # Info
        self.lines += [combatant.name+" uses "+action.name+" on "+target.name+"!"]
        
        # Let's assume we are dealing with a regular action for now
        baseDamage = 0.0
        if action.type == "physical":
            baseDamage = combatant.physicalBaseDamage()
        else:
            baseDamage = combatant.magicalBaseDamage()
            
        # Invert damage if we are dealing with restorative magic
        if action.elemental["restorative"]:
            baseDamage = -float(baseDamage)
            
        # Take the power of the attack into account
        baseDamage *= action.factor
        
        # Take the target's defense into account
        defense = target.derivedStats[ "def" if action.type == "physical" else "mdf" ]
        baseDamage *= ( (512.0 - target.derivedStats["def"])/512.0 )
    
        # Elemental properties now
        for element in action.elemental:
            if element != "restorative":
                # For example, if the action has "ice":1
                if action.elemental[element]:
                    # Multiply damage by the factor the
                    # target has set for it
                    baseDamage *= target.derivedElemental[element]
    
        # Round it
        baseDamage = int(baseDamage)

        # We can always miss, of course...
        hit = annchienta.randFloat() <= action.hit

        if hit:
            # Check for status effects
            if action.statusEffect!="none" and action.statusEffect not in target.statusEffects:
                if annchienta.randFloat() <= action.statusHit:
                    target.statusEffects += [action.statusEffect]
                    print target.name+" is now "+action.statusEffect+"!"

            # Finally, do damage to damaged ones
            target.healthStats["hp"] -= baseDamage
            if target.healthStats["hp"] < 0:
                target.healthStats["hp"] = 0
            if target.healthStats["hp"] > target.healthStats["mhp"]:
                target.healthStats["hp"] = target.healthStats["mhp"]
        else:
            self.lines += [ combatant.name.capitalize()+" misses!" ]

        # That took some effort, rest and get mp
        combatant.healthStats["mp"] -= action.cost

        # Play animation
        self.playAnimation( action, combatant, target )

        # Damage animation only if hit
        if hit:
            target.damage = baseDamage

    # Plays the animation for the given parameters
    # This calls to playXAnimation, where X depends on the action
    def playAnimation( self, action, combatant, target ):

        if action.animation == "attack":
            self.playAttackAnimation( combatant, target )
        elif action.animation == "sprite":
            self.playSpriteAnimation( target, action.animationData )

    # Animation that moves the given combatant to
    # the given position
    def playMoveAnimation( self, combatant, position, duration=400.0 ):

        start = self.engine.getTicks()
        origPosition = annchienta.Vector(combatant.position)
        while self.inputManager.running() and self.engine.getTicks()<start+duration:
            
            self.update()

            factor = float(self.engine.getTicks()-start)/duration
            combatant.position = origPosition*(1.0-factor) + position*factor

            self.videoManager.begin()
            self.draw()
            self.videoManager.end()

        # Make sure we're in the right position in the end.
        combatant.position = annchienta.Vector( position )

    # Moves the combatant to the target and back again
    def playAttackAnimation( self, combatant, target ):

        origPosition = annchienta.Vector( combatant.position )
        position = annchienta.Vector( target.position )
        dx = ( target.width/2 + combatant.width/2 )
        dx = dx if target.ally else -dx
        position.x += dx
        self.playMoveAnimation( combatant, position )
        self.playMoveAnimation( combatant, origPosition )

    def playSpriteAnimation( self, combatant, sprite, duration=800.0 ):

        start = self.engine.getTicks()
        surf = self.cacheManager.getSurface( sprite )

        while self.inputManager.running() and self.engine.getTicks()<start+duration:
            
            self.update()

            factor = float(self.engine.getTicks()-start)/duration
            position = combatant.position + annchienta.Vector(0,-30)*factor

            self.videoManager.begin()
            self.draw()
            self.videoManager.drawSurface( surf, int(position.x)-surf.getWidth()/2, int(position.y)-surf.getHeight()/2 )
            self.videoManager.end()

