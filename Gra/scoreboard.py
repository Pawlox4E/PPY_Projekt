import sys

import pygame

from Button import Button


def draw_scoreboard(surface, font, scores, WINDOW_WIDTH, WINDOW_HEIGHT):
    scoreboard_width = WINDOW_WIDTH // 2
    scoreboard_height = WINDOW_HEIGHT // 2
    scoreboard_surface = pygame.Surface((scoreboard_width, scoreboard_height))
    scoreboard_surface.set_alpha(200)
    scoreboard_surface.fill((0, 0, 0))

    title_text = font.render("Scoreboard", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(scoreboard_width // 2, 30))
    scoreboard_surface.blit(title_text, title_rect)


    for i, score in enumerate(scores):
        score_text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(scoreboard_width // 2, 80 + i * 40))
        scoreboard_surface.blit(score_text, score_rect)

    surface.blit(scoreboard_surface, (WINDOW_WIDTH // 2 - scoreboard_width // 2, WINDOW_HEIGHT // 2 - scoreboard_height // 2))

def scoreboard(screen, font, background_image, background_rect, WINDOW_WIDTH, WINDOW_HEIGHT):
    running = True
    move_left = True
    clock = pygame.time.Clock()

    # Example scores
    scores = ["Player1: 1000", "Player2: 900", "Player3: 800", "Player4: 700"]
    quitButton = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.80, WINDOW_WIDTH * 0.2, WINDOW_HEIGHT * 0.1, "QUIT", font,
                        (255, 255, 255), pygame.image.load("images/menu/button_background1.png").convert_alpha())

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_image, background_rect)
        quitButton.draw(screen)

        if move_left:
            background_rect.x -= 1
            if background_rect.right <= WINDOW_WIDTH:
                move_left = False
        else:
            background_rect.x += 1
            if background_rect.left >= 0:
                move_left = True

        draw_scoreboard(screen, font, scores, WINDOW_WIDTH, WINDOW_HEIGHT)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if quitButton.check_click(mousePos):
                    running = False

        pygame.display.update()
        clock.tick(60)
