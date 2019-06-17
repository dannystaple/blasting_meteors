from pygame import Vector2

WIDTH = 800
HEIGHT = 800

player = Actor("spaceship")
player.speed = Vector2(0, 0)
player.x = WIDTH // 2
player.y = HEIGHT // 2

fireball = Actor('fireball')
fireball_radius = player.height // 2 + fireball.height // 2

def draw():
    screen.fill((0, 0, 0))
    player.draw()
    if keyboard.up:
        fireball.draw()

def update():
    player.x = (player.x + player.speed.x) % WIDTH
    player.y = (player.y + player.speed.y) % HEIGHT

    if keyboard.left:
        player.angle += 20
    elif keyboard.right:
        player.angle -= 20
    if keyboard.up:
        new_speed = Vector2()
        new_speed.from_polar((1, 90 - player.angle))
        player.speed += new_speed

    fireball_rel = Vector2()
    fireball_rel.from_polar((fireball_radius, 270 - player.angle))
    fireball.angle = player.angle + 90
    fireball.center = (player.center[0] + fireball_rel.x, player.center[1] + fireball_rel.y)
