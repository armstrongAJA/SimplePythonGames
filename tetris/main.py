import sys
import pygame
import random
import tetris
import piece
import globalVariables as mn

# Screen dimensions
WIDTH, HEIGHT = mn.WIDTH, mn.HEIGHT
GRID_SIZE = mn.GRID_SIZE

# Colors
WHITE = mn.WHITE
BLACK = mn.BLACK
RED = mn.RED
BLUE = mn.BLUE
GREEN = mn.GREEN
COLORS = mn.COLORS

#set the frame rate
FPS = mn.FPS

# define piece shapes as list
SHAPES = mn.SHAPES

def draw_score(screen, score, x, y):
    """Draw the score on the screen"""
    size = 20
    rect = pygame.Rect(x, y, size*5, size)
    pygame.draw.rect(screen, BLACK, rect)

    font = pygame.font.Font(None, size)
    text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(text, (x, y))
    
    
def draw_game_over(screen, x, y):
    """Draw the game over text on the screen"""
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (x, y))
    
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    game = tetris.Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
    
    fall_time = 0
    fall_speed = 200
    print('initialized game')
          
    while True:
        # Fill the screen with black
        screen.fill(BLACK) 
        for event in pygame.event.get():
            # Check for the QUIT event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Check for the KEYDOWN event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print('left pressed')
                    if game.validMove(game.currentPiece, -1, 0, 0):
                        print('moving piece left...')
                        game.currentPiece.x -= 1 # Move the piece to the left
                if event.key == pygame.K_RIGHT:
                    print('right pressed')
                    if game.validMove(game.currentPiece, 1, 0, 0):
                        print('moving piece right...')
                        game.currentPiece.x += 1 # Move the piece to the right
                if event.key == pygame.K_DOWN:
                    print('down pressed')
                    if game.validMove(game.currentPiece, 0, 1, 0):
                        game.currentPiece.y += 1 # Move the piece down
                if event.key == pygame.K_UP:
                    print('up pressed')
                    if game.validMove(game.currentPiece, 0, 0, 1):
                        game.currentPiece.rotation += 1 # Rotate the piece
                if event.key == pygame.K_SPACE:
                    print('space pressed')
                    while game.validMove(game.currentPiece, 0, 1, 0):
                        game.currentPiece.y += 1 # Move the piece down until it hits the bottom
                    game.lockPiece(game.currentPiece) # Lock the piece in place
        # Get the number of milliseconds since the last frame
        delta_time = clock.get_rawtime() 
        # Add the delta time to the fall time
        fall_time += delta_time 
        if fall_time >= fall_speed:
            # Move the piece down
            game.updatePiece()
            # Reset the fall time
            fall_time = 0
        # Draw the grid and the current piece

        game.draw(screen)
        draw_score(screen, game.score, 20, 20)
        # Draw the score on the screen
        if game.isGameOver:
            # Draw the "Game Over" message
            draw_game_over(screen, WIDTH // 2 - 100, HEIGHT // 2 - 30)  # Draw the "Game Over" message
            # You can add a "Press any key to restart" message here
            # Check for the KEYDOWN event
            if event.type == pygame.KEYDOWN:
                # Create a new Tetris object
                game = tetris.Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
        # Update the display
        pygame.display.flip()
        # Set the framerate
        clock.tick(FPS)

main()
