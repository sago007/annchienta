import annchienta
import Animation

class SpriteAnimation( Animation.Animation ):

    def __init__( self, sprite, sound ):
        Animation.Animation.__init__( self, sprite, sound )
        self.audioManager = annchienta.getAudioManager()

    def play( self ):

        if self.getSound():
            self.audioManager.playSound( self.getSound() )

        self.spriteOver( self.getTarget(), self.getSprite() )
