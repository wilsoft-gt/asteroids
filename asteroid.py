import arcade

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_location(400, 200)

        arcade.set_background_color(arcade.color.BLACK_BEAN)



    def on_draw(self):
        arcade.start_render()
        textureImg = arcade.load_texture("resources/images/unnamed.png")
        arcade.draw_texture_rectangle(center_x=200, center_y=200, width=40, height=40, texture=textureImg, alpha=255)
        arcade.Sprite('resources/images/unnamed.png')
MyGame(800, 500, "It is working!")
arcade.run()