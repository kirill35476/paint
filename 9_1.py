import pygame
from all_colors import *

pygame.init()

size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Рисовать с прямоугольниками")
BACKGROUND = (255, 255, 255)
brush_color = (0, 0, 0)
brush_width = 5

BORDER_COLOR = (0, 0, 0)
CUR_INDEX = 0

canvas = pygame.Surface(screen.get_size())
canvas.fill(BACKGROUND)

COLORS = [BLACK, WHITE, RED, GREEN, YELLOW, CYAN, MAGENTA, GRAY,
          ORANGE, PINK, BROWN, PURPLE, LIME, NAVY, OLIVE, MAROON, TEAL, COLD]

size = 50
palette_rect = pygame.Rect(10, 10, size * 12, size)
palette = pygame.Surface(palette_rect.size)


drawing_rect = False
rect_start_pos = None
force_square = False


def draw_palette():
    palette.fill(BACKGROUND)
    for i in range(12):
        color_rect = pygame.Rect(i * size, 0, size, size)
        pygame.draw.rect(palette, COLORS[i], color_rect)

    border_rect = pygame.Rect(CUR_INDEX * size, 0, size, size)
    pygame.draw.rect(palette, BORDER_COLOR, border_rect, width=3)
    screen.blit(palette, palette_rect.topleft)


dragging_palette = False

FPS = 60
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if palette_rect.collidepoint(event.pos):
                    dragging_palette = True
                    offset = (event.pos[0] - palette_rect.left,
                              event.pos[1] - palette_rect.top)
                else:

                    drawing_rect = True
                    rect_start_pos = event.pos

            elif event.button == 1:
                if palette_rect.collidepoint(event.pos):
                    selected_color_index = ((event.pos[0] - palette_rect.left) // size)
                    CUR_INDEX = selected_color_index
                    brush_color = COLORS[CUR_INDEX]

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                dragging_palette = False
                if drawing_rect:

                    end_pos = event.pos
                    x = min(rect_start_pos[0], end_pos[0])
                    y = min(rect_start_pos[1], end_pos[1])
                    width = abs(end_pos[0] - rect_start_pos[0])
                    height = abs(end_pos[1] - rect_start_pos[1])

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        size_square = max(width, height)
                        width = height = size_square
                    pygame.draw.rect(canvas, brush_color,
                                     (x, y, width, height))

                    pygame.draw.rect(canvas, BORDER_COLOR,
                                     (x, y, width, height), 1)
                    drawing_rect = False
                    rect_start_pos = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                force_square = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                force_square = False

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    if mouse_pressed[0] and not palette_rect.collidepoint(mouse_pos):
        pygame.draw.circle(canvas, brush_color, mouse_pos, brush_width)

    if dragging_palette:
        new_pos = (mouse_pos[0] - offset[0],
                   mouse_pos[1] - offset[1])
        palette_rect.topleft = new_pos

    screen.blit(canvas, (0, 0))
    if drawing_rect and rect_start_pos:
        current_pos = mouse_pos
        x = min(rect_start_pos[0], current_pos[0])
        y = min(rect_start_pos[1], current_pos[1])
        width = abs(current_pos[0] - rect_start_pos[0])
        height = abs(current_pos[1] - rect_start_pos[1])

        if force_square:
            size_square = max(width, height)
            width = height = size_square

        pygame.draw.rect(screen, brush_color,
                         (x, y, width, height), 2)

        pygame.draw.rect(screen, BORDER_COLOR,
                         (x, y, width, height), 1)

    draw_palette()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
