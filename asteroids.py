from random import randint
from pygame import Vector2

HEIGHT = 600
WIDTH = 1000

#sprite image names
spaceship_image_name = 'spaceships_004_100.png'
engine_wash_image_name = 'spaceeffects_001_100.png'
meteor_image_name = 'spacemeteors_001_100.png'
crashed_spaceship_image_name = "crashed_spaceship.gif"
bullet_image_name = 'spacemissiles_037.png'

laser_sound = sounds.lasersmall_003
thrust_sound = sounds.thrusterfire_002
bullet_hit_asteroid_sound = sounds.explosioncrunch_003
spaceship_crashed_sound = sounds.explosioncrunch_000

speed_scale = 1
turn_speed = 10

score = 0

asteroid = Actor(meteor_image_name)
bullets = []
starfield = []

playing = True
thrusting = False


class Player(Actor):
    def __init__(self) -> None:
        super().__init__(spaceship_image_name)
        self.starting_position()
        self.rocket = Actor(engine_wash_image_name)
        self.rocket.engine_radius = self.height // 2 + self.rocket.height // 2
        self.thrusting = False

    def starting_position(self):
        self.image = spaceship_image_name
        self.speed = Vector2(0, 0)
        self.angle = 180
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.thrusting = False

    def update_rocket_flare(self):
        rocket_rel = Vector2()
        rocket_rel.from_polar((self.rocket.engine_radius, 270 - self.angle))
        self.rocket.angle = self.angle
        self.rocket.center = (self.center[0] + rocket_rel.x, self.center[1] + rocket_rel.y)

    def draw(self):
        super().draw()
        if self.thrusting:
            self.rocket.draw()


spaceship = Player()


def prepare_asteroid():
    global asteroid
    if spaceship.left < WIDTH // 2:
        asteroid.x = randint(max(WIDTH // 2, int(spaceship.right) + 50), WIDTH - 20)
    else:
        asteroid.x = randint(20, min(int(spaceship.left) - 50, WIDTH // 2))
    asteroid.bottom = randint(asteroid.height, HEIGHT-40)
    score_scale = score + 3
    asteroid.speed = Vector2()
    asteroid.speed.from_polar((randint(1, score_scale * speed_scale), randint(1, 360)) )


def starting_positions():
    """Reset all game assets"""
    global playing, bullets, asteroid, spaceship, score
    score = 0
    bullets = []
    spaceship.starting_position()
    spaceship.update_rocket_flare()
    prepare_asteroid()
    playing = True


class Star:
    __slots__ = ['x', 'y', 'speed', 'brightness']

    def __init__(self):
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)
        self.speed = randint(1, 8)
        self.brightness = 90 + self.speed * 20
    
    def update(self, spaceship_speed):
        star_vec = spaceship_speed * -self.speed * 0.2
        self.x = int(self.x + star_vec.x) % WIDTH
        self.y = int(self.y + star_vec.y) % HEIGHT

    def draw(self, screen):
        screen.draw.filled_circle((self.x, self.y), 1, (self.brightness, self.brightness, self.brightness))


class Bullet(Actor):
    def update(self):
        """Update the bullet. Return true if it hit"""
        global score
        self.x += self.speed.x
        self.y += self.speed.y
        if asteroid and self.colliderect(asteroid):
            bullet_hit_asteroid_sound.play()
            prepare_asteroid()
            score += 1
            return True
        if self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0:
            return True


def prepare_starfield():
    for n in range(200):
        starfield.append(Star())


def update():
    global playing, asteroid, thrusting
    if playing:
        spaceship.x = (spaceship.x + spaceship.speed.x) % WIDTH
        spaceship.y = (spaceship.y + spaceship.speed.y) % HEIGHT

        if keyboard.left:
            spaceship.angle += turn_speed
        elif keyboard.right:
            spaceship.angle -= turn_speed
        if keyboard.up:
            new_speed = Vector2()
            new_speed.from_polar((speed_scale, 90 - spaceship.angle))
            spaceship.speed += new_speed
            spaceship.update_rocket_flare()
            if spaceship.speed.length_squared() > (speed_scale * 3) ** 2:
                spaceship.speed.scale_to_length(speed_scale * 3)
            if not thrusting:
                thrust_sound.play()
                spaceship.thrusting = True
                thrusting = True
        else:
            thrust_sound.stop()
            thrusting = False
            spaceship.thrusting = False

    for star in starfield:
        star.update(spaceship.speed)

    if asteroid:
        asteroid.x += asteroid.speed.x
        asteroid.y += asteroid.speed.y
        if asteroid.y > HEIGHT:
            asteroid.y -= HEIGHT
        if asteroid.y < 0:
            asteroid.y += HEIGHT
        if asteroid.x > WIDTH:
            asteroid.x -= WIDTH
        if asteroid.x < 0:
            asteroid.x += WIDTH
        if asteroid.colliderect(spaceship) and playing:
            spaceship.image = crashed_spaceship_image_name
            spaceship_crashed_sound.play()
            playing = False
            thrusting = False
            thrust_sound.stop()
    for bullet in bullets:
        hit = bullet.update()
        if hit:
            bullets.remove(bullet)


def draw():
    """Redraw the screen."""
    screen.fill((0,0,0))
    for star in starfield:
        star.draw(screen)

    spaceship.draw()

    if asteroid:
        asteroid.draw()
    if not playing:
        screen.draw.text('Game Over', (WIDTH/2, HEIGHT/2))
        screen.draw.text('Press Space To Play Again', (WIDTH/2, HEIGHT/2 + 40))

    screen.draw.text('Score: % s' % (score * 50), (20, 20))
    for bullet in bullets:
        bullet.draw()


def on_key_down(key):
    if not playing:
        if key == keys.SPACE:
            starting_positions()
        return
    elif key == keys.SPACE:
        if len(bullets) < 10:
            new_bullet = Bullet(bullet_image_name)
            new_bullet.speed = Vector2()
            new_bullet.speed.from_polar((5 * speed_scale, 90 - spaceship.angle))
            new_bullet.angle = spaceship.angle
            new_bullet.pos = spaceship.pos + new_bullet.speed
            laser_sound.play()
            bullets.append(new_bullet)

starting_positions()
prepare_starfield()
