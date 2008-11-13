import annchienta, Battle, Enemy, PartyManager
import xml.dom.minidom

## Spawns random battles, provides easy interface
#  to run battles.
class BattleManager:

    def __init__( self ):

        self.engine = annchienta.getEngine()
        self.mathManager = annchienta.getMathManager()
        self.videoManager = annchienta.getVideoManager()
        self.inputManager = annchienta.getInputManager()
        self.logManager = annchienta.getLogManager()
        self.audioManager = annchienta.getAudioManager()
        self.partyManager = PartyManager.getPartyManager()

        self.enemiesLocation = "battle/enemies.xml"
        self.enemiesFile = xml.dom.minidom.parse( self.enemiesLocation )

        self.randomBattleDelay = self.mathManager.randInt(300,400)
        self.background = None

        # Drum on battle start
        self.drum = annchienta.Sound( "sounds/battle.ogg" )

        self.enemiesInMap = []

    ## A more simple function to run a battle.
    #
    def runBattle( self, enemyNames, background, canFlee=True ):

        combatants = list(self.partyManager.team)

        enemyElements = self.enemiesFile.getElementsByTagName("enemy")
        for name in enemyNames:
            found = filter( lambda e: str(e.getAttribute("name"))==name, enemyElements )
            if len(found):
                combatants += [ Enemy.Enemy( found[0] ) ]
            else:
                self.logManager.error( "No enemy called "+name+" found in "+self.enemiesLocation+"." )

        battle = Battle.Battle( combatants, background, canFlee )
        self.battleIntro()
        battle.run()

        return battle.won

    # Tries a random battle
    def throwRandomBattle( self ):

        if self.randomBattleDelay>0:
            self.randomBattleDelay -= 1
            return
        else:
            self.randomBattleDelay = self.mathManager.randInt( 400, 900 )

            # Return if there are no enemies in this level.
            if not len(self.enemiesInMap):
                return

            enames = map( lambda a: self.enemiesInMap[self.mathManager.randInt(0,len(self.enemiesInMap))], range(self.mathManager.randInt(2,5)))

            self.runBattle( enames, annchienta.Surface( self.background ), True )

    # Displays a battle intro.
    def battleIntro( self ):

        self.videoManager.setColor( 255, 255, 255, 200 )
        triangleLength = self.mathManager.max( self.videoManager.getScreenWidth(), self.videoManager.getScreenHeight() )
        self.videoManager.translate( self.videoManager.getScreenWidth()/2, self.videoManager.getScreenHeight()/2 )

        # Play intro sound
        self.audioManager.playSound( self.drum )

        for i in range(20):

            self.videoManager.rotate( self.mathManager.randInt(0, 360 ) )
            self.videoManager.translate( self.mathManager.randInt( -triangleLength/4, triangleLength/4 ), self.mathManager.randInt( -triangleLength/4, triangleLength/4 ) )
            self.videoManager.drawTriangle( 0, -triangleLength, -self.mathManager.randInt(2,10), triangleLength, self.mathManager.randInt(2,10), triangleLength )
            start = self.engine.getTicks()

            while self.inputManager.running() and self.engine.getTicks()<start+20:
                self.videoManager.end()

        self.videoManager.reset()

def initBattleManager():
    global globalBattleManagerInstance
    globalBattleManagerInstance = BattleManager()

def getBattleManager():
    return globalBattleManagerInstance

