from pyglet.window import Window
from pyglet.window import key
from pyglet import image
from pyglet.graphics import Batch  # pyglet uses batches to optimize rendering process
from pyglet.sprite import Sprite  # display positioned, scaled and rotated images.
import time
import random
from car import Car


# create a canvas to draw on
class Canvas(Window):
    frame_duration = 1 / 60  # class var: 60 times per sec

    def __init__(self, track, car_image_paths):
        super().__init__(width=960, height=540, caption='Car Game')
        self.track = track
        self.is_simulating = True
        self.background_batch = Batch()  # we keep adding elements to the batches --> first we added Sprite down below
        self.car_batch = Batch()
        self.track_image_sprite = Sprite(track.track_image, batch=self.background_batch)
        self.car_images = [image.load(c) for c in car_image_paths]

    def simulate_generation(self, networks):
        self.car_sprites = []
        for network in networks: # create a car for each network in the list
            self.car_sprites.append(Car(network, random.choice(self.car_images), self.car_batch))
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

    def update(self, delta_time):
        for car_sprite in self.car_sprites:
            car_sprite.update(delta_time)
            if car_sprite.is_running:
                if not self.track.is_road(car_sprite.body.x, car_sprite.body.y):
                    car_sprite.shut_off()
        running_cars = [c for c in self.car_sprites if c.is_running]
        self.population_alive = len(running_cars)

    def draw(self):
        self.clear()
        self.background_batch.draw()
        self.car_batch.draw()
        self.flip()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.is_simulating = False
            print("Simulation aborted.")
