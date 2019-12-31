import arcade

LAVA = arcade.load_texture("lava.png")

arcade.open_window(250, 250, "TEST")
arcade.start_render()

blocks = [(1, 0, 0, 0, 0), (1, 1, 0, 0, 0), (0, 1, 0, 0, 0), (0, 1, 1, 0, 0), (0, 0, 1, 0, 0)]
for x in range(len(blocks)):
    for y in range(len(blocks)):
        if blocks[x][y] == 0:
            arcade.draw_texture_rectangle(x * 50 + 25, y * 50 + 25, 50, 50, LAVA)

arcade.finish_render()
arcade.run()
