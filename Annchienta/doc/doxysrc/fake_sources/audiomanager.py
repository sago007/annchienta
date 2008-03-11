
## \brief Obtain the AudioManager instance.
#
#  Use this function to get access to the AudioManager
#  instance anywhere.
#
#  \return The global AudioManager instance.
def getAudioManager():
    pass


## \brief Handles audio tasks.
#
#  You use this class to perform audio tasks: play music, sounds, etc.
class AudioManager:

    ## \brief Plays a sound.
    #
    #  \param sound Sound to be played.
    def playSound( sound ):
        pass

    ## \brief Plays background some music.
    #
    #  When the given music is already playing, nothing happens. When
    #  other music is already playing, the other music is stopped.
    #
    #  \param filename Filename of the music file to be played.
    def playMusic( filename ):
        pass

