import pygame
import os

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flying MOOOOO')

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.75
GLIDE_GRAVITY = 0.2  # Reduced gravity for gliding
HIGH_JUMP_VELOCITY = -15  # Higher jump when pressing W
JUMP_VELOCITY = -11

# Define player action variables
moving_left = False
moving_right = False
paused = False  # Variable to track game pause state

# Define colors
BG = (144, 201, 120)
RED = (255, 0, 0)

# Function to load an image
def load_image(file_path):
    img = pygame.image.load(file_path)
    return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load background outside the main loop
background = load_image(r"\Flying Mooo\Background\Background.png")


class Cow(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Load all images for the player
        animation_types = ['Run']
        base_path = f'assets/{self.char_type}'  

        for animation in animation_types:
            temp_list = []
            animation_folder = os.path.join(base_path, animation)

            # Ensure directory exists
            if not os.path.exists(animation_folder):
                print(f"Error: Folder {animation_folder} does not exist!")
                continue

            num_of_frames = len(os.listdir(animation_folder))
            for i in range(num_of_frames):
                img_path = os.path.join(animation_folder, f'{i}.png')

                # Ensure image file exists
                if not os.path.isfile(img_path):
                    print(f"Error: Image {img_path} does not exist!")
                    continue

                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))  # Adjust scaling here
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def move(self):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed

        # High jump with 'W'
        if keys[pygame.K_w] and not self.jump and not self.in_air:
            self.vel_y = HIGH_JUMP_VELOCITY
            self.jump = True
            self.in_air = True

        # Regular jump with space bar
        if keys[pygame.K_SPACE] and not self.jump and not self.in_air:
            self.vel_y = JUMP_VELOCITY
            self.jump = True
            self.in_air = True

        # Glide when in air by holding 'W' (reducing gravity)
        if self.in_air and keys[pygame.K_w]:
            gravity_effect = GLIDE_GRAVITY
        else:
            gravity_effect = GRAVITY

        # Apply gravity
        self.vel_y += gravity_effect
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Limit cow's downward movement (ground level)
        if self.rect.bottom + dy > SCREEN_HEIGHT - 50:  # Adjust ground level
            dy = SCREEN_HEIGHT - 50 - self.rect.bottom
            self.in_air = False
            self.jump = False

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# Create the cow instance with a smaller scale
cow = Cow('cow', 200, 500, 1, 5)  

run = True
paused = False  # Game is initially not paused
while run:
    # Event handling (for pausing the game and quitting)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # Toggle pause when the Escape key is pressed
            if event.key == pygame.K_ESCAPE:
                paused = not paused  # Toggle the pause state

    if not paused:
        # Game logic only runs when not paused
        screen.blit(background, (0, 0))  # Draw the background

        # Update cow actions
        cow.move()
        cow.update_animation()
        cow.draw()

        pygame.display.update()

    # Slow down the game loop
    clock.tick(FPS)

pygame.quit()
