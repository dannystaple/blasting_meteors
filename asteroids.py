from random import randint
from pygame import Vector2

HEIGHT = 600
WIDTH = 1000

spaceship = Actor('spaceship.gif')
spaceship.speed = Vector2(0, 0)

rocket = Actor('fireball')
rocket.engine_radius = spaceship.height // 2 + rocket.height // 2

score = 0

asteroid = Actor("asteroid.png")
bullets = []
starfield = []

playing = True

speed_scale = 3

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


def update_rocket_flare():
    rocket_rel = Vector2()
    rocket_rel.from_polar((rocket.engine_radius, 270 - spaceship.angle))
    rocket.angle = spaceship.angle + 90
    rocket.center = (spaceship.center[0] + rocket_rel.x, spaceship.center[1] + rocket_rel.y)


def starting_positions():
    """Reset all game assets"""
    global playing, bullets, asteroid, rocket, spaceship, score
    score = 0
    bullets = []
    spaceship.image = "spaceship.gif"
    spaceship.speed = Vector2(0, 0)
    spaceship.angle = 180
    spaceship.x = WIDTH // 2
    spaceship.y = HEIGHT // 2
    update_rocket_flare()
    prepare_asteroid()
    playing = True


class Star:
    __slots__ = ['x', 'y', 'speed', 'brightness']

class Bullet(Actor):
    def update(self):
        """Update the bullet. Return true if it hit"""
        global score
        self.x += self.speed.x
        self.y += self.speed.y
        if asteroid and self.colliderect(asteroid):
            sounds.blast.play()
            prepare_asteroid()
            score += 1
            return True
        if self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0:
            return True


def prepare_starfield():
    for n in range(200):
        star = Star()
        star.x = randint(0, WIDTH)
        star.y = randint(0, HEIGHT)
        star.speed = randint(1, 8)
        star.brightness = 90 + star.speed * 20
        starfield.append(star)


def update():
    global playing, asteroid
    if playing:
        spaceship.x = (spaceship.x + spaceship.speed.x) % WIDTH
        spaceship.y = (spaceship.y + spaceship.speed.y) % HEIGHT

        if keyboard.left:
            spaceship.angle += 20
        elif keyboard.right:
            spaceship.angle -= 20
        if keyboard.up:
            new_speed = Vector2()
            new_speed.from_polar((speed_scale, 90 - spaceship.angle))
            spaceship.speed += new_speed
            update_rocket_flare()
            if spaceship.speed.length_squared() > (speed_scale * 3) ** 2:
                spaceship.speed.scale_to_length(speed_scale * 3)
            sounds.thrust.play()

    for star in starfield:
        star_vec = spaceship.speed * -star.speed * 0.2
        star.x = int(star.x + star_vec.x) % WIDTH
        star.y = int(star.y + star_vec.y) % HEIGHT

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
        if asteroid.colliderect(spaceship):
            spaceship.image = "crashed_spaceship.gif"
            sounds.bomb.play()
            playing = False
    for bullet in bullets:
        hit = bullet.update()
        if hit:
            bullets.remove(bullet)


def draw():
    """Redraw the screen."""
    screen.fill((0,0,0))
    for star in starfield:
        screen.draw.filled_circle((star.x, star.y), 1, (star.brightness, star.brightness, star.brightness))

    spaceship.draw()

    if keyboard.up:
        rocket.draw()
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
            new_bullet = Bullet('bullet')
            new_bullet.speed = Vector2()
            new_bullet.speed.from_polar((5 * speed_scale, 90 - spaceship.angle))
            new_bullet.pos = spaceship.pos + new_bullet.speed
            music.play_once("laser5")
            bullets.append(new_bullet)

starting_positions()
prepare_starfield()