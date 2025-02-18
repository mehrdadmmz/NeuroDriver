import math
from pyglet.sprite import Sprite
from pyglet.shapes import Line
import network


class Radar:
    max_length_pixel = 200  # max length of the radar in pixels which is the length of the line

    def __init__(self, angle, batch):
        self.angle = angle
        # radar beam which is a line in the game window that will be drawn
        self.beam = Line(0, 0, 0, 0, color=(255, 255, 255), batch=batch)


class Car:
    max_speed = 6.0

    def __init__(self, network, track, image, batch):
        self.network = network
        self.track = track
        image.anchor_x = 25
        image.anchor_y = 25
        self.body = Sprite(image, batch=batch)
        self.body.x, self.body.y = track.checkpoints[0]
        # adding 5 radars to the car, each radar will be at a different angle from the car
        self.radars = Radar(-70, batch), Radar(-35, batch), Radar(0, batch), Radar(35, batch), Radar(70, batch)
        self.speed = 0.0
        self.rotation = 0.0  # starts at angle 0
        self.is_running = True

    def update(self, delta_time):
        # delta time should be around 1/60 th of a second, so we will ,multiply it by 60 to get a value around 1
        # we use render speed when I apply the steering position to the rotation
        render_speed = delta_time * 60
        self.speed -= 0.05  # friction to slow down the car

        if self.is_running:
            # get the distance of the car from the walls of the track using the radar sensors
            # divide by the max length of the radar to normalize the value between 0 and 1
            measurements = [self.probe(radar)/radar.max_length_pixel for radar in self.radars]

            # inputs in the feed_forward will be the radar sensors on the car
            acceleration, steer_position = self.network.feed_forward(measurements)

            if acceleration > 0:
                self.speed += 0.1

            if self.speed > self.max_speed:
                self.speed = self.max_speed

            # * by speed cuz faster car will rotate faster
            self.rotation -= steer_position * self.speed * render_speed

        else:  # engine is off
            self.speed -= 0.05 * self.speed

        if self.speed < 0:  # prevent speed from getting negative
            self.speed = 0.0
            self.shut_off()  # when cars come to a halt, turn off the engine as wel

        self.body.rotation = -self.rotation  # apply rotation to the car Sprite
        # to make the car respect its position while steering --> making the car move in the direction pointing at
        # force will be the speed of the car and angle will be the rotation
        self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation))
        self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation))

    # probe function will be used to get the distance of the car from the walls of the track using the radar sensors
    # it
    def probe(self, radar):
        probe_length = 0  # starts probing at the origin of the car
        # set the start and end points of the radar beam to the center of the car
        radar.beam.x = self.body.x
        radar.beam.y = self.body.y
        x2 = radar.beam.x  # this is the end point of the radar beam in the x-axis
        y2 = radar.beam.y  # this is the end point of the radar beam in the y-axis

        # starting a while loop to keep probing until the radar beam hits a wall or reaches the max length
        while probe_length < radar.max_length_pixel and self.track.is_road(x2, y2):
            probe_length += 1  # increment the probe length by 1 pixel
            # calculate the end point of the radar beam using the formula of a line
            x2 = self.body.x + probe_length * math.cos(math.radians(self.rotation + radar.angle))
            y2 = self.body.y + probe_length * math.sin(math.radians(self.rotation + radar.angle))
        # now the line end coordinate will be updated
        radar.beam.x2 = x2
        radar.beam.y2 = y2
        # return the probe length
        return probe_length

    def shut_off(self):
        self.is_running = False
        self.radars = None  # remove the radars from the car when the engine is off
