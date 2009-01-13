import annchienta

class Animation(object):

    ## You need to call setBattle, setTarget and setCombatant
    #  before you can use it.
    def __init__( self, sprite, sound ):

        self.engine = annchienta.getEngine()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()

        self.sprite = sprite
        self.sound = sound

        self.battle = None 
        self.combatant = None
        self.target = None

    def getSprite( self ):
        return self.sprite

    def getSound( self ):
        return self.sound

    def setCombatant( self, combatant ):
        self.combatant = combatant

    def getCombatant( self ):
        return self.combatant

    def setBattle( self, battle ):
        self.battle = battle

    def setTarget( self, target ):
        self.target = target

    def getTarget( self ):
        return self.target

    def play( self ):
        pass

    def move( self, combatant, position ):

        duration = 400

        start = self.engine.getTicks()
        origPosition = annchienta.Vector( combatant.getPosition() )

        while self.inputManager.isRunning() and self.engine.getTicks()<start+duration:
            
            self.battle.update()

            factor = float( self.engine.getTicks() - start ) / duration
            combatant.setPosition( origPosition * (1.0 - factor) + position * factor )

            self.videoManager.clear()
            self.battle.draw()
            self.videoManager.flip()

        # Make sure we're in the right position in the end.
        combatant.setPosition( annchienta.Vector( position ) )

    def spriteOver( self, combatant, sprite ):

        duration = 800

        start = self.engine.getTicks()

        while self.inputManager.isRunning() and self.engine.getTicks()<start+duration:
            
            self.battle.update()

            factor = float( self.engine.getTicks() - start ) / duration
            position = combatant.getPosition() + annchienta.Vector( 0, -30 ) * factor

            self.videoManager.clear()
            self.battle.draw()

            self.videoManager.drawSurface( sprite, int(position.x)-sprite.getWidth()/2, int(position.y)-sprite.getHeight()/2 )

            self.videoManager.flip()

