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
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 30

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 15

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 7


#define the position on the screen
class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

#defines the velocity in x or y direction
class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0

#common properties betwen sprites
class MovingObject(ABC):
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.radius = 0
        self.angle = 0

    @abstractmethod
    def draw(self):
        print("You need to implement this on your class")
    
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    @abstractmethod
    def rotate(self):
        print("You need to setup the rotation in your class")

    def touch_edge(self):
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

#defined large asteroid class
class LargeAsteroid(MovingObject):
    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(0, SCREEN_WIDTH)
        self.center.y = random.uniform(0, SCREEN_HEIGHT)
        self.velocity.dx = random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED)
        self.velocity.dy = random.uniform(-BIG_ROCK_SPEED, BIG_ROCK_SPEED)
        self.radius = BIG_ROCK_RADIUS * 2
        self.angle = 0
        self.large_texture = arcade.load_texture("resources/images/meteorGrey_big1.png")

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius, self.radius, self.large_texture, self.angle)

    def rotate(self):
        self.angle += BIG_ROCK_SPIN

#medium asteroid class
class MediumAsteroid(MovingObject):
    def __init__(self, asteroidCX, asteroidCY, asteroidVX, asteroidVY):
        super().__init__()
        self.center.x = asteroidCX
        self.center.y = asteroidCY
        self.velocity.dx = asteroidVX
        self.velocity.dy = asteroidVY
        self.radius = MEDIUM_ROCK_RADIUS * 2
        self.angle = 0
        self.medium_texture = arcade.load_texture("resources/images/meteorGrey_med1.png")

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius, self.radius, self.medium_texture, self.angle)

    def rotate(self):
        self.angle += MEDIUM_ROCK_SPIN

#small asteroid class
class SmallAsteroid(MovingObject):
    def __init__(self, asteroidCX, asteroidCY, asteroidVX, asteroidVY):
        super().__init__()
        self.center.x = asteroidCX
        self.center.y = asteroidCY
        self.velocity.dx = asteroidVX
        self.velocity.dy = asteroidVY
        self.radius = SMALL_ROCK_RADIUS * 2
        self.angle = 0
        self.small_texture = arcade.load_texture("resources/images/meteorGrey_small1.png")

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius, self.radius, self.small_texture, self.angle)

    def rotate(self):
        self.angle += SMALL_ROCK_SPIN

#ship class
class Ship(MovingObject):
    def __init__(self):
        super().__init__()
        self.center.x = SCREEN_WIDTH/2
        self.center.y = SCREEN_HEIGHT/2
        self.velocity.dx = 0
        self.velocity.dy = 0
        self.lives = 3
        self.radius = SHIP_RADIUS * 1.5
        self.angle = 0
        self.ship_texture = arcade.load_texture("resources/images/playerShip1_orange.png")

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.radius, self.radius, self.ship_texture, self.angle)

    def rotate_left(self):
        self.angle += 3 

    def rotate_right(self):
        self.angle -= 3

    #move forward
    def acelerate(self):
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    #move backuards
    def decelerate(self):
        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    #set a limit on the velocity
    def check_velocity(self):
        if self.velocity.dy > 20:
            self.velocity.dy = 20
        if self.velocity.dy < -20:
            self.velocity.dy = -20
        if self.velocity.dx > 20:
            self.velocity.dx = 20
        if self.velocity.dx < -20:
            self.velocity.dx = -20
    
    #this method is called when the ship colide with an asteroid
    def reduceLive(self):
        if self.lives == 0:
            self.alive = False
        elif self.lives > 0:
            self.lives -= 1

    def rotate(self):
        pass

    
#bullet class
class Bullet(MovingObject):
    def __init__(self, ship_angle, ship_x, ship_y):
        super().__init__()
        self.center.x = ship_x
        self.center.y = ship_y
        self.angle = ship_angle -90
        self.time = 10
        self.radius = BULLET_RADIUS

    def draw(self):
        bullet = arcade.load_texture('resources/images/laserBlue01.png')
        arcade.draw_texture_rectangle(self.center.x, self.center.y,25,10, bullet, self.angle)

    def fire(self):
        self.velocity.dx -= math.sin(math.radians(self.angle+90)) * BULLET_SPEED
        self.velocity.dy += math.cos(math.radians(self.angle+90)) * BULLET_SPEED
    
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
        self.large_asteroid_array = []
        self.medium_asteroid_array = []
        self.small_asteroid_array = []
        self.bullets_list = []
        self.create_large_asteroids()

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # TODO: draw each object
        #draw ship
        self.ship.draw()

        #draw large asteroids
        for asteroid in self.large_asteroid_array:
            asteroid.draw()

        #draw medium asteroids
        for med_asteroids in self.medium_asteroid_array:
            med_asteroids.draw()

        #draw small asteroids
        for sma_asteroids in self.small_asteroid_array:
            sma_asteroids.draw()

        #draw bullets
        for bullet in self.bullets_list:
            bullet.draw()

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """

        self.check_keys()
        
        #make the ship to move
        self.ship.advance()

        #reposition the ship if an edge is touched
        self.ship.touch_edge()

        #check for all the colisions

        #make all the sprites to move, rotate and check if edge is touched
        for asteroid in self.large_asteroid_array:
            asteroid.advance()
            asteroid.rotate()
            asteroid.touch_edge()

        for asteroid in self.medium_asteroid_array:
            asteroid.advance()
            asteroid.rotate()
            asteroid.touch_edge()

        for asteroid in self.small_asteroid_array:
            asteroid.advance()
            asteroid.rotate()
            asteroid.touch_edge()

        for bullet in self.bullets_list:
            bullet.advance()
            bullet.fire()
            bullet.times()
            bullet.touch_edge()
            if bullet.alive == False:
                self.bullets_list.remove(bullet)

        self.check_collisions()

    #check for collisions betwen asteroids and bullets and asteroids and the ship.
    def check_collisions(self):

        self.check_collition_with_bullet(self.large_asteroid_array, self.created_from_big_asteroids, "large")
        self.check_collition_with_bullet(self.medium_asteroid_array, self.created_from_medium_asteroids, "medium")
        self.check_collition_with_bullet(self.small_asteroid_array, None, "small")
        
        self.check_collition_with_ship(self.large_asteroid_array)
        self.check_collition_with_ship(self.medium_asteroid_array)
        self.check_collition_with_ship(self.small_asteroid_array)

        self.delete_dead_sprites(self.large_asteroid_array)
        self.delete_dead_sprites(self.medium_asteroid_array)
        self.delete_dead_sprites(self.small_asteroid_array)
        self.delete_dead_sprites(self.bullets_list)


    """
    Since basically all the item arrays share the same porperties
    I created this method in order to take advantage of polymorphism
    and avoid code repetition
    """ 
    def check_collition_with_bullet(self, list2, to_create, asteroid_type):
        for bullet in self.bullets_list:
            for item2 in list2:
                if bullet.alive and item2.alive:
                    too_close = (bullet.radius/2) + (item2.radius/2)
                    if (abs(bullet.center.x - item2.center.x) < too_close and abs(bullet.center.y - item2.center.y) < too_close):
                        if asteroid_type != "small":
                            to_create(item2.center.x, item2.center.y, item2.velocity.dx, item2.velocity.dy)
                        bullet.alive = False
                        item2.alive = False

    """
    Same of above but with the ship
    """
    def check_collition_with_ship(self, asteroid_list):
        for asteroid in asteroid_list:
            if asteroid.alive and self.ship.alive:
                too_close = (self.ship.radius/2) + (asteroid.radius/2)
                if (abs(self.ship.center.x - asteroid.center.x) < too_close and abs(self.ship.center.y - asteroid.center.y) < too_close):
                    asteroid.alive = False
                    self.ship.reduceLive()


    """
    Same here, using the power of polymorphism to 
    delete all the items using just one method
    """
    def delete_dead_sprites(self, object_array):
        for sprite in object_array:
            if not sprite.alive:
                object_array.remove(sprite)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.check_velocity()
            self.ship.rotate_left()
            
        if arcade.key.RIGHT in self.held_keys:
            self.ship.check_velocity()
            self.ship.rotate_right()
            
        if arcade.key.UP in self.held_keys:
            self.ship.check_velocity()
            self.ship.acelerate()
                        
        if arcade.key.DOWN in self.held_keys:
            self.ship.check_velocity()
            self.ship.decelerate()

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

            #stop the ship when the key is released
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.ship.velocity.dx = 0
                self.ship.velocity.dy = 0

    #generate the first 5 asteroids randomly on the screen
    def create_large_asteroids(self):
        Asteroid1 = LargeAsteroid()
        self.large_asteroid_array.append(Asteroid1)
        Asteroid2 = LargeAsteroid()
        self.large_asteroid_array.append(Asteroid2)
        Asteroid3 = LargeAsteroid()
        self.large_asteroid_array.append(Asteroid3)
        Asteroid4 = LargeAsteroid()
        self.large_asteroid_array.append(Asteroid4)
        Asteroid5 = LargeAsteroid()
        self.large_asteroid_array.append(Asteroid5)

    """this method is called when a large asteroid is hit by a bullet,
    this method creates the 3 asteroids, 2 medium and 1 small asteroid."""
    def created_from_big_asteroids(self, centerX, centerY, velocityX, velocityY):
        med_asteroid_1 = MediumAsteroid(centerX, centerY, velocityX, (velocityY+2))
        self.medium_asteroid_array.append(med_asteroid_1)
        med_asteroid_2 = MediumAsteroid(centerX, centerY, velocityX, (velocityY-2))
        self.medium_asteroid_array.append(med_asteroid_2)
        small_asteroid = SmallAsteroid(centerX, centerY, velocityX + 5, velocityY)
        self.small_asteroid_array.append(small_asteroid)

    """
    This method is called when a medium asteroid is hit by a bullet, 
    this one creates 2 small asteorids.
    """
    def created_from_medium_asteroids(self, centerX, centerY, velocityX, velocityY):
        sm_asteroid_1 = SmallAsteroid(centerX, centerY, velocityX+1.5, velocityY+1.5)
        sm_asteroid_2 = SmallAsteroid(centerX, centerY, velocityX-1.5, velocityY-1.5)
        self.small_asteroid_array.append(sm_asteroid_1)
        self.small_asteroid_array.append(sm_asteroid_2)
        


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()