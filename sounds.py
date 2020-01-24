"""
-------------------------------------------------------------------------------
Name: sounds.py
Purpose: Code adding music.

Author:	Wang.D

Created: 12/01/2020
-------------------------------------------------------------------------------
"""
import arcade


class Sounds(arcade.PlaysoundException):
    def __init__(self):
        self.sounds = []
        self.add_sounds()

    def update(self, song: int) -> None:
        """
        Function to be called by on_update to play all sound needed
        :return: none
        """
        if 0 <= song < len(self.sounds):
            self.sounds[song].pause()
            self.sounds[song].play()

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
        self.sounds.append(arcade.Sound("sounds/player_attack.mp3"))
