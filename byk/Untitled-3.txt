import pygame
import sys
import os
import json



def draw_walls(walls):
    for wall in walls:
        screen.blit(wall.image, wall.rect.topleft)

# Create a list to store walls
walls = []

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

# Function to create a wall and add it to the walls list
def create_wall(x, y, width, height):
    wall = Wall(x, y, width, height)
    walls.append(wall)


# File to store settings
settings_file_path = os.path.join(os.path.expanduser("~"), "Documents", "My Games", "test_game", "settings.json")

# Function to load settings from file
def load_settings():
    if os.path.exists(settings_file_path):
        with open(settings_file_path, "r") as file:
            settings = json.load(file)
            return settings
    return {"music_volume": 0.5, "effect_volume": 0.5, "button_state": True, "sound_enabled": True}  # Default settings



# Function to save settings to file
def save_settings(settings):
    os.makedirs(os.path.dirname(settings_file_path), exist_ok=True)
    with open(settings_file_path, "w") as file:
        json.dump(settings, file)

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Получение размеров экрана
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h



# Цвета
WHITE = (255, 255, 255)
PINK = (255, 89, 118)
GRAY = (22, 67, 128)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Игра на Pygame")

# Установка стандартного курсора
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# Загрузка фоновой картинки
background_image = pygame.image.load("fon.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Загрузка изображений кнопок
button_normal = pygame.image.load("assets/ui (new)/menu_button.png")
button_pressed = pygame.image.load("assets/ui (new)/menu_button_press.png")
sound_on_icon = pygame.image.load(r"assets\ui (new)\pause_button.png")  # Replace with your sound on icon
sound_off_icon = pygame.image.load(r"assets\ui (new)\pause_button_press.png")  # Replace with your sound off icon

# Размеры кнопок
button_width = 200
button_height = 50
sound_icon_size = 30

# Масштабирование изображений кнопок
button_normal = pygame.transform.scale(button_normal, (button_width, button_height))
button_pressed = pygame.transform.scale(button_pressed, (button_width, button_height))
sound_on_icon = pygame.transform.scale(sound_on_icon, (sound_icon_size, sound_icon_size))
sound_off_icon = pygame.transform.scale(sound_off_icon, (sound_icon_size, sound_icon_size))

# Загрузка изображения для настроек
settings_image = pygame.image.load("assets/ui (new)/menu_settings.png")
settings_image = pygame.transform.scale(settings_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Инициализация звуков
pygame.mixer.music.load("your_background_music.mp3")
pygame.mixer.music.set_volume(0)
sound_effect = pygame.mixer.Sound("your_sound_effect.mp3")
sound_effect.set_volume(0.5)



# Глобальные переменные для управления звуком в настройках
sound_cursor_rect = pygame.Rect(0, 0, 30, 60)  # Изменил размеры sound_cursor_rect
sound_control_rect = pygame.Rect(0, 0, 400, 85)  # Изменил размеры sound_control_rect

# Флаги для управления кнопками
increase_button_pressed = False
decrease_button_pressed = False

# Загрузка фоновой картинки для игры
background_game_image = pygame.image.load("assets/levels/fon_DEFULT.png")
background_game_image = pygame.transform.scale(background_game_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Загрузка кадров анимации для персонажа (увеличенные в 3 раза)
knight_idle_frames = [pygame.transform.scale(pygame.image.load(f"assets\heroes\knight/knight_idle_anim_f{i}.png"), (50, 50)) for i in range(6)]

# Загрузка кадров анимации для ходьбы персонажа
knight_walk_frames = [pygame.transform.scale(pygame.image.load(f"assets\heroes\knight/knight_run_anim_f{i}.png"), (50, 50)) for i in range(6)]
walk_animation_speed = 100  # Скорость анимации ходьбы (в миллисекундах)
current_frame = 0


# Global variable for player facing direction
player_facing_left = False

def create_help_msg(text_help, image_keyboard_help=None):
    # Font for the text
    font = pygame.font.Font(None, 36)

    # Create a surface for the text
    text_surface = font.render(text_help, True, WHITE)
    
    # Get the width and height of the text surface
    text_width, text_height = text_surface.get_size()

    # Create a surface for the background (using a transparent background)
    background_surface = pygame.Surface((text_width + 20, text_height + 20), pygame.SRCALPHA)
    
    # Fill the background with a translucent black color
    pygame.draw.rect(background_surface, (0, 0, 0, 150), (0, 0, text_width + 20, text_height + 20))

    # Blit the text onto the background
    background_surface.blit(text_surface, (10, 10))

    # If an image is provided, blit it next to the text
    if image_keyboard_help:
        background_surface.blit(image_keyboard_help, (text_width + 30, (text_height - image_keyboard_help.get_height()) // 2 + 10))

    # Get the center position of the screen
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    # Get the position to blit the hint
    hint_x = center_x - (text_width + 20) // 2
    hint_y = center_y - (text_height + 20) // 2

    # Blit the background with text onto the screen
    screen.blit(background_surface, (hint_x, hint_y))


def play_game(running, walls):
    global current_frame, walk_animation_timer, player_facing_left
    walk_animation_timer = 0
    player_x, player_y = SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150
    player_width, player_height = 40, 20
    player_speed = 8
    running_speed = 12
    stamina = 10
    max_stamina = 40

    # Load the level image
    level_image = pygame.image.load("assets/levels/level_test_1.png")
    level_image = pygame.transform.scale(level_image, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))

    # Define the rectangle to center the level image within
    level_rect = level_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Update walk animation timer
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            walk_animation_timer = walk_animation_speed
        else:
            walk_animation_timer = 0

        # Temporarily store the player's new position
        new_player_x, new_player_y = player_x, player_y

        # Update player position based on key presses and running state
        if keys[pygame.K_a]:
            player_facing_left = True
            new_player_x -= running_speed if keys[pygame.K_LSHIFT] and stamina > 0 else player_speed
        elif keys[pygame.K_d]:
            player_facing_left = False
            new_player_x += running_speed if keys[pygame.K_LSHIFT] and stamina > 0 else player_speed

        if keys[pygame.K_w]:
            new_player_y -= running_speed if keys[pygame.K_LSHIFT] and stamina > 0 else player_speed
        elif keys[pygame.K_s]:
            new_player_y += running_speed if keys[pygame.K_LSHIFT] and stamina > 0 else player_speed

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # Create a temporary rectangle for the new player position
        new_player_rect = pygame.Rect(new_player_x, new_player_y + player_height + 5, player_width, player_height)

        # Check for collisions with walls
        player_collision = False
        for wall in walls:
            if new_player_rect.colliderect(wall.rect):
                player_collision = True
                break

        # Update the player's position if there are no collisions
        if not player_collision:
            player_x, player_y = new_player_x, new_player_y

        # Decrease stamina when running
        if keys[pygame.K_LSHIFT] and stamina > 0:
            stamina -= 1
        else:
            stamina = min(stamina + 0.5, max_stamina)

        screen.blit(background_game_image, (0, 0))
        screen.blit(level_image, level_rect)

        # Move this line outside the loop to draw help message after the background
        keyboard_image = pygame.image.load("assets/World Map/msg/10.png")

        create_help_msg("Use WASD keys to move", image_keyboard_help=keyboard_image)

        # Draw walls before drawing the player
        draw_walls(walls)

        if walk_animation_timer > 0:
            if player_facing_left:
                flipped_frame = pygame.transform.flip(knight_walk_frames[current_frame], True, False)
                screen.blit(flipped_frame, (player_x, player_y))
            else:
                screen.blit(knight_walk_frames[current_frame], (player_x, player_y))
            walk_animation_timer -= clock.get_rawtime()
            current_frame = (current_frame + 1) % len(knight_walk_frames)
        else:
            if player_facing_left:
                flipped_frame = pygame.transform.flip(knight_idle_frames[current_frame], True, False)
                screen.blit(flipped_frame, (player_x, player_y))
            else:
                screen.blit(knight_idle_frames[current_frame], (player_x, player_y))
            current_frame = (current_frame + 1) % len(knight_idle_frames)

        pygame.draw.rect(screen, (66, 135, 245), (10, 10, stamina, 20))
        pygame.draw.rect(screen, (0, 36, 94), (10 + stamina, 10, max_stamina - stamina, 20))

        pygame.display.flip()
        clock.tick(10)  # Set the desired frames per second

        # Clear the screen at the beginning of each iteration
        screen.fill((0, 0, 0))

        # Create walls and draw them
        create_wall(692, 300, 400, 50)
        create_wall(1083, 300, 200, 200)
        create_wall(640, 787, 610, 50)

        create_wall(1253, 300, 40, 500)

        create_wall(640, 300, 56, 300)
        create_wall(640, 590, 110, 113)
        create_wall(863, 590, 110, 113)
        create_wall(1083, 590, 200, 113)

    pygame.quit()
    sys.exit()












# Функция отрисовки кнопок и названия игры
def draw_interface():
    # Отрисовка фона
    screen.blit(background_image, (0, 0))

    # Отрисовка названия игры
    font_title = pygame.font.Font(None, 72)
    title_text = font_title.render("ВАШЕ НАЗВАНИЕ ИГРЫ", True, PINK)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 50))

    # Расположение кнопок
    start_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 - 50, button_width, button_height)
    exit_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 150, button_width, button_height)
    sound_button_rect = pygame.Rect(10, 10, sound_icon_size, sound_icon_size)

    # Проверка наведения мыши на кнопки и изменение изображения кнопок
    start_button_image = button_pressed if start_button_rect.collidepoint(pygame.mouse.get_pos()) else button_normal
    exit_button_image = button_pressed if exit_button_rect.collidepoint(pygame.mouse.get_pos()) else button_normal

    # Отрисовка кнопок
    screen.blit(start_button_image, (start_button_rect.x, start_button_rect.y))
    screen.blit(exit_button_image, (exit_button_rect.x, exit_button_rect.y))

    # Отрисовка текста на кнопках
    font_button = pygame.font.Font(None, 36)
    start_text = font_button.render("Играть", True, GRAY)
    exit_text = font_button.render("Выйти", True, GRAY)

    screen.blit(start_text, (start_button_rect.centerx - start_text.get_width() // 2, start_button_rect.centery - start_text.get_height() // 2))
    screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2, exit_button_rect.centery - exit_text.get_height() // 2))

    # Отрисовка кнопки звука
    sound_button_image = sound_off_icon if not sound_enabled else sound_on_icon
    screen.blit(sound_button_image, (sound_button_rect.x, sound_button_rect.y))

# Главный игровой цикл
running = True
clock = pygame.time.Clock()

# Воспроизведение музыки перед входом в цикл
pygame.mixer.music.play()

# Глобальные переменные управления звуком
settings = load_settings()
print("Loaded settings:", settings)  # Add this line to print loaded settings
music_volume = settings.get("music_volume", 0.5)
effect_volume = settings.get("effect_volume", 0.5)
button_state = settings.get("button_state", False)
sound_enabled = settings.get("sound_enabled", True)  # Use the value from the settings




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            start_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 - 50, button_width, button_height)
            exit_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 150, button_width, button_height)
            sound_button_rect = pygame.Rect(10, 10, sound_icon_size, sound_icon_size)

            if start_button_rect.collidepoint(mouse_x, mouse_y):
                play_game(running, walls)
            elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                running = False
            # Inside the event handling loop
            elif sound_button_rect.collidepoint(mouse_x, mouse_y):
                button_state = not button_state
                settings["button_state"] = button_state
                settings["sound_enabled"] = button_state  # Update "sound_enabled" key
                save_settings(settings)
                print("Saved settings:", settings)  # Add this line to print saved settings
                print("Updated button_state:", button_state)
                print("Updated sound_enabled:", sound_enabled)
                if button_state:
                    pygame.mixer.music.set_volume(music_volume)
                else:
                    pygame.mixer.music.set_volume(0)


        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                increase_button_pressed = True
            elif event.key == pygame.K_DOWN:
                decrease_button_pressed = True
            elif event.key == pygame.K_SPACE:
                button_state = not button_state
                settings["button_state"] = button_state
                save_settings(settings)
                print("Saved settings:", settings)  # Add this line to print saved settings
                print("Updated button_state:", button_state)
                print("Updated sound_enabled:", sound_enabled)
                if button_state:
                    pygame.mixer.music.set_volume(music_volume)
                else:
                    pygame.mixer.music.set_volume(0)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                increase_button_pressed = False
            elif event.key == pygame.K_DOWN:
                decrease_button_pressed = False

    # Move these lines inside the while loop to ensure sound_button_rect is defined
    sound_button_rect = pygame.Rect(10, 10, sound_icon_size, sound_icon_size)
    sound_button_image = sound_off_icon if not sound_enabled else sound_on_icon
    screen.blit(sound_button_image, (sound_button_rect.x, sound_button_rect.y))

    draw_interface()

    # Отображение изменений
    pygame.display.flip()

    # Ожидание
    clock.tick(30)  # 30 кадров в секунду

# Завершение работы Pygame
pygame.quit()
sys.exit()
