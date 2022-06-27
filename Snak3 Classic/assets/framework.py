import pygame
from pygame.locals import *

import sys
import random

import assets.utility_funcs as util

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

# Colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (152, 152, 152)
MEDIUM_GREY = (170, 170, 170)
LIGHT_GREY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (65, 105, 255)
YELLOW = (224, 208, 31)

# Images.
m = 20
head_img = pygame.transform.scale(pygame.image.load('assets/images/head.png'), (m, m))
body_img = pygame.transform.scale(pygame.image.load('assets/images/body.png'), (m, m))
food_img = pygame.transform.scale(pygame.image.load('assets/images/food.png'), (m, m))
boost_img = [pygame.transform.scale(pygame.image.load('assets/images/score_boost.png'), (m, m)),
			pygame.transform.scale(pygame.image.load('assets/images/speed_boost.png'), (m, m))]

# Sounds and music.
eating_sound = pygame.mixer.Sound('assets/sounds/eating.wav')
boost_sound = pygame.mixer.Sound('assets/sounds/boost.wav')
boost_sound.set_volume(0.5)
game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')
game_over_sound.set_volume(0.6)

# Shockwaves effect.
def shockwaves_generate(sw_list, click_flag, x, y, surf, color):
	# Append [[x, y], radius, width - also timer] of the shockwave
	if click_flag:
		sw_list.append([[x, y], 1, 5])

	# Loop through the shockwave list
	for sw in sw_list:
		if int(sw[2]) == 0:
			sw[2] = -1  # Set the width to -1, so it'll draw nothing
		pygame.draw.circle(surf, color, [sw[0][0], sw[0][1]], sw[1], int(sw[2]))
		sw[2] -= 0.07  # Decrease the line width of the circle over time, equivalent to increase the last duration of it
		sw[1] += 1  # Increase the radius of the circle over time

	#print(sorted(enumerate(sw_list), reverse=True))
	for i, v in sorted(enumerate(sw_list), reverse=True):
		if v[2] <= 0:
			sw_list.pop(i)

# Particles effect:
def particles_generate(particles_list, screen, color, x, y):
	#for i in range(10):
	particles_list.append([[x,y], [random.randint(0,40) / 10 - 2, random.randint(0,40) / 10 - 2], random.randint(2,3)])

	for particle in particles_list:
		# typically moves around:
		particle[0][0] += particle[1][0]
		particle[0][1] += particle[1][1]
		# typically changes over time:
		particle[2] -= 0.05
		#particle[1][1] += 0.1 # gravity of these particle
		pygame.draw.circle(screen, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

		radius = particle[2] * 2 #Bán kính xung quanh particle
		screen.blit(util.circle_to_surf(radius, (30,30,30)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
		
	# typically disappears after a certain amount of time:
	#Sắp xếp theo chiều giảm dần, enumerate là biến đổi list thành dạng [(index1:value1), (index2, value2)]
	#print(sorted(enumerate(particles), reverse = True))
	for i, v in sorted(enumerate(particles_list), reverse = True):
		if v[2] <= 0:
			particles_list.pop(i)

# Read from file.
def read_file(file_name):
	try:
		f = open(file_name, 'r')
		content = f.readlines()
		# print(content)
		
		for line in content:
			line = line.lower()
			if "music" in line:
				if "true" in line:
					music_flag = True
				else:
					music_flag = False
			
			elif "resolution" in line:
				splited_line = line.split()
				res_w = int(splited_line[2])
				res_h = int(splited_line[4])
			
			elif "fullscreen" in line:
				if "true" in line:
					fllscrn_flag = True
				else:
					fllscrn_flag = False
		
		return music_flag, fllscrn_flag, res_w, res_h
	
	except IOError:
		print('An error occurred while reading the file.')
	
	finally:
		f.close()

# Write to file.
def write_file(file_name, music_flag, fllscrn_flag, res_w, res_h):
	try:
		f = open(file_name, 'w')
		f.write(f'Music = {music_flag}\n')
		f.write(f'Resolution = {res_w} x {res_h}\n')
		f.write(f'Fullscreen: = {fllscrn_flag}\n')
	
	except IOError:
		print('An error occurred while writing to the file.')
	
	finally:
		f.close()

#Hàm settings:
def show_settings(music_flag, fllscrn_flag, res_w, res_h, WINDOW_SIZE, monitor_size, screen, ws, clock, framerate):
	running = True
	click = False
	shockwaves = []

	alpha = 255
	while running:
		screen.fill(WHITE)

		mx ,my = pygame.mouse.get_pos()

		util.draw_text('SETTINGS', ws[0]/2, ws[1]/6, 50, screen, bold=True)

		button_1 = pygame.Rect(200,340,200,50)
		util.draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/5*2)
		util.draw_text('Resolution', ws[0]/2, ws[1]/12*5, 30, screen)
		if button_1.collidepoint((mx,my)):
			util.draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*2)
			util.draw_text('Resolution', ws[0]/2, ws[1]/12*5, 30, screen, color=YELLOW)
			if click:
				util.fade_out(util.get_win_size(screen), screen)
				screen, ws, res_w, res_h, fllscrn_flag = show_resolution(music_flag, fllscrn_flag, res_w, res_h, WINDOW_SIZE, monitor_size, screen, ws, clock, framerate)
				alpha = 255

		button_2 = pygame.Rect(200,340,200,50)
		util.draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/2)
		util.draw_text('Controls', ws[0]/2, ws[1]/60*31, 30, screen)
		if button_2.collidepoint((mx,my)):
			util.draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/2)
			util.draw_text('Controls', ws[0]/2, ws[1]/60*31, 30, screen, color=YELLOW)
			if click:
				util.fade_out(util.get_win_size(screen), screen)
				screen, ws = show_controls(fllscrn_flag, WINDOW_SIZE, screen, ws, clock, framerate)
				alpha = 255

		button_3 = pygame.Rect(200,340,200,50)
		util.draw_rect(button_3, screen, GREY, ws[0]/2, ws[1]/5*3)
		if music_flag:
			util.draw_text('Music:[ON]', ws[0]/2, ws[1]/60*37, 30, screen)
		else:
			util.draw_text('Music:[OFF]', ws[0]/2, ws[1]/60*37, 30, screen)
		if button_3.collidepoint((mx,my)):
			if music_flag:
				util.draw_rect(button_3, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
				util.draw_text('Music:[ON]', ws[0]/2, ws[1]/60*37, 30, screen, color=YELLOW)
			else:
				util.draw_rect(button_3, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
				util.draw_text('Music:[OFF]', ws[0]/2, ws[1]/60*37, 30, screen, color=YELLOW)
			if click:
				music_flag = not music_flag
				write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)
				if music_flag:
					pygame.mixer.music.play(-1)
				else:
					pygame.mixer.music.stop()

		button_4 = pygame.Rect(200,400,200,50)
		util.draw_rect(button_4, screen, GREY, ws[0]/2, ws[1]/10*7)
		util.draw_text('Back', ws[0]/2, ws[1]/60*43, 30, screen)
		if button_4.collidepoint((mx,my)):
			util.draw_rect(button_4, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*7)
			util.draw_text('Back', ws[0]/2, ws[1]/60*43, 30, screen, color=YELLOW)
			if click:
				running = False
				util.fade_out(util.get_win_size(screen), screen)
				break

		util.draw_text('© by Constance, v1.0', ws[0]/2, ws[1]-15, 15, screen)

		shockwaves_generate(shockwaves, click, mx, my, screen, BLACK)
		
		if alpha > 0:
			if alpha == 255:
				fade_in = pygame.Surface(util.get_win_size(screen))
				fade_in.fill(WHITE)
				shockwaves.clear()

			fade_in.set_alpha(alpha)
			screen.blit(fade_in, (0,0))
			alpha -= 15

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
					util.fade_out(util.get_win_size(screen), screen)
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if not fllscrn_flag:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
		
		pygame.display.update()
		clock.tick(framerate)
	return screen, ws

#Hàm submenu controls:
def show_controls(fllscrn_flag, WINDOW_SIZE, screen, ws, clock, framerate):
	running = True 
	click = False
	alpha = 255
	shockwaves = []

	while running:
		screen.fill(WHITE)
		mx, my = pygame.mouse.get_pos()

		util.draw_text('CONTROLS', ws[0]/2, ws[1]/6, 50, screen, bold=True)

		util.draw_text('W: Up', ws[0]/2, ws[1]/60*17, 30, screen)
		util.draw_text('S: Down', ws[0]/2, ws[1]/20*7, 30, screen)
		util.draw_text('A: Left', ws[0]/2, ws[1]/12*5, 30, screen)
		util.draw_text('D: Right', ws[0]/2, ws[1]/60*29, 30, screen)
		util.draw_text('ESC: Pause Game', ws[0]/2, ws[1]/20*11, 30, screen)
		
		button_1 = pygame.Rect(200,400,100,50)
		util.draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/10*7)
		util.draw_text('Back', ws[0]/2, ws[1]/60*43, 30, screen)
		if button_1.collidepoint((mx,my)):
			util.draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*7)
			util.draw_text('Back', ws[0]/2, ws[1]/60*43, 30, screen, color=YELLOW)
			if click:
				running = False
				util.fade_out(util.get_win_size(screen), screen)
				break

		util.draw_text('© by Constance, v1.0', ws[0]/2, ws[1]-15, 15, screen)

		shockwaves_generate(shockwaves, click, mx, my, screen, BLACK)

		if alpha > 0:
			if alpha == 255:
				fade_in = pygame.Surface(util.get_win_size(screen))
				fade_in.fill(WHITE)
				shockwaves.clear()

			fade_in.set_alpha(alpha)
			screen.blit(fade_in, (0,0))
			alpha -= 15

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
					util.fade_out(util.get_win_size(screen), screen)
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if not fllscrn_flag:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		pygame.display.update()
		clock.tick(framerate)
	return screen, ws

#Hàm submenu resolution
def show_resolution(music_flag, fllscrn_flag, res_w, res_h, WINDOW_SIZE, monitor_size, screen, ws, clock, framerate):
	running = True 
	click = False
	alpha = 255
	shockwaves = []

	while running:
		screen.fill(WHITE)
		mx,my = pygame.mouse.get_pos()

		util.draw_text('RESOLUTION', ws[0]/2, ws[1]/6, 50, screen, bold=True)

		if not fllscrn_flag:
			button_1 = pygame.Rect(200,340,200,50)
			util.draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/10*3)
			if res_w == 600 and res_h == 600:
				util.draw_rect(button_1, screen, YELLOW, ws[0]/2, ws[1]/10*3)
				util.draw_text('600 x 600', ws[0]/2, ws[1]/60*19, 30, screen)
			else:
				util.draw_text('600 x 600', ws[0]/2, ws[1]/60*19, 30, screen)
			if button_1.collidepoint((mx,my)):
				if res_w != 600 and res_h != 600:
					util.draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*3)
					util.draw_text('600 x 600', ws[0]/2, ws[1]/60*19, 30, screen, color=YELLOW)
				if click:
					res_w = 600
					res_h = 600
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)
			
			button_2 = pygame.Rect(200,340,200,50)
			util.draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/5*2)
			if res_w == 1152 and res_h == 864:
				util.draw_rect(button_2, screen, YELLOW, ws[0]/2, ws[1]/5*2)
				util.draw_text('1152 x 864', ws[0]/2, ws[1]/12*5, 30, screen)
			else:
				util.draw_text('1152 x 864', ws[0]/2, ws[1]/12*5, 30, screen)
			if button_2.collidepoint((mx,my)):
				if res_w != 1152 and res_h != 864:
					util.draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*2)
					util.draw_text('1152 x 864', ws[0]/2, ws[1]/12*5, 30, screen, color=YELLOW)
				if click:
					res_w = 1152
					res_h = 864
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)

			button_3 = pygame.Rect(200,340,200,50)
			util.draw_rect(button_3, screen, GREY, ws[0]/2, ws[1]/2)
			if res_w == 1366 and res_h == 768:
				util.draw_rect(button_3, screen, YELLOW, ws[0]/2, ws[1]/2)
				util.draw_text('1366 x 768', ws[0]/2, ws[1]/60*31, 30, screen)
			else:
				util.draw_text('1366 x 768', ws[0]/2, ws[1]/60*31, 30, screen)
			if button_3.collidepoint((mx,my)):
				if res_w != 1366 and res_h != 768:
					util.draw_rect(button_3, screen, MEDIUM_GREY, ws[0]/2, ws[1]/2)
					util.draw_text('1366 x 768', ws[0]/2, ws[1]/60*31, 30, screen, color=YELLOW)
				if click:
					res_w = 1366
					res_h = 768
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)

			button_4 = pygame.Rect(200,340,200,50)
			util.draw_rect(button_4, screen, GREY, ws[0]/2, ws[1]/5*3)
			if res_w == 1600 and res_h == 900:
				util.draw_rect(button_4, screen, YELLOW, ws[0]/2, ws[1]/5*3)
				util.draw_text('1600 x 900', ws[0]/2, ws[1]/60*37, 30, screen)
			else:
				util.draw_text('1600 x 900', ws[0]/2, ws[1]/60*37, 30, screen)
			if button_4.collidepoint((mx,my)):
				if res_w != 1600 and res_h != 900:
					util.draw_rect(button_4, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
					util.draw_text('1600 x 900', ws[0]/2, ws[1]/60*37, 30, screen, color=YELLOW)
				if click:
					res_w = 1600
					res_h = 900
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)
		
		else:
			button_1 = pygame.Rect(200,340,200,50)
			util.draw_rect(button_1, screen, LIGHT_GREY, ws[0]/2, ws[1]/10*3)
			util.draw_text('600 x 600', ws[0]/2, ws[1]/60*19, 30, screen, color=GREY)

			button_2 = pygame.Rect(200,340,200,50)
			util.draw_rect(button_2, screen, LIGHT_GREY, ws[0]/2, ws[1]/5*2)
			util.draw_text('1152 x 864', ws[0]/2, ws[1]/12*5, 30, screen, color=GREY)

			button_3 = pygame.Rect(200,340,200,50)
			util.draw_rect(button_3, screen, LIGHT_GREY, ws[0]/2, ws[1]/2)
			util.draw_text('1366 x 768', ws[0]/2, ws[1]/60*31, 30, screen, color=GREY)

			button_4 = pygame.Rect(200,340,200,50)
			util.draw_rect(button_4, screen, LIGHT_GREY, ws[0]/2, ws[1]/5*3)
			util.draw_text('1600 x 900', ws[0]/2, ws[1]/60*37, 30, screen, color=GREY)

		button_5 = pygame.Rect(200,340,200,50)
		util.draw_rect(button_5, screen, GREY, ws[0]/2, ws[1]/10*7)
		if fllscrn_flag:
			util.draw_rect(button_5, screen, YELLOW, ws[0]/2, ws[1]/10*7)
			util.draw_text('Fullscreen', ws[0]/2, ws[1]/60*43, 30, screen)
		else:
			util.draw_text('Fullscreen', ws[0]/2, ws[1]/60*43, 30, screen)
		if button_5.collidepoint((mx,my)):
			if not fllscrn_flag:
				util.draw_rect(button_5, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*7)
				util.draw_text('Fullscreen', ws[0]/2, ws[1]/60*43, 30, screen, color=YELLOW)
			if click:
				fllscrn_flag = not fllscrn_flag
				
				if fllscrn_flag:
					screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
					ws = [screen.get_width(), screen.get_height()]
				else:
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
				
				write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)

		button_6 = pygame.Rect(200,400,200,50)
		util.draw_rect(button_6, screen, GREY, ws[0]/2, ws[1]/5*4)
		util.draw_text('Back', ws[0]/2, ws[1]/60*49, 30, screen)
		if button_6.collidepoint((mx,my)):
			util.draw_rect(button_6, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*4)
			util.draw_text('Back', ws[0]/2, ws[1]/60*49, 30, screen, color=YELLOW)
			if click:
				running = False
				util.fade_out(util.get_win_size(screen), screen)
				break

		util.draw_text('© by Constance, v1.0', ws[0]/2, ws[1]-15, 15, screen)

		shockwaves_generate(shockwaves, click, mx, my, screen, BLACK)

		if alpha > 0:
			if alpha == 255:
				fade_in = pygame.Surface(util.get_win_size(screen))
				fade_in.fill(WHITE)
				shockwaves.clear()

			fade_in.set_alpha(alpha)
			screen.blit(fade_in, (0,0))
			alpha -= 15

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
					util.fade_out(util.get_win_size(screen), screen)
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if not fllscrn_flag:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		pygame.display.update()
		clock.tick(framerate)
	return screen, ws, res_w, res_h, fllscrn_flag

#Hàm pause game:
def pause_menu(exit_flag, fllscrn_flag, WINDOW_SIZE, screen, ws, clock, framerate):
	running = True
	click = False
	exit_flag = False

	surf = pygame.Surface(WINDOW_SIZE)
	surf.fill(GREY)
	surf.set_alpha(150)
	screen.blit(surf, (0,0))
	while running:
		mx, my = pygame.mouse.get_pos()

		util.draw_text('PAUSED', ws[0]/2, ws[1]/3, 50, screen, color=RED, bold=True)

		button_1 = pygame.Rect(0,0,250,50)
		util.draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/2)
		util.draw_text('Resume', ws[0]/2, ws[1]/60*31, 30, screen)
		if button_1.collidepoint((mx,my)):
			util.draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/2)
			util.draw_text('Resume', ws[0]/2, ws[1]/60*31, 30, screen, color=YELLOW)
			if click:
				running = False

		button_2 = pygame.Rect(0,0,250,50)
		util.draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/5*3)
		util.draw_text('Return to Menu', ws[0]/2, ws[1]/60*37, 30, screen)
		if button_2.collidepoint((mx, my)):
			util.draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
			util.draw_text('Return to Menu', ws[0]/2, ws[1]/60*37, 30, screen, color=YELLOW)
			if click:
				exit_flag = True
				running = False

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					running = False
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if not fllscrn_flag:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					surf = pygame.Surface(util.get_win_size(screen))
					surf.fill(GREY)
					surf.set_alpha(150)
					screen.blit(surf, (0,0))

		pygame.display.update()
		clock.tick(framerate)
	return exit_flag, ws, screen

#Hàm game over:
def game_over(return_menu_flag, retry_flag,  fllscrn_flag, screen, ws, clock, framerate, score, high_score):
	running = True
	click = False
	return_menu_flag = False
	retry_flag = False
	shockwaves = []
	game_over_sound.play()

	while running:
		
		mx, my = pygame.mouse.get_pos()

		screen.fill(WHITE)
		util.draw_text('GAME OVER', ws[0]/2, ws[1]/6, 50, screen, color=RED, bold=True)
		show_score(0, score, high_score, screen, ws) #Hiển thị điểm

		button_1 = pygame.Rect(0,0,250,50)
		util.draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/3*2)
		util.draw_text('Retry', ws[0]/2, ws[1]/60*41, 30, screen)
		if button_1.collidepoint((mx,my)):
			util.draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/3*2)
			util.draw_text('Retry', ws[0]/2, ws[1]/60*41, 30, screen, color=YELLOW)
			if click:
				retry_flag = True
				running = False

		button_2 = pygame.Rect(0,0,250,50)
		util.draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/30*23)
		util.draw_text('Return to Menu', ws[0]/2, ws[1]/60*47, 30, screen)
		if button_2.collidepoint((mx, my)):
			util.draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/30*23)
			util.draw_text('Return to Menu', ws[0]/2, ws[1]/60*47, 30, screen, color=YELLOW)
			if click:
				return_menu_flag = True
				running = False

		shockwaves_generate(shockwaves, click, mx, my, screen, BLACK)

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if not fllscrn_flag:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		pygame.display.update() #Cập nhật screen
		clock.tick(framerate)
	return retry_flag, return_menu_flag, ws, screen


#Hàm hiện điểm:
def show_score(choice, score, high_score, screen, ws):
	if choice == 1:
		util.draw_text(f'Score: {score}', 70, 20, 15, screen)
		util.draw_text(f'High Score: {high_score}', ws[0]-100, 20, 15, screen)
	else:
		if score == high_score:
			util.draw_text(f'New High Score: {high_score}', ws[0]/2, ws[1]/12*5, 25, screen)
		else:
			util.draw_text(f'High Score: {high_score}', ws[0]/2, ws[1]/12*5, 25, screen)
		util.draw_text(f'Current Score: {score}', ws[0]/2, ws[1]/15*7, 20, screen)