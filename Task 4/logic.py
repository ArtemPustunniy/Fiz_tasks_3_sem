import math


class Body:
    def __init__(self, mass, velocity_x, velocity_y, x, y, radius=0.5):
        self.mass = mass
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.x = x
        self.y = y
        self.radius = radius

    def update_position(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt


def collision_with_wall(body, box_width, box_height):
    if body.x - body.radius < 0:
        body.x = body.radius
        body.velocity_x *= -1
    elif body.x + body.radius > box_width:
        body.x = box_width - body.radius
        body.velocity_x *= -1

    if body.y - body.radius < 0:
        body.y = body.radius
        body.velocity_y *= -1
    elif body.y + body.radius > box_height:
        body.y = box_height - body.radius
        body.velocity_y *= -1


def elastic_collision(body1, body2):
    dx = body1.x - body2.x
    dy = body1.y - body2.y
    dist = math.hypot(dx, dy)

    if dist <= body1.radius + body2.radius:
        nx = dx / dist
        ny = dy / dist

        dvx = body1.velocity_x - body2.velocity_x
        dvy = body1.velocity_y - body2.velocity_y
        velocity_along_normal = dvx * nx + dvy * ny

        if velocity_along_normal > 0:
            return

        impulse = (2 * velocity_along_normal) / (body1.mass + body2.mass)

        body1.velocity_x -= impulse * body2.mass * nx
        body1.velocity_y -= impulse * body2.mass * ny
        body2.velocity_x += impulse * body1.mass * nx
        body2.velocity_y += impulse * body1.mass * ny
