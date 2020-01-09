import arcade


class Sounds():
    def __init__(self):
        self.sounds = []
        self.add_sounds()

    def update(self) -> None:
        """
        Function to be called by on_update to play all sound needed
        :return: none
        """
        self.sounds[0].play()

    def play_sound(self, sound) -> None:
        """
        Plays a sound with the specified name
        :param sound: sound name
        :return: none
        """

    def add_sounds(self) -> None:
        """
        loads all sounds from disk and adds them to self.sounds for later use
        :return: none
        """
        self.sounds.append(arcade.Sound("sounds/minecraft-theme.mp3"))
        self.sounds.append(arcade.Sound("sounds/starcraft-theme.mp3"))
