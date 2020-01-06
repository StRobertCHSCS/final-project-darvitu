import arcade
class myGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)


        # sets the player variables, speed for movement, bools for if key is being pressed
        self.player_speed = 250
        self.right = False
        self.left = False
        self.up = False
        self.down = False

        # creates player class and list of players
        self.player_list = None
        self.player = None

        self.setup()
    
    # following 8 functions are animation for the player sprite
    def face_forward(self):
        self.player.textures = []
        for i in range(3):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=0,width=96,height=104,scale=0.5))
    
    def face_left(self):
        self.player.textures = []
        for i in range(3):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=104,width=96,height=104,scale=0.5))
    
    def face_up(self):
        self.player.textures = []
        for i in range(1):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=208,width=96,height=104,scale=0.5))
    
    def face_right(self):
        self.player.textures = []
        for i in range(3):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=312,width=96,height=104,scale=0.5))
    
    def move_down(self):
        self.player.textures = []
        for i in range(10):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=416,width=96,height=104,scale=0.5))
    
    def move_left(self):
        self.player.textures = []
        for i in range(10):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=520,width=96,height=104,scale=0.5))
    
    def move_up(self):
        self.player.textures = []
        for i in range(10):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=624,width=96,height=104,scale=0.5))
    
    def move_right(self):
        self.player.textures = []
        for i in range(10):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=728,width=96,height=104,scale=0.5))
        
    def setup(self):
        # creates an animated sprite for the player, sets animation refresh to once every 15 frames
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedTimeSprite()
        self.player.texture_change_frames = 30

        # spawning in facing forward
        self.face_forward()
        
        # sets positional center of player sprite
        self.player.center_x = 800 // 2
        self.player.center_y = 800 // 2 

        # adds player sprite to list of player sprites
        self.player_list.append(self.player)

        # loads tiled map
        my_map = arcade.tilemap.read_tmx("Maps/test-map-4.tmx")
        self.ground_list = arcade.tilemap.process_layer(my_map,"ground",1,)



    def on_draw(self):
        arcade.start_render()
        self.ground_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        # updates the animation state of the player sprite
        self.player_list.update_animation()


        # checks the bools to see which key is being pressed and direction of movement
        if self.right:
            self.player.center_x += self.player_speed * delta_time
        if self.left:
            self.player.center_x -= self.player_speed * delta_time
        if self.up:
            self.player.center_y += self.player_speed * delta_time
        if self.down:
            self.player.center_y -= self.player_speed * delta_time
            
    def on_key_press(self, symbol, modifiers):
        # sets animation refresh to faster rate for more noticeable movement
        self.player.texture_change_frames = 5

        # checks for arrow key press, runs animation of walking
        if symbol == arcade.key.RIGHT:
            self.right = True
            self.move_right()
        if symbol == arcade.key.LEFT:
            self.left = True
            self.move_left()
        if symbol == arcade.key.UP:
            self.up = True
            self.move_up()
        if symbol == arcade.key.DOWN:
            self.down = True
            self.move_down()
    
    def on_key_release(self, symbol, modifiers):
        # sets animation to lower refresh rate
        self.player.texture_change_frames = 30

        # sets key bools back to false after key release, starts standing animation
        if symbol == arcade.key.RIGHT:
            self.right = False
            self.face_right()
        if symbol == arcade.key.LEFT:
            self.left = False
            self.face_left() 
        if symbol == arcade.key.UP:
            self.up = False
            self.face_up()
        if symbol == arcade.key.DOWN:
            self.down = False
            self.face_forward() 


myGameWindow(800,800,"Sprite Test")
arcade.run()