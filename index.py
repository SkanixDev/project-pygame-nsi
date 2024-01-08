import pygame

# Initalition de pygame
pygame.init()

# Création de la fenêtre
window_width = 644
window_height = 644
window = pygame.display.set_mode((window_width, window_height))

# Titre de la fenêtre
pygame.display.set_caption("My Game")

## Test Variables 
background_test = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,0,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,0],
]
object_test = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]


# Chargements des assets
# - Backgrounds (list of all background with name 'fond1','fond2',...)
bgs = [pygame.image.load('assets/backgrounds/fond_lune_1.png'),pygame.image.load('assets/backgrounds/fond_lune_2.png')]
objects = [pygame.image.load('assets/objects/vide.png'),pygame.image.load('assets/objects/rocher.png')]

# Dessin du fond
def draw_background():
    for row in range(14):
        for column in range(14):
            window.blit(bgs[background_test[row][column]],(column*46,row*46))

# Dessin des objets
def draw_objects():
    for row in range(14):
        for column in range(14):
            window.blit(objects[object_test[row][column]],(column*46,row*46))

# Classe personnage
class Player:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.image = pygame.image.load("assets/player/personnage.png")
        
    def deplacer(self, dx, dy):
        self.x += dx*46
        self.y += dy*46

    def dessiner(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_position(self):
        return (int(self.x/46),int(self.y/46))


# Définition des instances
player = Player(0,0)
clock = pygame.time.Clock()
draw_background()
draw_objects()

# Game loop
running = True
while running:
    clock.tick(4)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # déplacement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.deplacer(0,-1)
    if keys[pygame.K_DOWN]:
        player.deplacer(0,1)
    if keys[pygame.K_LEFT]:
        player.deplacer(-1,0)
    if keys[pygame.K_RIGHT]:
        player.deplacer(1,0)

    print(player.get_position())
    # Draw
    draw_background()
    draw_objects()
    player.dessiner(window)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
