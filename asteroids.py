import random
HEIGHT = 600
WIDTH = 1000

spaceship = Actor('spaceship.gif')
spaceship.x = WIDTH // 2
spaceship.y = HEIGHT - 20
spaceship.angle = 180

spaceship.x_increment = 0
spaceship.y_increment = 0
spaceship.fire_direction = (0, -5)
spaceship.fire_location = lambda: spaceship.midtop
score = 0

asteroid = Actor("asteroid.png")

def prepare_asteroid():
    global asteroid
    if random.randint(0, 1) >= 1:
        asteroid.x = random.randint(int(spaceship.right) + 50, WIDTH - 20)
    else:
        asteroid.x = random.randint(20, int(spaceship.left) - 50)
    asteroid.bottom = random.randint(asteroid.height, HEIGHT-40)
    score_scale = (score) + 3
    asteroid.x_velocity = random.randint(-score_scale, score_scale)
    asteroid.y_velocity = random.randint(-score_scale, score_scale)

prepare_asteroid()
bullets = []

playing = True


speed_scale = 3


class Bullet(Actor):
    def update(self):
        """Update the bullet. Return true if it hit"""
        global score
        self.x += self.x_velocity * speed_scale
        self.y += self.y_velocity * speed_scale
        if asteroid and self.colliderect(asteroid):
            sounds.blast.play()
            prepare_asteroid()
            asteroid.x = random.randint(20, WIDTH - 20)
            asteroid.bottom = random.randint(asteroid.height, HEIGHT - 40)
            asteroid.x_velocity = random.randint(-4, 4)
            asteroid.y_velocity = random.randint(-4, 4)
            score += 1
            return True
        if self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0:
            return True


def update():
    global playing, asteroid
    if playing:
        spaceship.x = (spaceship.x + spaceship.x_increment * speed_scale) % WIDTH
        spaceship.y = (spaceship.y + spaceship.y_increment * speed_scale) % HEIGHT
        #
    if asteroid:
        asteroid.x += asteroid.x_velocity * speed_scale
        asteroid.y += asteroid.y_velocity * speed_scale
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
    spaceship.draw()
    if asteroid:
        asteroid.draw()
    if not playing:
        screen.draw.text('Game Over', (WIDTH/2, HEIGHT/2))
    screen.draw.text('Score: % s' % (score * 50), (20, 20))
    for bullet in bullets:
        bullet.draw()

def on_key_down(key):
    if not playing:
        return
    if key == keys.UP:
        spaceship.angle = 180
        spaceship.y_increment = -2
        spaceship.fire_direction = (0, -5)
        spaceship.fire_location = lambda: spaceship.midtop
    elif key == keys.DOWN:
        spaceship.angle = 0
        spaceship.y_increment = 2
        spaceship.fire_direction = (0, 5)
        spaceship.fire_location = lambda: spaceship.midbottom
    elif key == keys.RIGHT:
        spaceship.angle = 90
        spaceship.x_increment = 2
        spaceship.fire_direction = (5, 0)
        spaceship.fire_location = lambda: spaceship.midright
    elif key == keys.LEFT:
        spaceship.angle = 270
        spaceship.x_increment = -2
        spaceship.fire_direction = (-5, 0)
        spaceship.fire_location = lambda: spaceship.midleft
    elif key == keys.SPACE:
        if len(bullets) < 10:
            new_bullet = Bullet('bullet', spaceship.fire_location())
            new_bullet.x_velocity = spaceship.fire_direction[0]
            new_bullet.y_velocity = spaceship.fire_direction[1]
            music.play_once("laser5")
            bullets.append(new_bullet)


def on_key_up():
    spaceship.x_increment = 0
    spaceship.y_increment = 0