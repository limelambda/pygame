#importing modules
import pygame
import time

def main():

    def load_sprite(img,size):
        return pygame.transform.scale(pygame.image.load(img), (size, size))

    class Entity:
        def __init__(self, x, y, sprite, x_speed = 0, y_speed = 0, direction = "down"):
            print(self.__class__.__name__, "created!")
            self.x_speed = x_speed
            self.y_speed = y_speed
            self.x = x
            self.y = y
            self.sprite = sprite
            self.direction = direction
        
        def do_move(self):
            self.x += self.x_speed / 2
            self.y += self.y_speed / 2
            self.x_speed = round(self.x_speed/1.1, 4)
            self.y_speed = round(self.y_speed/1.1, 4)

        def do_blit(self):
            print(self.x_speed, self.y_speed)
            if abs(self.x_speed) != abs(self.y_speed):
                if abs(self.x_speed) > abs(self.y_speed):
                    if self.x_speed < 0:
                        self.direction = "left"
                    else:
                        self.direction = "right"
                else:
                    if self.y_speed < 0:
                        self.direction = "up"
                    else:
                        self.direction = "down"
            screen.blit(player.sprite[self.direction], (player.x,player.y))

    # initializing the pygame module
    pygame.init()
    #load icon
    pygame.display.set_caption("Gam")
    # creating 240 x 180 screen surface
    screen = pygame.display.set_mode((540, 265), pygame.RESIZABLE)
    # define a variable to control the main loop
    running = True
     
    #make player
    player = Entity(128, 128, {
        "down":load_sprite("player/down.png",64), 
        "up":load_sprite("player/up.png",64), 
        "left":load_sprite("player/left.png",64), 
        "right":load_sprite("player/right.png",64)})
    while running:
        screen_width, screen_height = pygame.display.get_surface().get_size()
        #handle events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            player.y_speed -= 1
        if pressed[pygame.K_DOWN]:
            player.y_speed += 1
        if pressed[pygame.K_RIGHT]:
            player.x_speed += 1
        if pressed[pygame.K_LEFT]:
            player.x_speed -= 1
        player.do_move()
        player.do_blit()
        #render
        pygame.display.flip()
        screen.fill((200,200,0))

        #fps limiter
        time.sleep(0.01)

if __name__=="__main__":
    #call the main function
    main()