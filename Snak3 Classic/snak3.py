import pygame
from pygame.locals import *

import sys
import random

import assets.utility_funcs as util
import assets.framework as frwk

# Khởi tạo pygame
pygame.init()

# Khởi tạo mixer phát âm thanh
pygame.mixer.pre_init(44100, -16, 2, 512)

# FPS
mainClock = pygame.time.Clock()
framerate = 60

# Các hằng
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (152, 152, 152)
MEDIUM_GREY = (170, 170, 170)
LIGHT_GREY = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (65, 105, 255)
YELLOW = (224, 208, 31)
monitor_size = [pygame.display.Info().current_w,
				pygame.display.Info().current_h]

# Tạo cửa sổ
pygame.display.set_caption('Snak3: Classic')
pygame.display.set_icon(pygame.image.load('assets/images/snak3.png'))
screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
ws = [screen.get_width(), screen.get_height()]  # Window Size

# Load hình ảnh, âm thanh, nhạc:
m = 20  # The size of single unit
pygame.mixer.music.load('assets/musics/Blues.ogg')
pygame.mixer.music.set_volume(0.5)

# Define the data type of the variables:
music_on = False  # A flag to check if the music is on or not
fullscreen = False  # Fullscreen flag
res_w = 0  # The width of the current resolution
res_h = 0  # The height of the current resolution

# Set allowed events to be placed on the queue.
pygame.event.set_blocked(None)  # Block all the events.
pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, KEYDOWN, VIDEORESIZE])  # Allow these specific events.

# Hàm menu chính:
def main_menu():
	global screen, music_on, res_w, res_h, fullscreen
	shockwaves = []  # A List that stores shockwave attributes

	music_on, fullscreen, res_w, res_h = frwk.read_file('data/user_config.txt')

	if fullscreen:
		screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
		ws = [screen.get_width(), screen.get_height()]
	else:
		screen = pygame.display.set_mode((res_w, res_h), pygame.RESIZABLE)
		ws = [screen.get_width(), screen.get_height()]

	if music_on:
		pygame.mixer.music.play(-1)

	click = False  # Click flag
	alpha = 0  # Alpha value for transparent effect

	while True:
		# Lắp đầy màn hình bằng màu trằng
		screen.fill(WHITE)

		# Lấy vị trí của chuột:
		mx, my = pygame.mouse.get_pos()

		# Tiêu đề:
		util.draw_text('SNAK3: CLASSIC', ws[0] / 2, ws[1] / 6, 50, screen, bold=True)

		# Nút bấm:
		button_1 = pygame.Rect(300, 240, 270, 50)
		util.draw_rect(button_1, screen, GREY, ws[0] / 2, ws[1] / 5 * 2)
		util.draw_text('Casual Mode', ws[0] / 2, ws[1] / 12 * 5, 30, screen)
		
		if button_1.collidepoint((mx, my)):  # Khi dí trỏ chuột vào
			util.draw_rect(button_1, screen, MEDIUM_GREY, ws[0] / 2, ws[1] / 5 * 2)
			util.draw_text('Casual Mode', ws[0] / 2, ws[1] / 12 * 5, 30, screen, color=YELLOW)
			if click:  # Khi bấm chuột vào
				util.fade_out(util.get_win_size(screen), screen)
				game(0)
				alpha = 255


		button_2 = pygame.Rect(165, 300, 270, 50)
		util.draw_rect(button_2, screen, GREY, ws[0] / 2, ws[1] / 2)
		util.draw_text('Borderless Mode', ws[0] / 2, ws[1] / 60 * 31, 30, screen)
		
		if button_2.collidepoint((mx, my)):
			util.draw_rect(button_2, screen, MEDIUM_GREY, ws[0] / 2, ws[1] / 2)
			util.draw_text('Borderless Mode', ws[0] / 2, ws[1] / 60 * 31, 30, screen, color=YELLOW)
			if click:
				util.fade_out(util.get_win_size(screen), screen)
				game(1)
				alpha = 255


		button_3 = pygame.Rect(165, 300, 270, 50)
		util.draw_rect(button_3, screen, GREY, ws[0] / 2, ws[1] / 5 * 3)
		util.draw_text('Settings', ws[0] / 2, ws[1] / 60 * 37, 30, screen)
		
		if button_3.collidepoint((mx, my)):  # Khi dí trỏ chuột vào
			util.draw_rect(button_3, screen, MEDIUM_GREY, ws[0] / 2, ws[1] / 5 * 3)
			util.draw_text('Settings', ws[0] / 2, ws[1] / 60 * 37, 30, screen, color=YELLOW)
			if click:  # Khi bấm chuột vào
				util.fade_out(util.get_win_size(screen), screen)
				screen, ws = frwk.show_settings(music_on, fullscreen, res_w, res_h, util.get_win_size(screen), monitor_size, screen, ws, mainClock, framerate)
				alpha = 255


		button_4 = pygame.Rect(165, 300, 270, 50)
		util.draw_rect(button_4, screen, GREY, ws[0] / 2, ws[1] / 10 * 7)
		util.draw_text('Quit', ws[0] / 2, ws[1] / 60 * 43, 30, screen)
		
		if button_4.collidepoint((mx, my)):  # Khi dí trỏ chuột vào
			util.draw_rect(button_4, screen, MEDIUM_GREY, ws[0] / 2, ws[1] / 10 * 7)
			util.draw_text('Quit', ws[0] / 2, ws[1] / 60 * 43, 30, screen, color=YELLOW)
			if click:  # Khi bấm chuột vào
				pygame.quit()
				sys.exit()


		util.draw_text('© by Constance, v1.0', ws[0] / 2, ws[1] - 15, 15, screen)

		frwk.shockwaves_generate(shockwaves, click, mx, my, screen, BLACK)

		if alpha > 0:
			if alpha == 255:
				fade_in = pygame.Surface(util.get_win_size(screen))
				fade_in.fill(WHITE)
				shockwaves.clear()  # Reset the shockwaves list

			fade_in.set_alpha(alpha)
			screen.blit(fade_in, (0, 0))
			alpha -= 15

		click = False
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == MOUSEBUTTONDOWN:
				if event.button == 1:  # Khi bấm chuột trái
					click = True
			if event.type == VIDEORESIZE:
				if not fullscreen:
					screen = pygame.display.set_mode(
						(event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		pygame.display.update()
		mainClock.tick(framerate)


# Hàm game:
def game(choice):
	global screen, ws
	# Khai báo biến:
	snake_pos = [100, 60]  # Vị trí ban đầu của con rắn
	# Vị trí các phần đầu, thân, đuôi
	snake_body = [[100, 60], [80, 60], [60, 60]]

	# Thức ăn
	food_x = random.randrange(2, int(ws[0] / 10 - 3))
	food_y = random.randrange(3, int(ws[1] / 10 - 3))
	if food_x % 2 != 0:
		food_x += 1  # Nếu là số lẻ thì tăng lên 1
	if food_y % 2 != 0:
		food_y += 1
	food_pos = [food_x * 10, food_y * 10]  # Food position
	food_flag = True  # Cờ thức ăn, kiểm tra rắn có ăn dc mồi hay ko

	# Boost
	boost_x = random.randrange(2, int(ws[0] / 10 - 3))
	boost_y = random.randrange(3, int(ws[1] / 10 - 3))
	if boost_x % 2 != 0:
		boost_x += 1
	if boost_y % 2 != 0:
		boost_y += 1
	if boost_x == food_x and boost_y == food_y:
		boost_x += 20
		if boost_x == ws[0] - 30:
			boost_x -= 20
	boost_pos = [boost_x * 10, boost_y * 10]  # Boost position
	boost_flag = True

	direction = 'RIGHT'  # Starting direction
	change_to = direction  # Đổi hướng di chuyển
	score = 0
	high_score = 0
	apple_count = 0  # Checking when will the boost respawn
	exit_to_menu = False  # Exit to menu flag
	running = True  # Running state
	# Index for the type of boost: 0 for score x5, 1 for speed x1.5
	index = random.randint(0, 1)
	if index == 0:
		boost_time = 75
	elif index == 1:
		boost_time = 113
	particles = []  # A list that stores particle attributes

	# Vòng lặp chính:
	while running:
		# Hiệu quả buff khi nhặt boost:

		if snake_pos[0] == boost_pos[0] and snake_pos[1] == boost_pos[1]:
			if boost_flag:
				frwk.boost_sound.play()
			boost_flag = False

		if not boost_flag:
			boost_time -= 1

		if exit_to_menu:
			running = False
			util.fade_out(util.get_win_size(screen), screen)

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					exit_to_menu, ws, screen = frwk.pause_menu(exit_to_menu, fullscreen, util.get_win_size(screen), screen, ws, mainClock, framerate)
					# running = False  # Ấn escape sẽ trở về menu
				if event.key == K_d:
					change_to = 'RIGHT'
				if event.key == K_a:
					change_to = 'LEFT'
				if event.key == K_w:
					change_to = 'UP'
				if event.key == K_s:
					change_to = 'DOWN'
			if event.type == VIDEORESIZE:
				if not fullscreen:
					screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
					ws = [screen.get_width(), screen.get_height()]

		# Hướng đi: tránh rắn đi ngược lại, đi lùi
		if change_to == 'RIGHT' and direction != 'LEFT':
			direction = 'RIGHT'
		if change_to == 'LEFT' and direction != 'RIGHT':
			direction = 'LEFT'
		if change_to == 'UP' and direction != 'DOWN':
			direction = 'UP'
		if change_to == 'DOWN' and direction != 'UP':
			direction = 'DOWN'

		# Góc xoay, số (+) là ngược chiều kim đồng hồ, (-) là thuận chiều kim đồng hồ
		angle = 0
		# Cập nhật vị trí mới:
		if direction == 'RIGHT':  # Mặc định hình ảnh nằm ngang
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

		# Thêm khúc dài ra khi ăn:
		# Chèn vị trí vào phần tử thứ 1 trong list body
		snake_body.insert(0, list(snake_pos))
		if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:  # Khi 2 tọa đồ trùng nhau
			frwk.eating_sound.play()
			if not boost_flag:
				apple_count += 1
			if not boost_flag and boost_time > 0:
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

		# Sản sinh mồi:
		if not food_flag:  # Nếu ăn dc rồi, thì tạo vị trí mới cho mồi
			food_x = random.randrange(2, int(ws[0] / 10 - 3))
			food_y = random.randrange(3, int(ws[1] / 10 - 3))
			if food_x % 2 != 0:
				food_x += 1
			if food_y % 2 != 0:
				food_y += 1
			food_pos = [food_x * 10, food_y * 10]
			food_flag = True

		# Sản sinh vị trí boost mới:
		if not boost_flag:
			boost_x = random.randrange(2, int(ws[0] / 10 - 3))
			boost_y = random.randrange(3, int(ws[1] / 10 - 3))
			if boost_x % 2 != 0:
				boost_x += 1
			if boost_y % 2 != 0:
				boost_y += 1
			if boost_x == food_x and boost_y == food_y:
				boost_x += 20
				if boost_x == ws[0] - 30:
					boost_x -= 20
			boost_pos = [boost_x * 10, boost_y * 10]

		# Reset flag khi ăn đủ 10 trái táo
		if apple_count == 10:
			boost_flag = True
			index = random.randint(0, 1)
			if index == 0:
				boost_time = 75
			else:
				boost_time = 113
			apple_count = 0

		# Điều kiện chỉ vẽ lên màn hình khi running == True:
		if running:
			# Cập nhật rắn và mồi lên màn hình:
			screen.fill(WHITE)

			# Hiệu ứng particle khi đạt điểm nhất định
			if score >= 30:
				frwk.particles_generate(particles, screen, BLACK, snake_body[0][0] + frwk.head_img.get_width() / 2, snake_body[0][1] + frwk.head_img.get_height() / 2)

			for pos in snake_body[1:]:  # Trừ đầu
				screen.blit(frwk.body_img, pygame.Rect(pos[0], pos[1], m, m))

			head_img_copy = pygame.transform.rotate(frwk.head_img, angle)
			screen.blit(head_img_copy, pygame.Rect(snake_body[0][0], snake_body[0][1], m, m))  # Đầu
			screen.blit(frwk.food_img, pygame.Rect(food_pos[0], food_pos[1], m, m))  # Thức ăn

			# Vẽ boost
			if boost_flag:
				if index == 0:  # Score boost
					screen.blit(frwk.boost_img[0], pygame.Rect(boost_pos[0], boost_pos[1], m, m))
				else:  # Speed boost
					screen.blit(frwk.boost_img[1], pygame.Rect(boost_pos[0], boost_pos[1], m, m))

			# Vẽ thanh hiệu lực của boost
			if not boost_flag and boost_time > 0:
				if index == 0:
					util.draw_text('x5 Score ', ws[0] / 20 * 7, 20, 15, screen, color=RED)
					duration_bar = pygame.Rect(ws[0] / 12 * 5, 18, round(boost_time * 1.5), 20)
				else:
					util.draw_text('x1.5 Speed ', ws[0] / 20 * 7, 20, 15, screen, color=RED)
					duration_bar = pygame.Rect(ws[0] / 12 * 5, 18, boost_time, 20)
				pygame.draw.rect(screen, RED, duration_bar)

			# Xử lý khi di chuyển chạm 4 cạnh biên, xử lý ở chế độ borderless
			# Casual Mode:
			if choice == 0:
				# 2 là độ dày của biên
				pygame.draw.rect(screen, BLACK, (10, 10, ws[0] - 20, ws[1] - 20), 2)
				# X axis
				if snake_pos[0] > ws[0] - 30 or snake_pos[0] < 20:
					running, exit_to_menu, ws, screen = frwk.game_over(exit_to_menu, running, fullscreen, screen, ws, mainClock, framerate, score, high_score)
					if running:
						snake_pos = [100, 60]
						snake_body = [[100, 60], [80, 60], [60, 60]]
						score = 0
						apple_count = 0
						direction = 'RIGHT'
						change_to = direction
						boost_flag = True
						index = random.randint(0, 1)
						if index == 0:
							boost_time = 75
						else:
							boost_time = 113
					else:
						util.fade_out(util.get_win_size(screen), screen)
						break
				# Y Axis
				if snake_pos[1] > ws[1] - 30 or snake_pos[1] < 20:
					running, exit_to_menu, ws, screen = frwk.game_over(exit_to_menu, running, fullscreen, screen, ws, mainClock, framerate, score, high_score)
					if running:
						snake_pos = [100, 60]
						snake_body = [[100, 60], [80, 60], [60, 60]]
						score = 0
						direction = 'RIGHT'
						change_to = direction
						boost_flag = True
						index = random.randint(0, 1)
						if index == 0:
							boost_time = 75
						else:
							boost_time = 113
					else:
						util.fade_out(util.get_win_size(screen), screen)
						break
			# Borderless Mode
			else:
				# Reset pos khi vượt quá Windows Size
				if snake_pos[0] > ws[0]:
					snake_pos[0] = -20
				elif snake_pos[0] < 0:
					snake_pos[0] = ws[0]
				elif snake_pos[1] > ws[1]:
					snake_pos[1] = -20
				elif snake_pos[1] < 0:
					snake_pos[1] = ws[1]
		# If not running then stop drawing
		else:
			break

		# Xử lý khi tự ăn chính mình:
		for part in snake_body[1:]:  # Make a copy of a list
			# Khi đầu chạm vào bất kỳ phần nào của thân
			if snake_pos[0] == part[0] and snake_pos[1] == part[1]:
				running, exit_to_menu, ws, screen = frwk.game_over(exit_to_menu, running, fullscreen, screen, ws, mainClock, framerate, score, high_score)
				if running:
					snake_pos = [100, 60]
					snake_body = [[100, 60], [80, 60], [60, 60]]
					score = 0
					direction = 'RIGHT'
					change_to = direction
					boost_flag = True
					index = random.randint(0, 1)
					if index == 0:
						boost_time = 75
					else:
						boost_time = 113
				else:
					util.fade_out(util.get_win_size(screen), screen)
					break

		frwk.show_score(1, score, high_score, screen, ws)
		pygame.display.update()
		if not boost_flag and boost_time > 0:
			if index == 1:
				mainClock.tick(15)
			else:
				mainClock.tick(10)
		else:
			mainClock.tick(10)


# Gọi main menu để chạy cả chương trình khi và chỉ khi snak3.py là chương trình chính.
if __name__ == '__main__':
	main_menu()
