import pygame
import sys
import random
from pygame.locals import *

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

mainClock = pygame.time.Clock()
fps = 60

pygame.display.set_caption('Shockwave')
screen = pygame.display.set_mode((500, 500))

# User defined event.
CREATE_SHOCKWAVE = pygame.USEREVENT + 0
pygame.time.set_timer(CREATE_SHOCKWAVE, 500)
pygame.event.set_blocked(None)
pygame.event.set_allowed([QUIT, KEYDOWN, CREATE_SHOCKWAVE])

def shockwaves_generate(sw_list, x, y, surf, color, click_flag = False):
	# Append [[x, y], radius, width - also timer] of the shockwave.
	if click_flag:
		sw_list.append([[x, y], 1, 5])

	# Loop through the shockwave list.
	for sw in sw_list:
		if int(sw[2]) == 0:
			sw[2] = -1  # Set the width to -1, so it'll draw nothing.

		pygame.draw.circle(surf, color, [sw[0][0], sw[0][1]], sw[1], int(sw[2]))
		# Decrease the line width of the circle over time, equivalent to countdown the timer.
		sw[2] -= 0.07
		sw[1] += 1  # Increase the radius of the circle over time.

	#print(sorted(enumerate(sw_list), reverse=True))
	for i, v in sorted(enumerate(sw_list), reverse=True):
		if v[2] <= 0:
			sw_list.pop(i)


shockwaves = []
click = False

while True:
	screen.fill(WHITE)

	#mx, my = pygame.mouse.get_pos()
	x = random.randint(0, 500)
	y = random.randint(0, 500)

	shockwaves_generate(shockwaves, x, y, screen, BLACK, click)

	click = False
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

		if event.type == CREATE_SHOCKWAVE:
			click = True

	pygame.display.update()
	mainClock.tick(fps)
