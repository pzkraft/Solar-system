import pygame
import time

WIDTH = 1400
HEIGHT = 700
FPS = 200
G = 6.67430 / 10 ** 11  # gravitational constant
k = 1_000_000  # metres in one pixel at the start

# user's pov at the start
w_x = -600_000_000
w_y = -450_000_000

time_coef = 10_000  # time acceleration coefficient at the start

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 36)
text_FPS = font.render('FPS: ' + str(FPS), True, 'green')
text_time_coef = font.render('Time: x' + str(time_coef), True, 'green')


class AstroObject:
    def __init__(self, real_x, real_y, real_radius, mass, colour):
        self.real_x = real_x
        self.real_y = real_y
        self.real_r = real_radius
        self.mass = mass
        self.colour = colour
        self.speed = [0, 0]
        self.a = [0, 0]
        self.f = [0, 0]
        self.trace_count = 0
        self.trace = []
        self.status = True  # if astronomical object exists

    def update(self):
        self.a[0] = (self.f[0] / self.mass) * (time_coef ** 2) / FPS ** 2
        self.a[1] = (self.f[1] / self.mass) * (time_coef ** 2) / FPS ** 2

        self.speed[0] += self.a[0]
        self.speed[1] += self.a[1]

        self.real_x += self.speed[0]
        self.real_y += self.speed[1]

        # trajectory:
        self.trace_count += (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5
        if self.trace_count / k >= 5:
            self.trace_count = 0
            self.trace.append((self.real_x,
                               self.real_y))
        if len(self.trace) > 1000:
            self.trace.pop(0)

    def draw(self):
        pygame.draw.circle(screen,
                           self.colour,
                           ((self.real_x - w_x) / k,
                            (self.real_y - w_y) / k),
                           self.real_r / k
                           )
        for i in self.trace:
            pygame.draw.circle(screen,
                               self.colour,
                               ((i[0] - w_x) / k,
                                (i[1] - w_y) / k),
                               1)


astro_objects = []

# Earth:
Earth = AstroObject(0, 0, 6_371_000, 5.9722 * 10 ** 24, 'blue')
astro_objects.append(Earth)
astro_objects[-1].speed[1] += 29782.77 * time_coef / FPS

# Moon:
Moon = AstroObject(-363_104_000, 0, 1737100, 7.35 * 10 ** 22, 'grey')
astro_objects.append(Moon)
astro_objects[-1].speed[1] = 1080 * time_coef / FPS
astro_objects[-1].speed[1] += 29782.77 * time_coef / FPS

# International Space Station:
Iss = AstroObject(0, 6_371_000 + 415_000, 45, 440_075, 'yellow')
astro_objects.append(Iss)
astro_objects[-1].speed[0] = 7600 * time_coef / FPS
astro_objects[-1].speed[1] += 29782.77 * time_coef / FPS

# Venus:
Venus = AstroObject(42 * 10 ** 9, 0, 6_051_000, 4.867 * 10 ** 24, 'orange')
astro_objects.append(Venus)
astro_objects[-1].speed[1] = 35020 * time_coef / FPS

# Mercury:
Mercury = AstroObject(91 * 10 ** 9, 0, 2_439_000, 3.285 * 10 ** 23, 'red')
astro_objects.append(Mercury)
astro_objects[-1].speed[1] = 47360 * time_coef / FPS

# Mars
Mars = AstroObject(-78 * 10 ** 9, 0, 3_400_000, 6.39 * 10 ** 23, 'red')
astro_objects.append(Mars)
astro_objects[-1].speed[1] = 24130 * time_coef / FPS

# Jupiter
Jupiter = AstroObject(-628 * 10 ** 9, 0, 71_000_000, 1.898 * 10 ** 27, 'orange')
astro_objects.append(Jupiter)
astro_objects[-1].speed[1] = 13070 * time_coef / FPS

# Saturn
Saturn = AstroObject(-1276 * 10 ** 9, 0, 60_000_000, 5.683 * 10 ** 26, 'brown')
astro_objects.append(Saturn)
astro_objects[-1].speed[1] = 9690 * time_coef / FPS

# Sun
Sun = AstroObject(149.6 * 10 ** 9, 0, 696_000_000, 1.9891 * 10 ** 30, 'purple')
astro_objects.append(Sun)

print("Astronomical objects exist:", len(astro_objects))

tick = 0
tm = time.time()
running = True
while running:
    clock.tick(FPS)
    tick += 1
    if tick == 100:
        tick = 0
        text_FPS = font.render('FPS: ' + str(int((100 / (time.time() - tm)))), True,
                               'green')

        tm = time.time()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # place which user chooses
            xx = event.pos[0]
            yy = event.pos[1]
            jump_x = w_x + xx * k
            jump_y = w_y + yy * k

            if event.button == 4:
                k = k * 0.85

                w_x = jump_x - xx * k
                w_y = jump_y - yy * k

            if event.button == 5:
                k = k / 0.85

                w_x = jump_x - xx * k
                w_y = jump_y - yy * k

            # add astronomical object under the cursor
            if event.button == 3:
                # Jupiter:
                # balls.append(Ball(jump_x, jump_y, 71_000_000, 1.898 * 10 ** 27, 'orange'))

                # Sun:
                # balls.append(Ball(jump_x, jump_y, 696_000_000, 1.9891*10**30, 'purple'))

                # Black hole:
                # balls.append(Ball(jump_x,jump_y, 10_000_000, 1.9891*10**30*4000000, 'pink'))

                # Earth
                astro_objects.append(AstroObject(jump_x, jump_y, 6_371_000, 5.9722 * 10 ** 24, 'blue'))

            # time control
            if event.button == 2:
                if time_coef == 100_0000:
                    time_coef = 1
                    for i in astro_objects:
                        i.speed[0] /= 100_0000
                        i.speed[1] /= 100_0000
                else:
                    time_coef *= 10
                    for i in astro_objects:
                        i.speed[0] *= 10
                        i.speed[1] *= 10

                text_time_coef = font.render('Time: x' + str(time_coef), True, 'green')

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                w_x -= event.rel[0] * k
                w_y -= event.rel[1] * k

    collisions = []
    # calculate forces for each astronomical object
    for i in range(len(astro_objects)):
        for j in range(i + 1, len(astro_objects)):
            dx = astro_objects[j].real_x - astro_objects[i].real_x
            dy = astro_objects[j].real_y - astro_objects[i].real_y
            d = (dx ** 2 + dy ** 2) ** 0.5
            ff = G * astro_objects[i].mass * astro_objects[j].mass / d ** 2

            astro_objects[i].f[0] += dx * ff / d
            astro_objects[i].f[1] += dy * ff / d

            astro_objects[j].f[0] -= dx * ff / d
            astro_objects[j].f[1] -= dy * ff / d

            if astro_objects[i].real_r > d - astro_objects[j].real_r:
                collisions.append((i, j))

    # collisions handler:
    for i in collisions:
        obj1 = astro_objects[i[0]]
        obj2 = astro_objects[i[1]]
        if obj1.status and obj2.status:
            obj1.status = False
            obj2.status = False
            if obj1.real_r > obj2.real_r:
                c = obj1.colour
            else:
                c = obj2.colour

            t = AstroObject((obj1.real_x * obj1.mass + obj2.real_x * obj2.mass) / (obj1.mass + obj2.mass),
                            (obj1.real_y * obj1.mass + obj2.real_y * obj2.mass) / (obj1.mass + obj2.mass),
                            (obj1.real_r ** 3 + obj2.real_r ** 3) ** (1 / 3),
                            obj1.mass + obj2.mass,
                            c)
            t.speed[0] = (obj1.mass * obj1.speed[0] + obj2.mass * obj2.speed[0]) / (obj1.mass + obj2.mass)
            t.speed[1] = (obj1.mass * obj1.speed[1] + obj2.mass * obj2.speed[1]) / (obj1.mass + obj2.mass)
            astro_objects.append(t)

    tt = []
    for obj in astro_objects:
        if obj.status:
            tt.append(obj)
    astro_objects = tt

    for obj in astro_objects:
        obj.update()
        obj.f = [0, 0]

    # drawing
    screen.fill('black')

    for obj in astro_objects:
        obj.draw()

    screen.blit(text_FPS, (10, 10))
    screen.blit(text_time_coef, (10, 50))
    pygame.display.update()
pygame.quit()
