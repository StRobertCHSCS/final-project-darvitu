"""
-------------------------------------------------------------------------------
Name: test.py
Purpose: Code to test.

Author:	Wang.D

Created: 23/12/2020
-------------------------------------------------------------------------------
"""
import arcade

arcade.open_window(500,500, "WINDOW")
arcade.set_background_color(arcade.color.BLACK)
arcade.start_render()
arcade.draw_texture_rectangle(50,50, 40,40, arcade.load_texture("images/boss_bullet.png"))
arcade.finish_render()
arcade.run()