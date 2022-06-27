import pygame, sys, random, time
from pygame.locals import *

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (152,152,152)
MEDIUM_GREY = (170,170,170)
LIGHT_GREY = (220,220,220)
RED = (255,0,0)
BLUE = (65,105,255)
YELLOW = (224,208,31)

m = 20
head_img = pygame.transform.scale(pygame.image.load('assets/images/head.png'),(m,m))
body_img = pygame.transform.scale(pygame.image.load('assets/images/body.png'),(m,m))
food_img = pygame.transform.scale(pygame.image.load('assets/images/food.png'),(m,m))
boost_img = [pygame.transform.scale(pygame.image.load('assets/images/score_boost.png'),(m,m)),
			pygame.transform.scale(pygame.image.load('assets/images/speed_boost.png'),(m,m))]
eating_sound = pygame.mixer.Sound('assets/sounds/eating.wav')
boost_sound = pygame.mixer.Sound('assets/sounds/boost.wav')
boost_sound.set_volume(0.5)
game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav')
game_over_sound.set_volume(0.6)

#Hàm lấy kích thước cửa sổ:
def get_win_size(screen):
	win_size = (screen.get_width(), screen.get_height())
	return win_size

#Hàm hiệu ứng chuyển cảnh:
def fade_out(WINDOW_SIZE, draw_surface):
	fade_out = pygame.Surface(WINDOW_SIZE)
	fade_out.fill(WHITE)
	for alpha in range(0,256): #Set opaque value 
		fade_out.set_alpha(alpha)
		draw_surface.blit(fade_out, (0,0))
		pygame.display.update()
		pygame.time.delay(4) #Thời gian chuyển cảnh

#Hàm vẽ vùng sáng quanh particle
def circle_to_surf(radius, color):
	surf = pygame.Surface((radius * 2, radius * 2)) #Bán kính ánh sáng gấp đôi particle
	pygame.draw.circle(surf, color, (radius, radius), radius) #Vẽ hình tròn ở tâm của surface
	surf.set_colorkey(BLACK)
	return surf

#Hàm viết văn bản:
def draw_text(text, font_name, size, bold, color, surface, x, y):
	font = pygame.font.SysFont(font_name, size, bold)
	textobj = font.render(text, True, color)
	textrect = textobj.get_rect()
	textrect.midtop = (x,y)
	surface.blit(textobj, textrect)

#Hàm vẽ hình chữ nhật ở vị trí midtop:
def draw_rect(Rect_name, draw_surface, color, x, y):
	Rect_name.midtop = (x,y)
	pygame.draw.rect(draw_surface, color, Rect_name)

#Hàm sản sinh particles effect:
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
		screen.blit(circle_to_surf(radius, (30,30,30)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags=BLEND_RGB_ADD)
		
	# typically disappears after a certain amount of time:
	#Sắp xếp theo chiều giảm dần, enumerate là biến đổi list thành dạng [(index1:value1), (index2, value2)]
	#print(sorted(enumerate(particles), reverse = True))
	for i, v in sorted(enumerate(particles_list), reverse = True):
		if v[2] <= 0:
			particles_list.pop(i)

#Hàm đọc file:
def read_file(file_name, music_flag, fllscrn_flag, res_w, res_h):
	f = open(file_name, 'r')
	contents = f.readlines()
	for line in contents:
		if "Music" in line:
			if "True" in line:
				music_flag = True
			else: music_flag = False
		if "Resolution" in line:
			splited_line = line.split()
			res_w = int(splited_line[2])
			res_h = int(splited_line[4])
		if "Fullscreen" in line:
			if "True" in line:
				fllscrn_flag = True
			else: fllscrn_flag = False
	f.close()
	return music_flag, fllscrn_flag, res_w, res_h

#Hàm ghi file
def write_file(file_name, music_flag, fllscrn_flag, res_w, res_h):
	f = open(file_name, 'w')
	f.write(f'Music = {music_flag}\n')
	f.write(f'Resolution = {res_w} x {res_h}\n')
	f.write(f'Fullscreen: = {fllscrn_flag}\n')
	f.close()

#Hàm settings:
def show_settings(music_flag, fllscrn_flag, res_w, res_h, WINDOW_SIZE, monitor_size, screen, ws, clock, framerate):
	running = True
	click = False

	alpha = 255
	while running:
		screen.fill(WHITE)

		mx ,my = pygame.mouse.get_pos()

		draw_text('SETTINGS', 'consolas', 50, True, BLACK, screen, ws[0]/2, ws[1]/6)

		button_1 = pygame.Rect(200,340,200,50)
		draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/5*2)
		draw_text('Resolution', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/12*5)
		if button_1.collidepoint((mx,my)):
			draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*2)
			draw_text('Resolution', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/12*5)
			if click:
				fade_out(get_win_size(screen), screen)
				ws, screen, res_w, res_h, fllscrn_flag = show_resolution(music_flag, fllscrn_flag, res_w, res_h, WINDOW_SIZE, monitor_size, screen, ws, clock, framerate)
				alpha = 255

		button_2 = pygame.Rect(200,340,200,50)
		draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/2)
		draw_text('Controls', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*31)
		if button_2.collidepoint((mx,my)):
			draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/2)
			draw_text('Controls', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*31)
			if click:
				fade_out(get_win_size(screen), screen)
				ws, screen = show_controls(fllscrn_flag, WINDOW_SIZE, screen, ws, clock, framerate)
				alpha = 255

		button_3 = pygame.Rect(200,340,200,50)
		draw_rect(button_3, screen, GREY, ws[0]/2, ws[1]/5*3)
		if music_flag:
			draw_text('Music:[ON]', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*37)
		else:
			draw_text('Music:[OFF]', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*37)
		if button_3.collidepoint((mx,my)):
			if music_flag:
				draw_rect(button_3, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
				draw_text('Music:[ON]', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*37)
			else:
				draw_rect(button_3, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
				draw_text('Music:[OFF]', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*37)
			if click:
				music_flag = not music_flag
				write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)
				if music_flag:
					pygame.mixer.music.play(-1)
				else:
					pygame.mixer.music.stop()

		button_4 = pygame.Rect(200,400,200,50)
		draw_rect(button_4, screen, GREY, ws[0]/2, ws[1]/10*7)
		draw_text('Back', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*43)
		if button_4.collidepoint((mx,my)):
			draw_rect(button_4, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*7)
			draw_text('Back', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*43)
			if click:
				running = False
				fade_out(get_win_size(screen), screen)
				break

		draw_text('© by Constance, v1.0', 'consolas', 15, False, BLACK, screen, ws[0]/2, ws[1]-15)
		
		if alpha > 0:
			if alpha == 255:
				fade_in = pygame.Surface(get_win_size(screen))
				fade_in.fill(WHITE)
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
					fade_out(get_win_size(screen), screen)
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if fllscrn_flag == False:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
		
		pygame.display.update()
		clock.tick(framerate)
	return ws, screen

#Hàm submenu controls:
def show_controls(fllscrn_flag, WINDOW_SIZE, screen, ws, clock, framerate):
	running = True 
	click = False
	alpha = 255

	while running:
		screen.fill(WHITE)
		mx,my = pygame.mouse.get_pos()

		draw_text('CONTROLS', 'consolas', 50, True, BLACK, screen, ws[0]/2, ws[1]/6)

		draw_text('W: Up', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*17)
		draw_text('S: Down', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/20*7)
		draw_text('A: Left', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/12*5)
		draw_text('D: Right', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*29)
		draw_text('ESC: Pause Game', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/20*11)
		
		button_1 = pygame.Rect(200,400,100,50)
		draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/10*7)
		draw_text('Back', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*43)
		if button_1.collidepoint((mx,my)):
			draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*7)
			draw_text('Back', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*43)
			if click:
				running = False
				fade_out(get_win_size(screen), screen)
				break

		draw_text('© by Constance, v1.0', 'consolas', 15, False, BLACK, screen, ws[0]/2, ws[1]-15)

		if alpha > 0:
			if alpha == 255:
				fade_in = pygame.Surface(get_win_size(screen))
				fade_in.fill(WHITE)
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
					fade_out(get_win_size(screen), screen)
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if fllscrn_flag == False:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		pygame.display.update()
		clock.tick(framerate)
	return ws, screen

#Hàm submenu resolution
def show_resolution(music_flag, fllscrn_flag, res_w, res_h, WINDOW_SIZE, monitor_size, screen, ws, clock, framerate):
	running = True 
	click = False
	alpha = 255

	while running:
		screen.fill(WHITE)
		mx,my = pygame.mouse.get_pos()

		draw_text('RESOLUTION', 'consolas', 50, True, BLACK, screen, ws[0]/2, ws[1]/6)

		if fllscrn_flag == False:
			button_1 = pygame.Rect(200,340,200,50)
			draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/10*3)
			if res_w == 600 and res_h == 600:
				draw_rect(button_1, screen, YELLOW, ws[0]/2, ws[1]/10*3)
				draw_text('600 x 600', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*19)
			else:
				draw_text('600 x 600', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*19)
			if button_1.collidepoint((mx,my)):
				if res_w != 600 and res_h != 600:
					draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*3)
					draw_text('600 x 600', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*19)
				if click:
					res_w = 600
					res_h = 600
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)
			
			button_2 = pygame.Rect(200,340,200,50)
			draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/5*2)
			if res_w == 1152 and res_h == 864:
				draw_rect(button_2, screen, YELLOW, ws[0]/2, ws[1]/5*2)
				draw_text('1152 x 864', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/12*5)
			else:
				draw_text('1152 x 864', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/12*5)
			if button_2.collidepoint((mx,my)):
				if res_w != 1152 and res_h != 864:
					draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*2)
					draw_text('1152 x 864', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/12*5)
				if click:
					res_w = 1152
					res_h = 864
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)

			button_3 = pygame.Rect(200,340,200,50)
			draw_rect(button_3, screen, GREY, ws[0]/2, ws[1]/2)
			if res_w == 1366 and res_h == 768:
				draw_rect(button_3, screen, YELLOW, ws[0]/2, ws[1]/2)
				draw_text('1366 x 768', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*31)
			else:
				draw_text('1366 x 768', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*31)
			if button_3.collidepoint((mx,my)):
				if res_w != 1366 and res_h != 768:
					draw_rect(button_3, screen, MEDIUM_GREY, ws[0]/2, ws[1]/2)
					draw_text('1366 x 768', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*31)
				if click:
					res_w = 1366
					res_h = 768
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)

			button_4 = pygame.Rect(200,340,200,50)
			draw_rect(button_4, screen, GREY, ws[0]/2, ws[1]/5*3)
			if res_w == 1600 and res_h == 900:
				draw_rect(button_4, screen, YELLOW, ws[0]/2, ws[1]/5*3)
				draw_text('1600 x 900', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*37)
			else:
				draw_text('1600 x 900', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*37)
			if button_4.collidepoint((mx,my)):
				if res_w != 1600 and res_h != 900:
					draw_rect(button_4, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
					draw_text('1600 x 900', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*37)
				if click:
					res_w = 1600
					res_h = 900
					screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					write_file('data/user_config.txt', music_flag, fllscrn_flag, res_w, res_h)
		elif fllscrn_flag == True:
			button_1 = pygame.Rect(200,340,200,50)
			draw_rect(button_1, screen, LIGHT_GREY, ws[0]/2, ws[1]/10*3)
			draw_text('600 x 600', 'consolas', 30, False, GREY, screen, ws[0]/2, ws[1]/60*19)

			button_2 = pygame.Rect(200,340,200,50)
			draw_rect(button_2, screen, LIGHT_GREY, ws[0]/2, ws[1]/5*2)
			draw_text('1152 x 864', 'consolas', 30, False, GREY, screen, ws[0]/2, ws[1]/12*5)

			button_3 = pygame.Rect(200,340,200,50)
			draw_rect(button_3, screen, LIGHT_GREY, ws[0]/2, ws[1]/2)
			draw_text('1366 x 768', 'consolas', 30, False, GREY, screen, ws[0]/2, ws[1]/60*31)

			button_4 = pygame.Rect(200,340,200,50)
			draw_rect(button_4, screen, LIGHT_GREY, ws[0]/2, ws[1]/5*3)
			draw_text('1600 x 900', 'consolas', 30, False, GREY, screen, ws[0]/2, ws[1]/60*37)

		button_5 = pygame.Rect(200,340,200,50)
		draw_rect(button_5, screen, GREY, ws[0]/2, ws[1]/10*7)
		if fllscrn_flag:
			draw_rect(button_5, screen, YELLOW, ws[0]/2, ws[1]/10*7)
			draw_text('Fullscreen', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*43)
		else:
			draw_text('Fullscreen', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*43)
		if button_5.collidepoint((mx,my)):
			if fllscrn_flag == False:
				draw_rect(button_5, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*7)
				draw_text('Fullscreen', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*43)
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
		draw_rect(button_6, screen, GREY, ws[0]/2, ws[1]/5*4)
		draw_text('Back', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*49)
		if button_6.collidepoint((mx,my)):
			draw_rect(button_6, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*4)
			draw_text('Back', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*49)
			if click:
				running = False
				fade_out(get_win_size(screen), screen)
				break

		draw_text('© by Constance, v1.0', 'consolas', 15, False, BLACK, screen, ws[0]/2, ws[1]-15)

		if alpha > 0:
			if alpha == 255:
				fade_in = pygame.Surface(get_win_size(screen))
				fade_in.fill(WHITE)
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
					fade_out(get_win_size(screen), screen)
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if fllscrn_flag == False:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		pygame.display.update()
		clock.tick(framerate)
	return ws, screen, res_w, res_h, fllscrn_flag

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

		draw_text('PAUSED', 'consolas', 50, True, RED, screen, ws[0]/2, ws[1]/3)

		button_1 = pygame.Rect(0,0,250,50)
		draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/2)
		draw_text('Resume', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*31)
		if button_1.collidepoint((mx,my)):
			draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/2)
			draw_text('Resume', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*31)
			if click:
				running = False

		button_2 = pygame.Rect(0,0,250,50)
		draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/5*3)
		draw_text('Return to Menu', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*37)
		if button_2.collidepoint((mx, my)):
			draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
			draw_text('Return to Menu', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*37)
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
				if fllscrn_flag == False:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
					surf = pygame.Surface(get_win_size(screen))
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
	game_over_sound.play()

	while running:
		
		mx, my = pygame.mouse.get_pos()

		screen.fill(WHITE)
		draw_text('GAME OVER', 'consolas', 50, True, RED, screen, ws[0]/2, ws[1]/6)
		show_score(0, score, high_score, screen, ws) #Hiển thị điểm

		button_1 = pygame.Rect(0,0,250,50)
		draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/3*2)
		draw_text('Retry', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*41)
		if button_1.collidepoint((mx,my)):
			draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/3*2)
			draw_text('Retry', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*41)
			if click:
				retry_flag = True
				running = False

		button_2 = pygame.Rect(0,0,250,50)
		draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/30*23)
		draw_text('Return to Menu', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*47)
		if button_2.collidepoint((mx, my)):
			draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/30*23)
			draw_text('Return to Menu', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*47)
			if click:
				return_menu_flag = True
				running = False

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == VIDEORESIZE:
				if fllscrn_flag == False:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		pygame.display.update() #Cập nhật screen
		clock.tick(framerate)
	return retry_flag, return_menu_flag, ws, screen


#Hàm hiện điểm:
def show_score(choice, score, high_score, screen, ws):
	if choice == 1:
		draw_text(f'Score: {score}', 'consolas', 15, False, BLACK, screen, 70, 20)
		draw_text(f'High Score: {high_score}', 'consolas', 15, False, BLACK, screen, ws[0]-100, 20)
	else:
		if score == high_score:
			draw_text(f'New High Score: {high_score}', 'consolas', 25, False, BLACK, screen, ws[0]/2, ws[1]/12*5)
		else:
			draw_text(f'High Score: {high_score}', 'consolas', 25, False, BLACK, screen, ws[0]/2, ws[1]/12*5)
		draw_text(f'Current Score: {score}', 'consolas', 20, False, BLACK, screen, ws[0]/2, ws[1]/15*7)