import pygame
import sys
from pygame.locals import *
import pygame_gui
from pygame_gui import UIManager
from game.game import MainGameScene

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Game Start Page")
clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("res/graphics/imgTransparencyPlace/bg.png").convert()
background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
background_rect = background_image.get_rect()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 50)
game = MainGameScene(screen, clock)

# UIManager for pygame_gui
ui_manager = UIManager((screen.get_width(), screen.get_height()))

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            pygame.draw.rect(surface, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
        draw_text(self.text, font, BLACK, surface, self.x + self.width // 2, self.y + self.height // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
                self.action()

# Function to draw text on screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Function to start the game
def start_game():
    print("Starting the game...")
    game.run()

# Function to quit the game
def quit_game():
    print("Quitting the game...")
    pygame.quit()
    sys.exit()

# Function to show high scores using pygame_gui elements
def show_high_scores():
    high_scores_window = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(
        rect=pygame.Rect((100, 100), (600, 400)),
        manager=ui_manager,
        window_title="High Scores",
        action_long_desc="Close"
    )
    

# Buttons
start_button = Button("Start", screen.get_width() // 2 - 100, screen.get_height() // 2, 200, 50, WHITE, (200, 200, 200), start_game)
quit_button = Button("Quit", screen.get_width() // 2 - 100, screen.get_height() * 3 // 4, 200, 50, WHITE, (200, 200, 200), quit_game)
high_scores_button = Button("High Scores", screen.get_width() // 2 - 100, screen.get_height() // 2 + 100, 200, 50, WHITE, (200, 200, 200), show_high_scores)

# Main loop
running = True
while running:
    screen.blit(background_image, background_rect)
    start_button.draw(screen)
    quit_button.draw(screen)
    high_scores_button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        start_button.handle_event(event)
        quit_button.handle_event(event)
        high_scores_button.handle_event(event)
        ui_manager.process_events(event)

    ui_manager.draw_ui(screen)
    pygame.display.update()

# Clean up
pygame.quit()
sys.exit()
