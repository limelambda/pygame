#importing modules
import pygame
import time

def main():
    class Entity:
        def __init__(self, x, y, sprite):
            self.x = x
            self.y = y
            self.sprite = sprite
    # initializing the pygame module
    pygame.init()
    #load icon
    pygame.display.set_caption("Gam")
    # creating 240 x 180 screen surface
    screen = pygame.display.set_mode((540, 265), pygame.RESIZABLE)
    # define a variable to control the main loop
    running = True
     
    #make player
    player = Entity(128, 128, pygame.transform.scale(pygame.image.load("player.png"), (64, 64)))
    while running:
        screen_width, screen_height = pygame.display.get_surface().get_size()
        screen.blit(player.sprite, (player.x,player.y))
        print(screen_width, screen_height)
        #handle events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    player.y -= 10
                elif event.key == pygame.K_DOWN:
                    player.y += 10
                elif event.key == pygame.K_RIGHT:
                    player.x += 10
                elif event.key == pygame.K_LEFT:
                    player.x -= 10
        #render
        pygame.display.flip()
        screen.fill((200,200,0))

        #fps limiter
        time.sleep(0.01)

if __name__=="__main__":
    #call the main function
    main()