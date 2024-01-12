import pygame

# Initalition de pygame
pygame.init()

# Création de la fenêtre
tile = 46
window_width = 16*tile
window_height = 16*tile
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
enemy_test = [{ 
    'type_enemy': 0, # 0 = red block
    'start': [9,12],
    'end': [0,12],
    'x': 10,
    'y': 12,
}] 


# Chargements des assets
# - Backgrounds (list of all background with name 'fond1','fond2',...)
bgs = [pygame.image.load('assets/backgrounds/fond_lune_1.png'),pygame.image.load('assets/backgrounds/fond_lune_2.png')]
objects = [pygame.image.load('assets/objects/vide.png'),pygame.image.load('assets/objects/rocher.png')]
enemies = [pygame.image.load('assets/enemies/redblock.png')]

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

# Dessin des ennemis
def draw_enemies():
    for enemy in enemy_test:
        window.blit(enemies[enemy['type_enemy']],(enemy['x']*46,enemy['y']*46))

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


# Mise à jour des ennemis
def update_enemy(enemy):
    if enemy['x'] == enemy['end'][0] and enemy['y'] == enemy['end'][1]:
        enemy['end'],enemy['start'] = enemy['start'],enemy['end']
    else:
        if enemy['x'] > enemy['end'][0]:
            enemy['x'] -= 1
        if enemy['x'] < enemy['end'][0]:
            enemy['x'] += 1
        if enemy['y'] > enemy['end'][1]:
            enemy['y'] -= 1
        if enemy['y'] < enemy['end'][1]:
            enemy['y'] += 1
    

# Définition des instances
player = Player(0,0)
clock = pygame.time.Clock()
draw_background()
draw_objects()
draw_enemies()

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
        if object_test[player.get_position()[1]-1][player.get_position()[0]] == 0:
            player.deplacer(0,-1)
    if keys[pygame.K_DOWN]:
        if object_test[player.get_position()[1]+1][player.get_position()[0]] == 0:
            player.deplacer(0,1)
    if keys[pygame.K_LEFT]:
        if object_test[player.get_position()[1]][player.get_position()[0]-1] == 0:
            player.deplacer(-1,0)
    if keys[pygame.K_RIGHT]:
        if object_test[player.get_position()[1]][player.get_position()[0]+1] == 0:
            player.deplacer(1,0)

    # Update enemies
    update_enemy(enemy_test[0])

    # Draw
    draw_background()
    draw_objects()
    draw_enemies()
    player.dessiner(window)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
