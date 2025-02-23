# from pyglet.sprite import Sprite
# from pyglet.shapes import Line
# import math
#
#
# class Radar:
#     # max length of the radar in pixels which is the length of the line
#     max_length_pixels = 200
#
#     def __init__(self, angle, batch):
#         self.angle = angle
#         # radar beam which is a line in the game window that will be drawn
#         self.beam = Line(0, 0, 0, 0, color=(255, 255, 255, 127), batch=batch)
#
#
# class Car:
#     max_speed = 6.0
#     slipping_speed = max_speed * 0.75  # if the speed gets over the slipping speed, I will decrease the steering impact
#
#     def __init__(self, network, track, image, batch):
#         self.network = network
#         self.track = track
#         image.anchor_x = 25
#         image.anchor_y = 25
#         self.body = Sprite(image, batch=batch)
#         self.body.x, self.body.y = track.checkpoints[0]
#         # adding 5 radars to the car, each radar will be at a different angle from the car
#         self.radars = (
#             Radar(-70, batch),
#             Radar(-35, batch),
#             Radar(0, batch),
#             Radar(35, batch),
#             Radar(70, batch)
#         )
#         self.speed = 0.0
#         self.rotation = 0.0  # starts at angle 0
#         self.is_running = True
#         self.last_checkpoint_passed = 0  # set the first checkpoint as 0 that will be the starting point of the track
#         self.smallest_edge_distance = 100  # the smallest distance from the car to the edge of the track 100 pixels
#
#     def update(self, delta_time):
#         # delta time should be around 1/60th of a second, so we will multiply it by 60 to get a value around 1
#         # we use render_speed when I apply the steering position to the rotation
#         render_speed = delta_time * 60
#         self.speed -= 0.05  # friction to slow down the car
#         if self.is_running:
#             # get the distance of the car from the walls of the track using the radar sensors
#             # divide by the max length of the radar to normalize the value between 0 and 1
#             measurements = [self.probe(radar) / radar.max_length_pixels for radar in self.radars]
#             # inputs in the feed_forward will be the radar sensors on the car
#             acceleration, steer_position = self.network.feed_forward(measurements)
#
#             if acceleration > 0:
#                 self.speed += 0.1
#
#             if self.speed > self.max_speed:
#                 self.speed = self.max_speed
#
#             # if the speed gets over the slipping speed, I will decrease the steering impact.
#             # {x < t: 1, -x / m + t / m + 1}
#             # TODO: check the formula, as of now both are kinda similar, the commented one is non-quadratic
#             """if self.speed > self.slipping_speed:
#                 steer_impact = -self.speed / self.max_speed + self.slipping_speed / self.max_speed + 1
#             else:
#                 steer_impact = 1"""
#             if self.speed > self.slipping_speed:
#                 factor = (self.speed - self.slipping_speed) / (self.max_speed - self.slipping_speed)
#                 steer_impact = max(0.5, 1 - factor ** 2)
#             else:
#                 steer_impact = 1
#
#             # * by speed cuz faster car will rotate faster
#             # I multiply the steer position by 3 to make the car steer faster. I know that the second output of the
#             # network is the steering position, and it ranges from -1 to 1, so I multiply it by 3 to make the car steer
#             # faster.
#             # with the steering impact applied, cars will have more problems steering at high speeds
#             self.rotation -= steer_position * self.speed * steer_impact * render_speed * 3
#         else:  # engine is off
#             self.speed -= 0.05 * self.speed
#
#         if self.speed < 0:  # prevent speed from getting negative
#             self.speed = 0.0
#             self.shut_off()  # when cars come to a halt, turn off the engine as well
#
#         self.body.rotation = -self.rotation  # apply rotation to the car Sprite
#         # to make the car respect its position while steering --> making the car move in the direction pointing at
#         # force will be the speed of the car and angle will be the rotation
#         self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation))
#         self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation))
#
#     # probe function will be used to get the distance of the car from the walls of the track using the radar sensors
#     def probe(self, radar):
#         probe_length = 0  # starts probing at the origin of the car
#         # set the start and end points of the radar beam to the center of the car
#         radar.beam.x = self.body.x
#         radar.beam.y = self.body.y
#         x2 = radar.beam.x  # this is the end point of the radar beam in the x-axis
#         y2 = radar.beam.y  # this is the end point of the radar beam in the y-axis
#
#         # starting a while loop to keep probing until the radar beam hits a wall or reaches the max length
#         while probe_length < radar.max_length_pixels and self.track.is_road(x2, y2):
#             probe_length += 2  # increment the probe length by 2 pixels
#             # calculate the end point of the radar beam using the formula of a line
#             x2 = self.body.x + probe_length * math.cos(math.radians(self.rotation + radar.angle))
#             y2 = self.body.y + probe_length * math.sin(math.radians(self.rotation + radar.angle))
#         # now the line end coordinate will be updated
#         radar.beam.x2 = x2
#         radar.beam.y2 = y2
#         if probe_length < self.smallest_edge_distance:
#             self.smallest_edge_distance = probe_length
#         return probe_length
#
#     def hit_checkpoint(self, id):
#         if id - self.last_checkpoint_passed == 1:  # if the car passes the checkpoints in order
#             self.last_checkpoint_passed = id  # update the last checkpoint passed
#         elif id < self.last_checkpoint_passed:  # driving in the wrong direction
#             self.shut_off()
#
#     def shut_off(self):
#         self.is_running = False
#         self.radars = None  # remove the radars from the car when the engine is off
#
from pyglet.sprite import Sprite
from pyglet.shapes import Line
import math


class Radar:
    max_length_pixels = 200

    def __init__(self, angle, batch):
        self.angle = angle
        self.beam = Line(0, 0, 0, 0, color=(255, 255, 255, 127), batch=batch)


class Car:
    max_speed = 6.0
    slipping_speed = max_speed * 0.75

    def __init__(self, network, track, image, batch):
        self.network = network
        self.track = track
        image.anchor_x = 25
        image.anchor_y = 25
        self.body = Sprite(image, batch=batch)
        self.body.x, self.body.y = track.checkpoints[0]
        self.radars = Radar(-70, batch), Radar(-35, batch), Radar(0, batch), Radar(35, batch), Radar(70, batch)
        self.speed = 0.0
        self.rotation = 0.0
        self.is_running = True
        self.last_checkpoint_passed = 0
        self.smallest_edge_distance = 100  # pixels

    def update(self, delta_time):
        render_speed = delta_time * 60
        self.speed -= 0.05  # friction
        if self.is_running:
            measurements = [self.probe(radar) / radar.max_length_pixels for radar in self.radars]
            acceleration, steer_position = self.network.feed_forward(measurements)

            if acceleration > 0:
                self.speed += 0.1

            if self.speed > self.max_speed:
                self.speed = self.max_speed

            if self.speed > self.slipping_speed:
                steer_impact = -self.speed / self.max_speed + self.slipping_speed / self.max_speed + 1
            else:
                steer_impact = 1

            self.rotation -= steer_position * self.speed * steer_impact * render_speed * 3
        else:  # engine is off
            self.speed -= 0.05 * self.speed

        if self.speed < 0:
            self.speed = 0.0
            self.shut_off()

        self.body.rotation = -self.rotation
        self.body.x += self.speed * render_speed * math.cos(math.radians(self.rotation))
        self.body.y += self.speed * render_speed * math.sin(math.radians(self.rotation))

    def probe(self, radar):
        probe_length = 0
        radar.beam.x = self.body.x
        radar.beam.y = self.body.y
        x2 = radar.beam.x
        y2 = radar.beam.y
        while probe_length < radar.max_length_pixels and self.track.is_road(x2, y2):
            probe_length += 2  # pixels
            x2 = self.body.x + probe_length * math.cos(math.radians(self.rotation + radar.angle))
            y2 = self.body.y + probe_length * math.sin(math.radians(self.rotation + radar.angle))
        radar.beam.x2 = x2
        radar.beam.y2 = y2
        if probe_length < self.smallest_edge_distance:
            self.smallest_edge_distance = probe_length
        return probe_length

    def hit_checkpoint(self, id):
        if id - self.last_checkpoint_passed == 1:
            self.last_checkpoint_passed = id
        elif id < self.last_checkpoint_passed:  # driving in the wrong direction or finish
            self.shut_off()

    def shut_off(self):
        self.is_running = False
        self.radars = None
