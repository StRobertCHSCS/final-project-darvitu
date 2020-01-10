import arcade
from blocks import Blocks


class TileMap:
    def __init__(self, width, height, x, y):
        self.WINDOW_WIDTH = width
        self.WINDOW_HEIGHT = height
        self.x = x
        self.y = y

    def read_map(self):
        self.map = [line.split(' ') for line in open("../Maps/tilemap.txt", 'r').readlines()]

    def draw_map(self):
        for y in range(15):
            for x in range(25):
                if self.map[y][x] == '1':
                    arcade.draw_texture_rectangle(x * 50 + 25, 750 - (50 * y) - 25, 50, 50, Blocks.LAVA)
                elif self.map[y][x] == '2':
                    arcade.draw_texture_rectangle(x * 50 + 25, 750 - (50 * y) - 25, 50, 50, Blocks.LEAVES)
                elif self.map[y][x] == '3':
                    arcade.draw_texture_rectangle(x * 50 + 25, 750 - (50 * y) - 25, 50, 50, Blocks.YELLOW_PATH)
                elif self.map[y][x] == '4':
                    arcade.draw_texture_rectangle(x * 50 + 25, 750 - (50 * y) - 25, 50, 50, Blocks.COBBLESTONE)
                elif self.map[y][x] == '5':
                    arcade.draw_texture_rectangle(x * 50 + 25, 750 - (50 * y) - 25, 50, 50, Blocks.WALL)
                else:
                    pass


arcade.open_window(1250, 750, "TileMap")
arcade.start_render()
map = TileMap(1250, 750, 0, 0)
map.read_map()
map.draw_map()
arcade.finish_render()
arcade.run()
