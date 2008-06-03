import annchienta
import battle
battleManager = battle.getBattleManager()
annchienta.getAudioManager().playMusic("music/tasumian.ogg")
annchienta.getVideoManager().setClearColor(20,51,2)
battleManager.enemiesInMap = [] #["spider", "worm"]
battleManager.battleBackground = "images/backgrounds/prison.png";
