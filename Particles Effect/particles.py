import pygame
import sys
import random
from pygame.locals import *

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (65, 105, 255)
YELLOW = (224, 208, 31)
color_list = [WHITE, RED, BLUE, YELLOW]

mainClock = pygame.time.Clock()
framerate = 60

pygame.display.set_caption('Particles')
screen = pygame.display.set_mode((500, 500), 0, 32)

'''a particle is a thing that exists at a location,
typically moves around, typically changes over time,
and typically disappears after a certain amount of time'''


def circle_to_surf(radius, color):
	# Bán kính ánh sáng gấp đôi particle
	surf = pygame.Surface((radius * 2, radius * 2))
	# Vẽ hình tròn ở tâm của surface
	pygame.draw.circle(surf, color, (radius, radius), radius)
	surf.set_colorkey(BLACK)
	return surf


def particles_generate(particles_list, screen, click_flag, x, y):
	if click_flag == True:
		# each particle has these attributes: [location[x, y], velocity[x, y], timer]
		# for i in range(10):
		particles_list.append(
			[[x, y], [random.randint(0, 20) / 10 - 1, -2], random.randint(6, 8)])

	for particle in particles_list:
		# typically moves around:
		particle[0][0] += particle[1][0]
		particle[0][1] += particle[1][1]
		# typically changes over time:
		particle[2] -= 0.05
		particle[1][1] += 0.1  # gravity of these particle
		pygame.draw.circle(
			screen, BLACK, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

		radius = particle[2] * 2  # Bán kính xung quanh particle
		screen.blit(circle_to_surf(radius, (30, 30, 30)), (int(particle[0][0] - radius), int(
			particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)  # Trừ radius để vẽ ngay tâm particle

	# typically disappears after a certain amount of time:
	# Sắp xếp theo chiều giảm dần, enumerate là biến đổi list thành dạng [(index1: value1), (index2: value2)]
	#print(sorted(enumerate(particles), reverse = True))
	for i, v in sorted(enumerate(particles_list), reverse=True):
		if v[2] <= 0:
			particles_list.pop(i)


# timer also is radius of a circle-shaped particle
particles = []
click = False

while True:
	screen.fill(WHITE)
	pygame.draw.rect(screen, YELLOW, pygame.Rect(100, 100, 200, 60))

	mx, my = pygame.mouse.get_pos()

	particles_generate(particles, screen, click, mx, my)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				click = True
		if event.type == MOUSEBUTTONUP:
			if event.button == 1:
				click = False

	pygame.display.update()
	mainClock.tick(framerate)
