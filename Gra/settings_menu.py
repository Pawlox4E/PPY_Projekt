import pygame
import sys
from Button import Button
from SliderButton import SliderButton, DiscreteSliderButton, LinkedDiscreteSliderButton
from usefull_methods import read_settings, save_settings_to_file


def settings_menu(screen, font, background_image, background_rect, WINDOW_WIDTH, WINDOW_HEIGHT):
    running = True
    move_left = True
    clock = pygame.time.Clock()
    background = pygame.image.load("images/menu/button_background1.png").convert_alpha()
    slider = pygame.image.load("images/menu/button_background.png").convert_alpha()

    # Tworzenie suwaków
    volume_slider = SliderButton(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.25, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.1, read_settings("VOLUME"), 100, font, (255, 255, 255), background, slider, "VOLUME")
    brightness_slider = SliderButton(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.35, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.1, read_settings("BRIGHTNESS"), 100, font, (255, 255, 255), background, slider, "BRIGHTNESS")
    font_slider = DiscreteSliderButton(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.45, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.1, read_settings("FONT_SIZE"), [1, 2, 3, 4], font, (255, 255, 255), background, slider, "FONT_SIZE")
    fps_slider = DiscreteSliderButton(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.55, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.1, read_settings("FPS"), [30, 60, 120], font, (255, 255, 255), background, slider, "FPS")
    width_slider = LinkedDiscreteSliderButton(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.65, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.1, read_settings("WIDTH"), [320, 640, 1024, 1240, 1920, 2560], font, (255, 255, 255), background, slider, "WIDTH")
    height_slider = LinkedDiscreteSliderButton(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.75, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.1, read_settings("HEIGHT"), [200, 480, 768, 800, 1080, 1440], font, (255, 255, 255), background, slider, "HEIGHT",width_slider)
    width_slider.link(height_slider)
    quitButton = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.85, WINDOW_WIDTH * 0.2, WINDOW_HEIGHT * 0.1, "QUIT", font, (255, 255, 255), background)

    sliders = [volume_slider,brightness_slider,font_slider,fps_slider, width_slider, height_slider]
    settings = {
        "VOLUME": read_settings("VOLUME"),
        "BRIGHTNESS": read_settings("BRIGHTNESS"),
        "FONT_SIZE": read_settings("FONT_SIZE"),
        "FPS": read_settings("FPS"),
        "WIDTH": read_settings("WIDTH"),
        "HEIGHT": read_settings("HEIGHT"),
        "TILE_SIZE": read_settings("TILE_SIZE"),
        "DIFFICULTY": read_settings("DIFFICULTY")
    }
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
                    settings[slider.text] = int(slider.get_selected_value())
                    save_settings_to_file(settings)
            elif event.type == pygame.MOUSEBUTTONUP:
                for slider in sliders:
                    slider.release()
                    settings[slider.text] = int(slider.get_selected_value())
                    save_settings_to_file(settings)
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