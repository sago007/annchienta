import annchienta
import battle

battleManager = battle.getBattleManager()
annchienta.getAudioManager().playMusic("music/tasumian.ogg")
annchienta.getVideoManager().setClearColor(20,51,2)
battleManager.enemiesInMap = ["hawk"]
battleManager.battleBackground = "images/backgrounds/woods.png";
