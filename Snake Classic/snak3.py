import pygame, sys, random, time
import assets.framework as frwk
from pygame.locals import *

#Khởi tạo pygame
pygame.init()

#Khởi tạo mixer phát âm thanh
pygame.mixer.pre_init(44100, -16, 2, 512)

#FPS
mainClock = pygame.time.Clock()
framerate = 60

#Các hằng
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (152,152,152)
MEDIUM_GREY = (170,170,170)
LIGHT_GREY = (220,220,220)
RED = (255,0,0)
BLUE = (65,105,255)
YELLOW = (224,208,31)
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

#Tạo cửa sổ
pygame.display.set_caption('Snak3: Classic')
pygame.display.set_icon(pygame.image.load('assets/images/snak3.png'))
global screen, ws
screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
ws = [screen.get_width(), screen.get_height()]

#Load hình ảnh, âm thanh, nhạc:
m = 20
pygame.mixer.music.load('assets/musics/Blues.ogg')
pygame.mixer.music.set_volume(0.5)

global music_on, res_w, res_h, fullscreen
#Define the data type of the variables:
music_on = False
fullscreen = False
res_w = 0
res_h = 0

#Hàm menu chính:
def main_menu():
	global screen, ws
	global music_on, res_w, res_h, fullscreen

	music_on, fullscreen, res_w, res_h = frwk.read_file('data/user_config.txt', music_on, fullscreen, res_w, res_h)

	if fullscreen == True:
		screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
		ws = [screen.get_width(), screen.get_height()]
	else:
		screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
		ws = [screen.get_width(), screen.get_height()]
	
	if music_on:
		pygame.mixer.music.play(-1)
	
	click = False
	alpha = 0

	while True:
		#Lấy vị trí của chuột:
		mx, my = pygame.mouse.get_pos()

		#Tiêu đề:
		screen.fill(WHITE)
		frwk.draw_text('SNAK3: CLASSIC', 'consolas', 50, True, BLACK, screen, ws[0]/2, ws[1]/6)

		#Nút bấm:
		button_1 = pygame.Rect(300,240,270,50)
		frwk.draw_rect(button_1, screen, GREY, ws[0]/2, ws[1]/5*2)
		frwk.draw_text('Casual Mode', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/12*5)
		if button_1.collidepoint((mx, my)): #Khi dí trỏ chuột vào
			frwk.draw_rect(button_1, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*2)
			frwk.draw_text('Casual Mode', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/12*5)
			if click: #Khi bấm chuột vào
				frwk.fade_out(frwk.get_win_size(screen), screen)
				game(0)
				alpha = 255
		
		button_2 = pygame.Rect(165,300,270,50)
		frwk.draw_rect(button_2, screen, GREY, ws[0]/2, ws[1]/2)
		frwk.draw_text('Borderless Mode', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*31)
		if button_2.collidepoint((mx, my)):
			frwk.draw_rect(button_2, screen, MEDIUM_GREY, ws[0]/2, ws[1]/2)
			frwk.draw_text('Borderless Mode', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*31)
			if click:
				frwk.fade_out(frwk.get_win_size(screen), screen)
				game(1)
				alpha = 255

		button_3 = pygame.Rect(165,300,270,50)
		frwk.draw_rect(button_3, screen, GREY, ws[0]/2, ws[1]/5*3)
		frwk.draw_text('Settings', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*37)
		if button_3.collidepoint((mx, my)): #Khi dí trỏ chuột vào
			frwk.draw_rect(button_3, screen, MEDIUM_GREY, ws[0]/2, ws[1]/5*3)
			frwk.draw_text('Settings', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*37)
			if click: #Khi bấm chuột vào
				frwk.fade_out(frwk.get_win_size(screen), screen)
				ws, screen = frwk.show_settings(music_on, fullscreen, res_w, res_h, frwk.get_win_size(screen), monitor_size, screen, ws, mainClock, framerate)
				alpha = 255

		button_4 = pygame.Rect(165,300,270,50)
		frwk.draw_rect(button_4, screen, GREY, ws[0]/2, ws[1]/10*7)
		frwk.draw_text('Quit', 'consolas', 30, False, BLACK, screen, ws[0]/2, ws[1]/60*43)
		if button_4.collidepoint((mx, my)): #Khi dí trỏ chuột vào
			frwk.draw_rect(button_4, screen, MEDIUM_GREY, ws[0]/2, ws[1]/10*7)
			frwk.draw_text('Quit', 'consolas', 30, False, YELLOW, screen, ws[0]/2, ws[1]/60*43)
			if click: #Khi bấm chuột vào
				pygame.quit()
				sys.exit()

		frwk.draw_text('© by Constance, v1.0', 'consolas', 15, False, BLACK, screen, ws[0]/2, ws[1]-15)

		if alpha > 0:
			if alpha == 255:
				fade_in = pygame.Surface(frwk.get_win_size(screen))
				fade_in.fill(WHITE)
			fade_in.set_alpha(alpha)
			screen.blit(fade_in, (0,0))
			alpha -= 15

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1: #Khi bấm chuột trái
					click = True
			if event.type == VIDEORESIZE:
				if fullscreen == False:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]
		
		pygame.display.update()
		mainClock.tick(framerate)

global high_score
high_score = 0

#Hàm game:
def game(choice):
	global screen, ws
	#Khai báo biến:
	snake_pos = [100,60] #Vị trí ban đầu của con rắn
	snake_body = [[100,60], [80,60], [60,60]] #Vị trí các phần đầu, thân, đuôi

	#Thức ăn
	food_x = random.randrange(2, int(ws[0]/10 - 3)) 
	food_y = random.randrange(3, int(ws[1]/10 - 3))
	if food_x % 2 != 0: food_x += 1 #Nếu là số lẻ thì tăng lên 1
	if food_y % 2 != 0: food_y += 1
	food_pos = [food_x * 10, food_y * 10]
	food_flag = True #Cờ thức ăn, kiểm tra rắn có ăn dc mồi hay ko

	#Boost
	boost_x = random.randrange(2, int(ws[0]/10 - 3))
	boost_y = random.randrange(3, int(ws[1]/10 - 3))
	if boost_x % 2 != 0: boost_x += 1
	if boost_y % 2 != 0: boost_y += 1
	if boost_x == food_x and boost_y == food_y:
		boost_x += 20
		if boost_x == ws[0] - 30:
			boost_x -= 20 
	boost_pos = [boost_x * 10, boost_y * 10]
	boost_flag = True

	direction = 'RIGHT' #Hướng di chuyển lúc đầu
	change_to = direction #Đổi hướng di chuyển
	score = 0
	apple_count = 0
	global high_score
	exit_to_menu = False
	running = True
	index = random.randint(0, 1)
	if index == 0:
		boost_time = 75
	elif index == 1:
		boost_time = 113
	particles = []

	#Vòng lặp chính:
	while running:	
		#Hiệu quả buff khi nhặt boost:

		if snake_pos[0] == boost_pos[0] and snake_pos[1] == boost_pos[1]:
			if boost_flag == True:
				frwk.boost_sound.play()
			boost_flag = False				

		if boost_flag == False:
			boost_time -= 1

		if exit_to_menu == True:
			running = False
			frwk.fade_out(frwk.get_win_size(screen), screen)
			
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					exit_to_menu, ws, screen = frwk.pause_menu(exit_to_menu, fullscreen, frwk.get_win_size(screen), screen, ws, mainClock, framerate)
					#running = False #Ấn escape sẽ trở về menu
				if event.key == K_d:
					change_to = 'RIGHT'
				if event.key == K_a:
					change_to = 'LEFT'
				if event.key == K_w:
					change_to = 'UP'
				if event.key == K_s:
					change_to = 'DOWN'
			if event.type == VIDEORESIZE:
				if fullscreen == False:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		#Hướng đi: tránh rắn đi ngược lại, đi lùi
		if change_to == 'RIGHT' and not direction == 'LEFT':
			direction = 'RIGHT'
		if change_to == 'LEFT' and not direction == 'RIGHT':
			direction = 'LEFT'
		if change_to == 'UP' and not direction == 'DOWN':
			direction = 'UP'
		if change_to == 'DOWN' and not direction == 'UP':
			direction = 'DOWN'

		angle = 0 #Góc xoay, số (+) là ngược chiều kim đồng hồ, (-) là thuận chiều kim đồng hồ
		#Cập nhật vị trí mới:
		if direction == 'RIGHT': #Mặc định hình ảnh nằm ngang
			snake_pos[0] += m
		elif direction == 'LEFT':
			snake_pos[0] -= m
			angle = 180
		elif direction == 'UP':
			snake_pos[1] -= m
			angle = 90
		elif direction == 'DOWN':
			snake_pos[1] += m
			angle = -90
		
		#Thêm khúc dài ra khi ăn:
		snake_body.insert(0,list(snake_pos)) #Chèn vị trí vào phần tử thứ 1 trong list body
		if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]: #Khi 2 tọa đồ trùng nhau
			frwk.eating_sound.play()
			if boost_flag == False:
				apple_count += 1
			if boost_flag == False and boost_time > 0:
				if index == 0:
					score += 5
				elif index == 1:
					score += 1
			else:
				score += 1
			food_flag = False
		else:
			snake_body.pop()

		if score > high_score:
			high_score = score

		#Sản sinh mồi:
		if food_flag == False: #Nếu ăn dc rồi, thì tạo vị trí mới cho mồi
			food_x = random.randrange(2, int(ws[0]/10 - 3))
			food_y = random.randrange(3, int(ws[1]/10 - 3))
			if food_x % 2 != 0: food_x += 1
			if food_y % 2 != 0: food_y += 1
			food_pos = [food_x * 10, food_y * 10]
		food_flag = True

		#Sản sinh vị trí boost mới:
		if boost_flag == False:
			boost_x = random.randrange(2, int(ws[0]/10 - 3))
			boost_y = random.randrange(3, int(ws[1]/10 - 3))
			if boost_x % 2 != 0: boost_x += 1
			if boost_y % 2 != 0: boost_y += 1
			if boost_x == food_x and boost_y == food_y:
				boost_x += 20
				if boost_x == ws[0] - 30:
					 boost_x -= 20 
			boost_pos = [boost_x * 10, boost_y * 10]
		#Reset flag khi ăn đủ 10 trái táo
		if apple_count == 10:
			boost_flag = True
			index = random.randint(0, 1)
			if index == 0:
				boost_time = 75
			elif index == 1:
				boost_time = 113
			apple_count = 0

		#Điều kiện chỉ vẽ lên màn hình khi running == True: 
		if running == True:
		#Cập nhật rắn và mồi lên màn hình:
			screen.fill(WHITE)
			#Hiệu ứng particle khi đạt điểm nhất định
			if score >= 30:
				frwk.particles_generate(particles, screen, BLACK, snake_body[0][0] + frwk.head_img.get_width()/2, snake_body[0][1] + frwk.head_img.get_height()/2)

			for pos in snake_body[1:]: #Trừ đầu và đuôi
				screen.blit(frwk.body_img, pygame.Rect(pos[0], pos[1], m, m))

			head_img_copy = pygame.transform.rotate(frwk.head_img, angle)
			screen.blit(head_img_copy, pygame.Rect(snake_body[0][0], snake_body[0][1], m ,m)) #Đầu
			screen.blit(frwk.food_img, pygame.Rect(food_pos[0], food_pos[1], m, m)) #Thức ăn

			if boost_flag == True:
				#frwk.particles_generate(particles, screen, BLACK, boost_pos[0] + frwk.boost_img.get_width()/2, boost_pos[1] + frwk.boost_img.get_height()/2)
				if index == 0: #Score boost
					screen.blit(frwk.boost_img[0], pygame.Rect(boost_pos[0], boost_pos[1], m, m))
				elif index == 1: #Speed boost
					screen.blit(frwk.boost_img[1], pygame.Rect(boost_pos[0], boost_pos[1], m, m))

			if boost_flag == False and boost_time > 0:
				if index == 0:
					frwk.draw_text('x5 Score ', 'consolas', 15, False, RED, screen, ws[0]/20*7, 20)
					duration_bar = pygame.Rect(ws[0]/12*5, 18, round(boost_time*1.5), 20)
				elif index == 1:
					frwk.draw_text('x1.5 Speed ', 'consolas', 15, False, RED, screen, ws[0]/20*7, 20)
					duration_bar = pygame.Rect(ws[0]/12*5, 18, boost_time, 20)
				pygame.draw.rect(screen, RED, duration_bar)
			
			#Xử lý khi di chuyển chạm 4 cạnh biên, xử lý ở chế độ borderless
			#Vẽ biên:
			if choice == 0:
				pygame.draw.rect(screen, BLACK, (10,10, ws[0] - 20, ws[1] - 20), 2) #2 là độ dày của biên
				if snake_pos[0] > ws[0] - 30 or snake_pos[0] < 20:
					running, exit_to_menu, ws, screen = frwk.game_over(exit_to_menu, running, fullscreen, screen, ws, mainClock, framerate, score, high_score)
					if running == True:
						snake_pos = [100,60]
						snake_body = [[100,60], [80,60], [60,60]]
						score = 0
						direction = 'RIGHT'
						change_to = direction
						boost_flag = True
						index = random.randint(0, 1)
						if index == 0:
							boost_time = 75
						elif index == 1:
							boost_time = 113
					else:
						frwk.fade_out(frwk.get_win_size(screen), screen)
						break
				if snake_pos[1] > ws[1] - 30 or snake_pos[1] < 20:
					running, exit_to_menu, ws, screen = frwk.game_over(exit_to_menu, running, fullscreen, screen, ws, mainClock, framerate, score, high_score)
					if running == True:
						snake_pos = [100,60]
						snake_body = [[100,60], [80,60], [60,60]]
						score = 0
						direction = 'RIGHT'
						change_to = direction
						boost_flag = True
						index = random.randint(0, 1)
						if index == 0:
							boost_time = 75
						elif index == 1:
							boost_time = 113
					else:
						frwk.fade_out(frwk.get_win_size(screen), screen)
						break
			else:
				#Reset pos khi vượt quá Windows Size
				if snake_pos[0] > ws[0]:
					snake_pos[0] = -20
				elif snake_pos[0] < 0:
					snake_pos[0] = ws[0]
				elif snake_pos[1] > ws[1]:
					snake_pos[1] = -20
				elif snake_pos[1] < 0:
					snake_pos[1] = ws[1]
		else: break

		#Xử lý khi tự ăn chính mình:
		for part in snake_body[1:]:
			if snake_pos[0] == part[0] and snake_pos[1] == part[1]: #Khi đầu chạm vào bất kỳ phần nào của thân
				running, exit_to_menu, ws, screen = frwk.game_over(exit_to_menu, running, fullscreen, screen, ws, mainClock, framerate, score, high_score)
				if running == True:
					snake_pos = [100,60]
					snake_body = [[100,60], [80,60], [60,60]]
					score = 0
					direction = 'RIGHT'
					change_to = direction
					boost_flag = True
					index = random.randint(0, 1)
					if index == 0:
						boost_time = 75
					elif index == 1:
						boost_time = 113
				else:
					frwk.fade_out(frwk.get_win_size(screen), screen)
					break

		frwk.show_score(1, score, high_score, screen, ws)
		pygame.display.update()
		if boost_flag == False and boost_time > 0:
			if index == 1:
				mainClock.tick(15)
			elif index == 0:
				mainClock.tick(10)
		else:
			mainClock.tick(10)

#Gọi main menu để chạy cả chương trình
main_menu()