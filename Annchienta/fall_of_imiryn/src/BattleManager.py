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

        self.randomBattleEnemies = []

    def setRandomBattleBackground( self, background ):
        self.randomBattleBackground = background

    def setRandomBattleEnemies( self, enemies ):
        self.randomBattleEnemies = enemies

    ## A more simple function to run a battle.
    #
    def runBattle( self, enemyNames, background, canFlee=True ):

        self.mathManager.newRandomSeed()

        combatants = list(self.partyManager.team)

        enemyElements = self.enemiesFile.getElementsByTagName("enemy")
        for name in enemyNames:
            found = filter( lambda e: str(e.getAttribute("name"))==name, enemyElements )
            if len(found):
                combatants += [ Enemy.Enemy( found[0] ) ]
            else:
                self.logManager.error( "No enemy called "+name+" found in "+self.enemiesLocation+"." )

        # Choose a nice battle music.
        playingMusic = self.audioManager.getPlayingMusic()
        self.audioManager.playMusic( "music/battle" + str(self.mathManager.randInt(1,4)) + ".ogg" )

        battle = Battle.Battle( combatants, background, canFlee )

        self.battleIntro()
        battle.run()

        self.audioManager.playMusic( playingMusic )

        return battle.won

    # Tries a random battle
    def throwRandomBattle( self ):

        if self.randomBattleDelay>0:
            self.randomBattleDelay -= 1
            return
        else:
            self.randomBattleDelay = self.mathManager.randInt( 400, 900 )

            # Return if there are no enemies in this area.
            if not len(self.randomBattleEnemies):
                return

            enames = map( lambda a: self.randomBattleEnemies[self.mathManager.randInt(0,len(self.randomBattleEnemies))], range(self.mathManager.randInt(2,5)))

            self.runBattle( enames, annchienta.Surface( self.randomBattleBackground ), True )

    # Displays a battle intro.
    def battleIntro( self ):

        # Play intro sound
        self.audioManager.playSound( self.drum )

        start = self.engine.getTicks()

        while self.engine.getTicks() < start + 800:

            self.videoManager.boxBlur( 0, 0, self.videoManager.getScreenWidth(), self.videoManager.getScreenHeight() )
            self.videoManager.flip()

def init():
    global globalBattleManagerInstance
    globalBattleManagerInstance = BattleManager()

def getBattleManager():
    return globalBattleManagerInstance

