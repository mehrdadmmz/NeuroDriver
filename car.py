import math
from pyglet.sprite import Sprite
import network

class Car:
    max_speed = 6.0

    def __init__(self, network, image, batch):
        self.network = network
        image.anchor_x = 25
        image.anchor_y = 25
        self.body = Sprite(image, batch=batch)
        self.body.x, self.body.y = 480, 260
        self.speed = 0.0
        self.rotation = 0.0  # starts at angle 0
        self.is_running = True

    def update(self, delta_time):
        # delta time should be around 1/60 th of a second, so we will ,multiply it by 60 to get a value around 1
        render_speed = delta_time * 60  # we use render speed when I apply the steering position to the rotation
        self.speed -= 0.05  # friction to slow down the car

        if self.is_running:
            acceleration, steer_position = self.network.feed_forward()

            if acceleration > 0:
                self.speed += 0.1

            if self.speed > self.max_speed:
                self.speed = self.max_speed

            self.rotation -= steer_position * self.speed * render_speed  # * by speed cuz faster car will rotate faster

        else:  # engine is off
            self.speed -= 0.05 * self.speed

        if self.speed < 0:  # prevent speed from getting negative
            self.speed = 0.0

        self.body.rotation = -self.rotation  # apply rotation to the car Sprite
        # to make the car respect its position while steering --> making the car move in the direction pointing at
        # force will be the speed of the car and angle will be the rotation
        self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation))
        self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation))

    def shut_off(self):
        self.is_running = False
