import annchienta, SceneManager, PartyManager
partyManager, sceneManager = PartyManager.getPartyManager(), SceneManager.getSceneManager()
mathManager = annchienta.getMathManager()

messages = [ "He doesn't look to healthy.", "Spooky.",
             "I wonder what happened to him?",
             "I have a bad feeling about this...",
             "This is getting scary...",
             "I wonder how he died?",
             "I hope I don't end up like that..." ]

sceneManager.initDialog( [partyManager.player] )
sceneManager.speak( partyManager.player, messages[ mathManager.randInt(len(messages)) ] )
sceneManager.quitDialog()
