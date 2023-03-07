import pygame
import math

# initialize pygame
pygame.init()

# set the size of the window
size = width, height = 640, 480

# set the center of the complex plane
center = width // 2, height // 2

# create the window
screen = pygame.display.set_mode(size)

# define the translation factors
tx = 4.5
ty = 2.5

# define the scale factor
scale = 100

def zetaa(s, n=100):
    """
    Computes the Riemann zeta function for complex s and positive integer n.
    """
    sum = 0
    for k in range(1, n+1):
        sum += 1/(k**s)
    return sum


def zeta(x, y):
    """
    Computes the Riemann zeta function for a point on the complex plane
    defined by x and y.
    """
    s = complex((x - center[0])/scale - tx, (y - center[1])/scale - ty)
    return zetaa(s)

# main game loop
while True:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get the mouse position
            pos = pygame.mouse.get_pos()
            # compute the zeta function
            result = zeta(*pos)
            # display the result
            print(f"zeta({pos}) = {result}")
            # display the translations
            print(f"Translations: tx = {tx}, ty = {ty}")
    # clear the screen
    screen.fill((255, 255, 255))
    # draw the axes
    pygame.draw.line(screen, (0, 0, 0), (0, center[1]), (width, center[1]))
    pygame.draw.line(screen, (0, 0, 0), (center[0], 0), (center[0], height))
    # draw the point
    pos = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (255, 0, 0), pos, 5)
    # update the display
    pygame.display.flip()
