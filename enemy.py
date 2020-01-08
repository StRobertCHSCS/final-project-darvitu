import arcade, math, random
from player import Player


class Enemy(arcade.AnimatedTimeSprite):

    def __init__(self, window_width: int, window_heigth: int, player_speed=250, direction="DOWN"):
        """Constructor of the Player class, that is the entity that the user will be moving controlling.

                          :param direction: default direction of player
                          :param player_speed: speed of player
                          :param window_width: width of game window
                          :param window_heigth: height of game window
                          """
        super().__init__()

        # setting speed and direction based on creation of Player object
        self.player_speed = player_speed
        self.direction = direction
        self.previous_direction_1 = "RIGHT"
        self.previous_direction_2 = "UP"

        # change animation rate
        self.texture_change_frames = 30

        # spawn facing forward
        self.face_direction(direction)

        # setting position of Player
        self.center_x = window_width // 2
        self.center_y = window_heigth // 2

        # defining size of player for later use
        self.width = None
        self.height = None
        self.movement = True
        self.count = 0

    # animation for the player to face when it is not moving
    def face_direction(self, direction) -> None:
        """
        Faces the character animation based on the direction.
        :param direction: direction for the character to face
        :return: None
        """
        if direction == "LEFT":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=104, width=96, height=104,
                                        scale=0.5))
        elif direction == "RIGHT":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=312, width=96, height=104,
                                        scale=0.5))
        elif direction == "UP":
            self.textures = []
            for i in range(1):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=208, width=96, height=104,
                                        scale=0.5))
        elif direction == "DOWN":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=0, width=96, height=104, scale=0.5))

        else:
            print("Invalid direction to face")

    # animation for moving
    def move_direction(self, direction) -> None:
        """
        Sets animation to the direction of the player movement
        :param direction: direction of player movement
        :return: None
        """
        if direction == "DOWN":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=416, width=96, height=104,
                                        scale=0.5))
        elif direction == "LEFT":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=520, width=96, height=104,
                                        scale=0.5))
        elif direction == "UP":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=624, width=96, height=104,
                                        scale=0.5))
        elif direction == "RIGHT":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=728, width=96, height=104,
                                        scale=0.5))
        else:
            print("Direction not valid to move")

    def follow(self, player: Player, delta_time = 1/60) -> None:
        """
        Makes enemy follow the player, engine that will run all moving sprites
        Method that is called in the main.py file on_update()
        :param delta_time: time of rate of execution
        :param player: the player to follow
        :return: none
        """
        self.texture_change_frames = 2.5

        wait = random.randint(25, 50)
        if self.movement:
            self.count += 1
            if abs(self.center_x - player.center_x) > 10:
                if self.center_x < player.center_x:
                    self.direction = "RIGHT"
                if self.center_x > player.center_x:
                    self.direction = "LEFT"
            else:
                self.count = wait
        else:
            self.count += 1
            if abs(self.center_y - player.center_y) > 10:
                if self.center_y < player.center_y:
                    self.direction = "UP"
                if self.center_y > player.center_y:
                    self.direction = "DOWN"
            else:
                self.count = wait

        # changing the direction (up/down to left/right) every 25 loops
        if self.count == wait:
            self.movement = not self.movement
            self.count = 0
        # update direction of sprite
        self.move_direction(self.direction)
        if self.direction is not None:
            if self.direction == "RIGHT":
                self.center_x += self.player_speed * delta_time
            if self.direction == "LEFT":
                self.center_x -= self.player_speed * delta_time
            if self.direction == "UP":
                self.center_y += self.player_speed * delta_time
            if self.direction == "DOWN":
                self.center_y -= self.player_speed * delta_time
