import annchienta

inputManager = annchienta.getInputManager()
mapManager = annchienta.getMapManager()

if inputManager.keyTicked( annchienta.SDLK_RETURN ):

    import scene
    import party
    sceneManager = scene.getSceneManager()
    partyManager = party.getPartyManager()

    partyManager.save()
    sceneManager.text("Game saved.")

