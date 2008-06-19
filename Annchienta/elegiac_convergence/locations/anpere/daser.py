import annchienta, scene

player = annchienta.getActiveObject()
daser = annchienta.getPassiveObject()

sceneManager.initDialog( [player,daser] )

sceneManager.chat( daser, "Work, work, work. All we do is work. I am getting sick of this.", ["Have you seen this white-haired man?"] )
sceneManager.chat( daser, "Hmm. Maybe I have. Maybe I haven't. It's not my business... If you want to board the ship to Aldwar, hurry up.", ["Where can I find that ship?"] )
sceneManager.speak( daser, "It's just down this pier..." )

sceneManager.quitDialog()
