import arcade
class myGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)


        
    def setup(self):
        


myGameWindow(800,800,"Start screen test")
arcade.run()