import pygame

# Constants.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def get_win_size(screen):
	win_size = (screen.get_width(), screen.get_height())
	return win_size

def flip(image, x_axis=True, y_axis=False):
	return pygame.transform.flip(image, x_axis, y_axis)

# pos is a tuple with two values x and y:
def blit_at_center(surf_a, surf_b, pos):
	x = int(surf_b.get_width() / 2)
	y = int(surf_b.get_height() / 2)
	surf_a.blit(surf_b, (pos[0] - x, pos[1] - y))

# Draw the light effect around particles.
def circle_to_surf(radius, color):
	surf = pygame.Surface((radius * 2, radius * 2))  # Light radius is doubled the particle radius.
	pygame.draw.circle(surf, color, (radius, radius), radius)  # Draw at the center.
	surf.set_colorkey(BLACK)
	return surf

# Draw text at midtop.
def draw_text(text, x, y, size, blit_surf, font_name="consolas", color=BLACK, bold=False):
	font = pygame.font.SysFont(font_name, size, bold)  # Get the font
	textobj = font.render(text, True, color)  # Render input text with that font
	textrect = textobj.get_rect()  # Get the font Rect object
	textrect.midtop = (x, y)  # Set the position to top center
	blit_surf.blit(textobj, textrect)  # Blit

# Draw rect at midtop.
def draw_rect(rect, draw_surface, color, x, y):
	rect.midtop = (x, y)
	pygame.draw.rect(draw_surface, color, rect)

# Fading out effect.
def fade_out(WINDOW_SIZE, draw_surface):
	fade_out = pygame.Surface(WINDOW_SIZE)
	fade_out.fill(WHITE)
	for alpha in range(0, 256):  # Set opaque value.
		fade_out.set_alpha(alpha)
		draw_surface.blit(fade_out, (0, 0))
		pygame.display.update()
		pygame.time.delay(4)  # The delay time.