import pygame
import sys
import os
import json

walk_animation_timer = 0
player_width, player_height = 40, 20
player_speed = 8
running_speed = 12
stamina = 10
max_stamina = 40

walls = []
barriers = []

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, walk_frames, idle_frames):
        super().__init__()
        self.walk_frames = walk_frames
        self.idle_frames = idle_frames
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.current_frame = 0
        self.walk_animation_timer = 0
        self.facing_left = False
        self.stamina = 10  # Make stamina an instance variable
        self.max_stamina = 40

    def update(self, keys, walls):
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            self.walk_animation_timer = walk_animation_speed
        else:
            self.walk_animation_timer = 0

        new_player_x, new_player_y = self.rect.topleft

        if keys[pygame.K_a]:
            self.facing_left = True
            new_player_x -= running_speed if keys[pygame.K_LSHIFT] and self.stamina > 0 else player_speed
        elif keys[pygame.K_d]:
            self.facing_left = False
            new_player_x += running_speed if keys[pygame.K_LSHIFT] and self.stamina > 0 else player_speed

        if keys[pygame.K_w]:
            new_player_y -= running_speed if keys[pygame.K_LSHIFT] and self.stamina > 0 else player_speed
        elif keys[pygame.K_s]:
            new_player_y += running_speed if keys[pygame.K_LSHIFT] and self.stamina > 0 else player_speed

        new_rect = pygame.Rect(new_player_x, new_player_y + self.rect.height + 5, self.rect.width, self.rect.height)
        player_collision = any(new_rect.colliderect(wall.rect) for wall in walls)

        if not player_collision:
            self.rect.topleft = new_player_x, new_player_y

        if keys[pygame.K_LSHIFT] and self.stamina > 0:
            self.stamina -= 1
        else:
            self.stamina = min(self.stamina + 0.5, self.max_stamina)

    def draw(self, screen):
        if self.walk_animation_timer > 0:
            if self.facing_left:
                flipped_frame = pygame.transform.flip(self.walk_frames[self.current_frame], True, False)
                screen.blit(flipped_frame, self.rect.topleft)
            else:
                screen.blit(self.walk_frames[self.current_frame], self.rect.topleft)
            self.walk_animation_timer -= clock.get_rawtime()
            self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
        else:
            if self.facing_left:
                flipped_frame = pygame.transform.flip(self.idle_frames[self.current_frame], True, False)
                screen.blit(flipped_frame, self.rect.topleft)
            else:
                screen.blit(self.idle_frames[self.current_frame], self.rect.topleft)
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)



class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, message):
        super().__init__()
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.message = message

    def display_message(self, screen):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.message, True, WHITE)
        text_width, text_height = text_surface.get_size()
        background_surface = pygame.Surface((text_width + 20, text_height + 20), pygame.SRCALPHA)
        pygame.draw.rect(background_surface, (0, 0, 0, 150), (0, 0, text_width + 20, text_height + 20))
        background_surface.blit(text_surface, (10, 10))
        screen.blit(background_surface, ((SCREEN_WIDTH - text_width - 20) // 2, SCREEN_HEIGHT - text_height - 40))




def draw_walls(walls):
    for wall in walls:
        screen.blit(wall.image, wall.rect.topleft)


def create_wall(x, y, width, height):
    wall = Wall(x, y, width, height)
    walls.append(wall)


def create_help_msg(text_help, x, y, image_keyboard_help=None):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text_help, True, WHITE)
    text_width, text_height = text_surface.get_size()
    background_surface = pygame.Surface((text_width + 20, text_height + 20), pygame.SRCALPHA)
    pygame.draw.rect(background_surface, (0, 0, 0, 150), (0, 0, text_width + 20, text_height + 20))
    background_surface.blit(text_surface, (10, 10))

    if image_keyboard_help:
        background_surface.blit(image_keyboard_help, (text_width + 30, (text_height - image_keyboard_help.get_height()) // 2 + 10))

    screen.blit(background_surface, (x, y))



def Home(running, walls, player, barriers):
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

        player.update(keys, walls)

        screen.blit(background_game_image, (0, 0))
        screen.blit(level_image, level_rect)
        # create_help_msg("Use WASD keys to move")
        create_help_msg("Use WASD keys to move", 750, 470)

        create_help_msg("<", 100, 470)

        draw_walls(walls)
        player.draw(screen)

        # Check if the player touches any barriers
        for barrier in barriers:
            if player.rect.colliderect(barrier.rect):
                barrier.display_message(screen)
                if keys[pygame.K_e]:  # Check if the player presses 'E'
                    # Move the player to a new location (change these coordinates accordingly)
                    player.rect.topleft = (500, 500)
                    # Call the level function with the new player location
                    start_level_1(running, walls, player, barriers)

        pygame.draw.rect(screen, (66, 135, 245), (10, 10, player.stamina, 20))
        pygame.draw.rect(screen, (0, 36, 94), (10 + player.stamina, 10, player.max_stamina - player.stamina, 20))

        pygame.display.flip()
        clock.tick(10)

        screen.fill((0, 0, 0))

        create_wall(692, 300, 400, 50)
        create_wall(1083, 300, 200, 200)
        create_wall(640, 787, 610, 50)
        create_wall(1253, 300, 40, 500)
        create_wall(640, 300, 56, 300)
        create_wall(640, 590, 110, 113)
        create_wall(863, 590, 110, 113)
        create_wall(1083, 590, 200, 113)

        # Create a barrier with a message
        barrier = Barrier(692, 300, 100, 50, "Press 'E' to teleport")
        barriers.append(barrier)

    pygame.quit()
    sys.exit()



def start_level_1(running, walls, player, barriers):
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

        player.update(keys, walls)

        screen.blit(background_game_image, (0, 0))
        screen.blit(level_image, level_rect)
        # create_help_msg("Use WASD keys to move")

        draw_walls(walls)
        player.draw(screen)

        # Check if the player touches any barriers
        for barrier in barriers:
            if player.rect.colliderect(barrier.rect):
                barrier.display_message(screen)
                if keys[pygame.K_e]:  # Check if the player presses 'E'
                    # Move the player to a new location (change these coordinates accordingly)
                    player.rect.topleft = (100, 100)

        pygame.draw.rect(screen, (66, 135, 245), (10, 10, player.stamina, 20))
        pygame.draw.rect(screen, (0, 36, 94), (10 + player.stamina, 10, player.max_stamina - player.stamina, 20))

        pygame.display.flip()
        clock.tick(10)

        screen.fill((0, 0, 0))

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






def draw_interface():
    screen.blit(background_image, (0, 0))

    font_title = pygame.font.Font(None, 72)
    title_text = font_title.render("ВАШЕ НАЗВАНИЕ ИГРЫ", True, PINK)
    screen.blit(title_text, ((SCREEN_WIDTH - title_text.get_width()) // 2, 50))

    start_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 - 50, button_width, button_height)
    exit_button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT // 2 + 150, button_width, button_height)
    sound_button_rect = pygame.Rect(10, 10, sound_icon_size, sound_icon_size)

    start_button_image = button_pressed if start_button_rect.collidepoint(pygame.mouse.get_pos()) else button_normal
    exit_button_image = button_pressed if exit_button_rect.collidepoint(pygame.mouse.get_pos()) else button_normal

    screen.blit(start_button_image, (start_button_rect.x, start_button_rect.y))
    screen.blit(exit_button_image, (exit_button_rect.x, exit_button_rect.y))

    font_button = pygame.font.Font(None, 36)
    start_text = font_button.render("Играть", True, GRAY)
    exit_text = font_button.render("Выйти", True, GRAY)

    screen.blit(start_text, (start_button_rect.centerx - start_text.get_width() // 2, start_button_rect.centery - start_text.get_height() // 2))
    screen.blit(exit_text, (exit_button_rect.centerx - exit_text.get_width() // 2, exit_button_rect.centery - exit_text.get_height() // 2))

    sound_button_image = sound_off_icon if not sound_enabled else sound_on_icon
    screen.blit(sound_button_image, (sound_button_rect.x, sound_button_rect.y))


# Initialize Pygame
pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

WHITE = (255, 255, 255)
PINK = (255, 89, 118)
GRAY = (22, 67, 128)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Игра на Pygame")
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

background_image = pygame.image.load("fon.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

button_normal = pygame.image.load("assets/ui (new)/menu_button.png")
button_pressed = pygame.image.load("assets/ui (new)/menu_button_press.png")
sound_on_icon = pygame.image.load(r"assets\ui (new)\pause_button.png")
sound_off_icon = pygame.image.load(r"assets\ui (new)\pause_button_press.png")

button_width = 200
button_height = 50
sound_icon_size = 30

button_normal = pygame.transform.scale(button_normal, (button_width, button_height))
button_pressed = pygame.transform.scale(button_pressed, (button_width, button_height))
sound_on_icon = pygame.transform.scale(sound_on_icon, (sound_icon_size, sound_icon_size))
sound_off_icon = pygame.transform.scale(sound_off_icon, (sound_icon_size, sound_icon_size))

settings_file_path = os.path.join(os.path.expanduser("~"), "Documents", "My Games", "test_game", "settings.json")


def load_settings():
    if os.path.exists(settings_file_path):
        with open(settings_file_path, "r") as file:
            settings = json.load(file)
            return settings
    return {"music_volume": 0.5, "effect_volume": 0.5, "button_state": True, "sound_enabled": True}


def save_settings(settings):
    os.makedirs(os.path.dirname(settings_file_path), exist_ok=True)
    with open(settings_file_path, "w") as file:
        json.dump(settings, file)


pygame.mixer.music.load("your_background_music.mp3")
pygame.mixer.music.set_volume(0)
sound_effect = pygame.mixer.Sound("your_sound_effect.mp3")
sound_effect.set_volume(0.5)

sound_cursor_rect = pygame.Rect(0, 0, 30, 60)
sound_control_rect = pygame.Rect(0, 0, 400, 85)

increase_button_pressed = False
decrease_button_pressed = False

background_game_image = pygame.image.load("assets/levels/fon_DEFULT.png")
background_game_image = pygame.transform.scale(background_game_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

knight_idle_frames = [pygame.transform.scale(pygame.image.load(f"assets\heroes\knight/knight_idle_anim_f{i}.png"), (50, 50)) for i in range(6)]
knight_walk_frames = [pygame.transform.scale(pygame.image.load(f"assets\heroes\knight/knight_run_anim_f{i}.png"), (50, 50)) for i in range(6)]
walk_animation_speed = 100
current_frame = 1

player = Player(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, 40, 20, knight_walk_frames, knight_idle_frames)

running = True
clock = pygame.time.Clock()
pygame.mixer.music.play()

settings = load_settings()
print("Loaded settings:", settings)
music_volume = settings.get("music_volume", 0.5)
effect_volume = settings.get("effect_volume", 0.5)
button_state = settings.get("button_state", False)
sound_enabled = settings.get("sound_enabled", True)

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
                Home(running, walls, player, barriers)
            elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                running = False
            elif sound_button_rect.collidepoint(mouse_x, mouse_y):
                button_state = not button_state
                settings["button_state"] = button_state
                settings["sound_enabled"] = button_state
                save_settings(settings)
                print("Saved settings:", settings)
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
                print("Saved settings:", settings)
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
# ... (previous code)

            elif event.key == pygame.K_DOWN:
                decrease_button_pressed = False

    sound_button_rect = pygame.Rect(10, 10, sound_icon_size, sound_icon_size)
    sound_button_image = sound_off_icon if not sound_enabled else sound_on_icon
    screen.blit(sound_button_image, (sound_button_rect.x, sound_button_rect.y))

    draw_interface()

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()
