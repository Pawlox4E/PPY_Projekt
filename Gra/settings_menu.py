import pygame
import sys
from Button import Button
from SliderButton import SliderButton
from SliderButton import DiscreteSliderButton


def save_settings_to_file(settings, file_path):
    with open(file_path, 'w') as file:
        for key, value in settings.items():
            file.write(f"{key}={value}\n")


def settings_menu(screen, font, background_image, background_rect, WINDOW_WIDTH):
    running = True
    move_left = True
    clock = pygame.time.Clock()
    background = pygame.image.load("images/menu/button_background1.png").convert_alpha()
    slider = pygame.image.load("images/menu/button_background.png").convert_alpha()

    # Tworzenie suwaków
    volume_slider = SliderButton(WINDOW_WIDTH/2, 275, 500, 100, 50, 100, font, (255, 255, 255), background,slider,"VOLUME")
    brightness_slider = SliderButton(WINDOW_WIDTH/2, 375, 500, 100, 75, 100, font, (255, 255, 255), background,slider,"BRIGHTNESS")
    contrast_slider = SliderButton(WINDOW_WIDTH/2, 475, 500, 100, 35, 100, font, (255, 255, 255), background,slider,"CONTRAST")

    #volume, brightness,contrast
    fps_slider = DiscreteSliderButton(WINDOW_WIDTH/2, 575, 500, 100, 60, [30,60,120], font, (255, 255, 255), background,slider,"FPS")
    width_slider = DiscreteSliderButton(WINDOW_WIDTH/2, 675, 500, 100, 75, [320,640,1024,1240,1920,2560], font, (255, 255, 255), background,slider,"WIDTH")
    height_slider = DiscreteSliderButton(WINDOW_WIDTH/2, 775, 500, 100, 35, [200,480,768,800,1080,1440], font, (255, 255, 255), background,slider,"HEIGHT")
    quitButton = Button(WINDOW_WIDTH // 2, 875, 400, 100, "Quit", font, (255,255,255), background)

    sliders = [volume_slider,brightness_slider,contrast_slider,fps_slider, width_slider, height_slider]

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_image, background_rect)

        if move_left:
            background_rect.x -= 1
            if background_rect.right <= WINDOW_WIDTH:
                move_left = False
        else:
            background_rect.x += 1
            if background_rect.left >= 0:
                move_left = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if quitButton.check_click(mouse_pos):
                    running = False
                for slider in sliders:
                    slider.check_click(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                for slider in sliders:
                    slider.release()
            elif event.type == pygame.MOUSEMOTION:
                mouse_x = event.pos[0]
                for slider in sliders:
                    if slider.is_dragging:
                        slider.move_slider(mouse_x)

        for slider in sliders:
            slider.draw(screen)
        quitButton.draw(screen)

        pygame.display.update()
        clock.tick(60)

