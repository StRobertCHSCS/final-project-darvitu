import arcade

from blocks import Blocks

arcade.open_window(1250, 750, "Darvuti")
arcade.start_render()
arcade.draw_texture_rectangle(25,25,50,50,Blocks.LAVA)
arcade.draw_texture_rectangle(75,25,50,50,Blocks.COBBLESTONE)
arcade.draw_texture_rectangle(125,25,50,50,Blocks.YELLOW_PATH)
arcade.draw_texture_rectangle(175,25,50,50,Blocks.LEAVES)
arcade.draw_texture_rectangle(225,25,50,50,Blocks.TREE)
arcade.finish_render()
arcade.run()