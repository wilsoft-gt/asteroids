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
import math

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
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
    def __init__(self):
        self.x = 0
        self.y = 0

class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0

class MovingObject(ABC):
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.lives = 0
        self.radius = 0
        self.angle = 0

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
    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(0, SCREEN_WIDTH)
        self.center.y = random.uniform(0, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED)
        self.velocity.dy = random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED)
        self.lives = 3
        self.radius = BIG_ROCK_RADIUS
        self.angle = 0

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

class MediumAsteroid(MovingObject):
    #TODO complete this one
    pass

class SmallAsteroid(MovingObject):
    #TODO complete this one
    pass

class Ship(MovingObject):
    def __init__(self):
        super().__init__()
        self.center.x = SCREEN_WIDTH/2
        self.center.y = SCREEN_HEIGHT/2
        self.velocity.dx = 0
        self.velocity.dy = 0
        self.thrust = 0
        self.lives = 3
        self.radius = 50
        self.angle = 0

    def draw(self):
        ship = arcade.load_texture("resources/images/playerShip1_orange.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, 50, 50, ship, self.angle)

    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def rotate_left(self):
        self.angle += 3 

    def rotate_right(self):
        self.angle -= 3

    def acelerate(self):
        self.velocity.dx = -math.sin(math.radians(self.angle)) * self.thrust
        self.velocity.dy = +math.cos(math.radians(self.angle)) * self.thrust

    def decelerate(self):
        self.velocity.dx = +math.sin(math.radians(self.angle)) * self.thrust
        self.velocity.dy = -math.cos(math.radians(self.angle)) * self.thrust

    def increaseThrust(self):
        if self.thrust < 5:
            self.thrust += 0.25
        else:
            self.thrust = 5.0

    def decreaseThrust(self):
        if self.thrust > 0.0:
            self.thrust -= 0.25
        else:
            self.thrust = 0.0
    
    def rotate(self):
        return True

class Bullet(MovingObject):
    def __init__(self, ship_angle, ship_x, ship_y):
        super().__init__()
        self.center.x = ship_x
        self.center.y = ship_y
        self.angle = ship_angle -90
        self.time = 60

    def draw(self):
        bullet = arcade.load_texture('resources/images/laserBlue01.png')
        arcade.draw_texture_rectangle(self.center.x, self.center.y,25,10, bullet, self.angle)
    
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def fire(self):
        self.velocity.dx = -math.sin(math.radians(self.angle+90)) * BULLET_SPEED
        self.velocity.dy = +math.cos(math.radians(self.angle+90)) * BULLET_SPEED
    
    def rotate(self):
        pass

    def times(self):
        if self.time > 0:
            self.time -= 1
        else:
            self.alive = False



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

        
        # TODO: declare anything here you need the game class to track
        self.ship = Ship()
        self.asteroid_array = []
        self.bullets_list = []
        self.create_asteroids()

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        self.ship.draw()
        for asteroid in self.asteroid_array:
            asteroid.draw()

        for bullet in self.bullets_list:
            bullet.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.ship.advance()
        self.ship.touchingEdges()
        for asteroid in self.asteroid_array:
            asteroid.advance()
            asteroid.rotate()
            asteroid.touchingEdges()

        for bullet in self.bullets_list:
            bullet.advance()
            bullet.fire()
            bullet.times()
            bullet.touchingEdges()
            if bullet.alive == False:
                self.bullets_list.remove(bullet)
        print("DX: {} - DY: {}".format(self.ship.velocity.dx, self.ship.velocity.dy))
        # TODO: Tell everything to advance or move forward one step in time

        # TODO: Check for collisions

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate_left()
            
        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate_right()
            
        if arcade.key.UP in self.held_keys:
            self.ship.increaseThrust()
            self.ship.acelerate()
                        
        if arcade.key.DOWN in self.held_keys:
            self.ship.increaseThrust()
            self.ship.decelerate()
            was_up = False

        if arcade.key.DOWN not in self.held_keys and arcade.key.UP not in self.held_keys:
            self.ship.decreaseThrust()
            self.ship.decelerate()
            self.ship.acelerate()

            

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
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
                self.bullets_list.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """

        if key in self.held_keys:
            self.held_keys.remove(key)

    def create_asteroids(self):
        Asteroid1 = LargeAsteroid()
        self.asteroid_array.append(Asteroid1)
        Asteroid2 = LargeAsteroid()
        self.asteroid_array.append(Asteroid2)
        Asteroid3 = LargeAsteroid()
        self.asteroid_array.append(Asteroid3)
        Asteroid4 = LargeAsteroid()
        self.asteroid_array.append(Asteroid4)
        Asteroid5 = LargeAsteroid()
        self.asteroid_array.append(Asteroid5)

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()