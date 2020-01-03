import arcade

class myGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)

        self.player_list = None
        self.player = None

        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedTimeSprite()
        self.player.texture_change_frames = 20
        self.player.textures = []

        for i in range(3):
            self.player.textures.append(arcade.load_texture("images/test_sprite_sheet.png",x=i*96,y=0,width=96,height=104))
        
        self.player.center_x = 1280 // 2
        self.player.center_y = 720 // 2 

        self.player_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update_animation()
            
    def on_key_press(self, symbol, modifiers):
        pass
    
    def on_key_release(self, symbol, modifiers):
        pass


myGameWindow(1280,720,"Sprite Test")
arcade.run()