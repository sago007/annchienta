import annchienta, Battle, Enemy, PartyManager
import xml.dom.minidom

## Spawns random battles, provides easy interface
#  to run battles.
class BattleManager:

    def __init__( self ):

        self.enemiesLocation = "battle/enemies.xml"
        self.enemiesFile = xml.dom.minidom.parse( self.enemiesLocation )

        self.randomBattleDelay = annchienta.randInt(300,400)
        self.background = None

        self.enemiesInMap = []

    ## A more simple function to run a battle.
    #
    def runBattle( self, enemyNames, background, canFlee=True ):

        logManager = annchienta.getLogManager()
        partyManager = PartyManager.getPartyManager()

        combatants = list(partyManager.team)

        enemyElements = self.enemiesFile.getElementsByTagName("enemy")
        for name in enemyNames:
            found = filter( lambda e: str(e.getAttribute("name"))==name, enemyElements )
            if len(found):
                combatants += [ Enemy.Enemy( found[0] ) ]
            else:
                logManager.error( "No enemy called "+name+" found in "+Battle.enemiesLocation+"." )

        battle = Battle.Battle( combatants, background, canFlee )
        battle.run()

        return battle.won

    # Tries a random battle
    def throwRandomBattle( self ):

        if self.randomBattleDelay>0:
            self.randomBattleDelay -= 1
            return
        else:
            self.randomBattleDelay = annchienta.randInt( 400, 900 )

            # Return if there are no enemies in this level.
            if not len(self.enemiesInMap):
                return

            enames = map( lambda a: self.enemiesInMap[annchienta.randInt(0,len(self.enemiesInMap)-1)], range(annchienta.randInt(2,4)))

            self.runBattle( enames, annchienta.Surface( self.background ), True )

def initBattleManager():
    global globalBattleManagerInstance
    globalBattleManagerInstance = BattleManager()

def getBattleManager():
    return globalBattleManagerInstance
