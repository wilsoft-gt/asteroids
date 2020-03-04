"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others

This program implements the asteroids game.
"""
from abc import ABC
from abc import abstractmethod
import arcade
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Velocity:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

class MovingObject(ABC):
    def __init__(self, centerX, centerY, velocityX, velocityY, lives, angle, radius):
        self.center = Point(centerY, centerY)
        self.velocity = Velocity(velocityX, velocityY)
        self.alive = True
        self.lives = lives
        self.radius = radius
        self.angle = angle

    @abstractmethod
    def draw(self):
        print("You need to implement this on your class")
    
    @abstractmethod
    def advance(self):
        print("You need to define the speed on your class")

    @abstractmethod
    def rotate(self):
        print("You need to setup the rotation in your class")

    def touchingEdges(self):
        if self.center.x >= SCREEN_WIDTH:
            self.center.x = 1

        if self.center.x <= 0:
            self.center.x = SCREEN_WIDTH

        if self.center.y >= SCREEN_HEIGHT:
            self.center.y = 1
            
        if self.center.y <= 0:
            self.center.y = SCREEN_HEIGHT

    def hit(self):
        self.alive = False


class LargeAsteroid(MovingObject):
    def __init__(self, center_x, center_y, velocity_x, velocity_y, lives, angle, radius):
        super().__init__(center_x, center_y, velocity_x, velocity_y, lives, angle, radius)
    

    def draw(self):
        large = arcade.load_texture("resources/images/meteorGrey_big1.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, 50, 50, large, self.angle)

    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def rotate(self):
        self.angle += 1
    def generate(self):
        pass

class Ship(MovingObject):
    def __init__(self, center_x, center_y, velocity_x, velocity_y, lives, angle, radius):
        super().__init__(center_x, center_y, velocity_x, velocity_y, lives, angle, radius)

    def draw(self):
        ship = arcade.load_texture("resources/images/playerSHip1_orange.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, 50, 50, ship, self.angle)

class SmallAsteroid(MovingObject):
    pass

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction

    This class will then call the appropriate functions of
    each of the above classes.

    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        self.Asteroid1 = LargeAsteroid(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), 3, 0, BIG_ROCK_RADIUS)
        self.Asteroid2 = LargeAsteroid(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), 3, 0, BIG_ROCK_RADIUS)
        self.Asteroid3 = LargeAsteroid(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), 3, 0, BIG_ROCK_RADIUS)
        self.Asteroid4 = LargeAsteroid(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), 3, 0, BIG_ROCK_RADIUS)
        self.Asteroid5 = LargeAsteroid(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED), 3, 0, BIG_ROCK_RADIUS)

        self.asteroid_array = [self.Asteroid1, self.Asteroid2, self.Asteroid3, self.Asteroid4, self.Asteroid5]
        
        # TODO: declare anything here you need the game class to track

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        for asteroid in self.asteroid_array:
            asteroid.draw()
        # TODO: draw each object

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        for asteroid in self.asteroid_array:
            asteroid.advance()
            asteroid.rotate()
            asteroid.touchingEdges()

        # TODO: Tell everything to advance or move forward one step in time

        # TODO: Check for collisions

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            pass

        if arcade.key.RIGHT in self.held_keys:
            pass

        if arcade.key.UP in self.held_keys:
            pass

        if arcade.key.DOWN in self.held_keys:
            pass

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                pass

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()