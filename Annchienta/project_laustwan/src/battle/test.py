import xml.dom.minidom
import Combatant, Battle
import annchienta

annchienta.init()

doc = xml.dom.minidom.parse( "test.xml" )
com1 = Combatant.BaseCombatant( doc.getElementsByTagName("combatant")[0] )
com2 = Combatant.BaseCombatant( doc.getElementsByTagName("combatant")[1] )

battle = Battle.Battle( [com1, com2] )
battle.run()

