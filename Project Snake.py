
#referenced from https://pythonguides.com/snake-game-in-python/
import pygame
import pygame_menu
from pygame_menu import themes
from pygame import mixer
from pygame.locals import *
import random
import pickle  # Import pickle for saving high score

# Initialize Pygame
pygame.init()

# Set up the game window dimensions
dis_width = 600
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Define colors using RGB values
white = (255, 255, 255)
blue = (50, 153, 213)
red = (213, 50, 80)
green = (0, 255, 0)
black = (0, 0, 0)

# Size of each snake segment and movement speed
snake_block = 20
snake_speed = 10  # Decreased snake speed for slower movement

# Fonts for displaying text
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 30)  # Font for displaying scores

# Initialize Pygame clock
clock = pygame.time.Clock()

# Initialize score variables
score = 0
high_score = 0

# Load background music
pygame.mixer.music.load('bensound-summer_mp3_music.ogg')  # Replace with your music file
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely

# Function to display current score on screen
def display_score(score):
    score_text = score_font.render("Score: " + str(score), True, black)
    dis.blit(score_text, (10, 10))

# Function to display high score on screen
def display_high_score(high_score):
    high_score_text = score_font.render("High Score: " + str(high_score), True, black)
    dis.blit(high_score_text, (dis_width - 150, 10))

# Function to save high score to a file
def save_high_score(high_score):
    with open('highscore.dat', 'wb') as file:
        pickle.dump(high_score, file)

# Function to load high score from a file
def load_high_score():
    try:
        with open('highscore.dat', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return 0  # Return 0 if high score file does not exist

# Function to draw the snake on the screen
def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Function to display messages on the screen
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 12, dis_height / 3])

# Main game loop function
def gameLoop():
    global score, high_score

    game_over = False
    game_close = False

    # Initial position of the snake
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    # List to keep track of snake segments
    snake_List = []
    Length_of_snake = 1

    # Initial position of food
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            # Display game over message and options to quit or play again
            dis.fill(blue)
            message("You Lost! Q-Quit C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        score = 0  # Reset score when starting a new game
                        gameLoop()

        # Event handling loop for Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Change snake direction based on arrow keys
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Check if snake hits the boundaries of the game window
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Update snake position
        x1 += x1_change
        y1 += y1_change

        # Fill the display with background color
        dis.fill(blue)

        # Draw food on the screen
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])

        # Store snake head position in snake_List
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        # Remove last segment of the snake if its length exceeds Length_of_snake
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check for snake collision with itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Draw the snake on the screen
        snake(snake_block, snake_List)

        # Display current score and high score on the screen
        display_score(score)
        display_high_score(high_score)

        # Update the display
        pygame.display.update()

        # If snake eats the food
        if x1 == foodx and y1 == foody:
            score += 10  # Increase score when snake eats food

            # Update high score if current score is higher
            if score > high_score:
                high_score = score
                save_high_score(high_score)  # Save high score to file

            # Generate new position for food
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

            # Increase snake length
            Length_of_snake += 1

        # Adjust game speed
        clock.tick(snake_speed)

    # Quit Pygame and exit the program
    pygame.quit()
    quit()

# Initialize main menu with Pygame Menu
mainmenu = pygame_menu.Menu('WELCOME', 600, 600, theme=themes.THEME_SOLARIZED)

# Add buttons to the main menu
mainmenu.add.button('Play', gameLoop)  # Start the game loop when 'Play' is clicked
mainmenu.add.button('Quit', pygame_menu.events.EXIT)  # Exit the game when 'Quit' is clicked

# Game loop for the main menu
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Update and draw the main menu
    dis.fill(white)
    mainmenu.update(events)
    mainmenu.draw(dis)
    pygame.display.update()
