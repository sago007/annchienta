import annchienta
import scene
import party

mapManager = annchienta.getMapManager()
sceneManager = scene.getSceneManager()
partyManager = party.getPartyManager()

player = partyManager.player
pp = player.getPosition()
layer = mapManager.getCurrentMap().getCurrentLayer()

guards = []
# find all guards
for i in range(layer.getNumberOfObjects()):
    if str(layer.getObject(i).getName())=="guard":
        guards.append( layer.getObject(i) )

# select the closest guard
guard = None
dist = 0
for g in guards:
    d = pp.distance( g.getPosition() )
    if d<=dist or guard is None:
        dist = d
        guard = g

if guard is not None:
    sceneManager.initDialog( [guard, player] )
    mapManager.renderFrame()
    sceneManager.speak( guard, "Hey, you!" )
    sceneManager.quitDialog()
    player.setPosition( annchienta.Point( annchienta.TilePoint, 3, 29 ) )
    partyManager.refreshMap()
