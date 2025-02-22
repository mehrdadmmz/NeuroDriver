import math
from hud import Hud
from car import Car
import random
import time
from pyglet.sprite import Sprite
from pyglet.graphics import Batch
from pyglet import image
from pyglet.window import key
from pyglet.window import Window
from pyglet.shapes import Circle
from pyglet.text import Label
# pyglet uses batches to optimize rendering process
# display positioned, scaled and rotated images.


# create a canvas to draw on
class Canvas(Window):
    frame_duration = 1 / 60  # class var: 60 times per sec

    def __init__(self, track, car_image_paths):
        super().__init__(width=960, height=540, caption='Car Game')
        self.track = track
        self.is_simulating = True
        # we keep adding elements to the batches --> first we added Sprite down below
        self.background_batch = Batch()
        self.car_batch = Batch()
        self.overlay_batch = Batch()
        self.track_image_sprite = Sprite(track.track_image, batch=self.background_batch)
        self.track_overlay_sprite = Sprite(track.track_overlay_image, batch=self.overlay_batch)
        self.car_images = [image.load(c) for c in car_image_paths]
        self.checkpoint_spirits = []
        # each checkpoint will be a tuple of a circle and label, we will draw them on the screen
        for i, checkpoint in enumerate(track.checkpoints):
            self.checkpoint_spirits.append((Circle(checkpoint[0], checkpoint[1], 15, color=(255, 255, 255, 100), batch=self.background_batch),
                                           Label(str(i), x=checkpoint[0], y=checkpoint[1], anchor_x="center", anchor_y="center", color=(255, 255, 255, 255), batch=self.background_batch)))

    def simulate_generation(self, networks, simulation_round):
        # since I only have room for visualizing one network, I will update the nodes with the first car network
        self.hud = Hud(simulation_round, networks[0].dimensions, self.overlay_batch)
        self.car_sprites = []
        for network in networks:  # create a car for each network in the list
            self.car_sprites.append(Car(network, self.track, random.choice(self.car_images), self.car_batch))
        self.population_total = len(self.car_sprites)
        self.population_alive = self.population_total
        last_time = time.perf_counter()
        while self.is_simulating and self.population_alive > 0:
            # time passed since the last frame, will pass it to all update functions to get smooth animations w/o lags
            elapsed_time = time.perf_counter() - last_time
            if elapsed_time > self.frame_duration:
                last_time = time.perf_counter()
                self.dispatch_events()
                self.update(elapsed_time)
                self.draw()

        for car in self.car_sprites:
            car.network.highest_checkpoint = car.last_checkpoint_passed
            if car.last_checkpoint_passed == len(self.track.checkpoints) - 1:  # if the car has reached the goal
                car.network.has_reached_goal = True

    def update(self, delta_time):
        for car_sprite in self.car_sprites:
            car_sprite.update(delta_time)
            if car_sprite.is_running:
                if not self.track.is_road(car_sprite.body.x, car_sprite.body.y):
                    car_sprite.shut_off()
                self.check_checkpoints(car_sprite, self.track.checkpoints)

        running_cars = [c for c in self.car_sprites if c.is_running]
        self.population_alive = len(running_cars)
        if self.population_alive > 0:
            self.hud.update(running_cars[0].network,
                            self.population_alive,
                            self.population_total,
                            running_cars[0].speed)  # speed of the first car alive

    def draw(self):
        self.clear()
        self.background_batch.draw()
        self.car_batch.draw()
        self.overlay_batch.draw()
        self.flip()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.is_simulating = False
            print("Simulation aborted.")

    # checking which checkpoints have been passed by the car. Loop through all checkpoints and calculate the distance
    # between the center of the car and the center of the checkpoint.
    def check_checkpoints(self, car_sprite, checkpoints):
        for i, checkpoint in enumerate(checkpoints):
            length = math.sqrt((checkpoint[0] - car_sprite.body.x) ** 2 +
                               (checkpoint[1] - car_sprite.body.y) ** 2)
            if length < 40:
                car_sprite.hit_checkpoint(i)
