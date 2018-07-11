import pygame

def load_image(screen, image, row, col, scale=True):
    if scale:
        screen.blit(image, (col * 32, row * 32))
    else:
        screen.blit(image, (col, row))
