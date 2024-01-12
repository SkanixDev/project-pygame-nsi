import pygame as pg
import json

tile = 46
size_screen = 16
screen_width = tile*size_screen
screen_height = tile*size_screen
screen = pg.display.set_mode((screen_width, screen_height))

def main():
    pg.init()
    pg.display.set_caption('Jeu')
    timer = pg.time.Clock()

    selected_level = 0
    walk_cooldown = 0
    running = True

    level = Level(0)
    player = Player(tile,tile*2)
    level.load_level()


    while running:
        delta =  timer.tick(30) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Input
        walk_cooldown -= delta

        if walk_cooldown <= 0:
            if pg.key.get_pressed()[pg.K_UP]:
                player.move(level, 0, -1)
                walk_cooldown = 0.2
            elif pg.key.get_pressed()[pg.K_DOWN]:
                player.move(level, 0, 1)
                walk_cooldown = 0.2
            elif pg.key.get_pressed()[pg.K_LEFT]:
                player.move(level, -1, 0)
                walk_cooldown = 0.2
            elif pg.key.get_pressed()[pg.K_RIGHT]:
                player.move(level, 1, 0)
                walk_cooldown = 0.2

        # Update
        level.render()
        player.update()
        pg.display.flip()


class Level():
    def __init__(self, id: int) -> None:
        self.id = id
        self.init = False
        self.name = ""
        self.description = ""
        self.textures_map = 0
        self.background = []
        self.background_textures = []
        self.objects = []
        self.objects_textures = []
        
    def load_level(self):
        with open('data.json', 'r') as file_open:
            file = json.load(file_open)
            for level in file["levels"]:
                if level["id"] == self.id:
                    self.name = level["name"]
                    self.decription = level["description"]
                    self.background = level["background"]
                    self.objects = level["objects"]
                    self.textures_map = level["textures_map"]
            for textures in file["textures_map"]:
                if textures["id"] == self.textures_map:
                    for background in textures["backgrounds"]:
                        self.background_textures.append(pg.image.load(background))
                    for objecT in textures["objects"]:
                        self.objects_textures.append(pg.image.load(objecT))
            self.init = True
            print("[INFO] - Niveau chargé")    

    def __render_background(self):
        if self.init == False:
            raise Exception("[ERREUR] - Niveau pas chargé")
        for y in range(size_screen):
            for x in range(size_screen):
                bg = self.background
                textures = self.background_textures
                screen.blit(textures[bg[y][x]], (x*tile, y*tile))
    
    def __render_objects(self):
        if self.init == False:
            raise Exception("[ERREUR] - Niveau pas chargé")
        for y in range(size_screen):
            for x in range(size_screen):
                obj = self.objects
                textures = self.objects_textures
                screen.blit(textures[obj[y][x]], (x*tile, y*tile))   
                     
    def render(self):
        # Render du background
        self.__render_background()
        self.__render_objects()
    
    def get_objects_position(self, x, y):
        return self.objects[y][x]
    
class Entity(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pg.Surface((tile, tile))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.draw()
        pass

    def draw(self):
        img = pg.image.load("assets/player/personnage.png")
        screen.blit(img, (self.rect.x, self.rect.y))
        pass
    
    def move(self, level, x, y):
        # if player out screen return 
        if self.rect.x//tile+x < 0 or self.rect.x//tile+x > size_screen or self.rect.y//tile+y < 0 or self.rect.y//tile+y > size_screen:
            return print("Impossible1")
        if level.get_objects_position((self.rect.x//tile)+x, (self.rect.y//tile)+y) == 0:
            for i in range(0, int(tile/2)):
                self.rect.x += x*2
                self.rect.y += y*2
                level.render()
                self.draw()
                pg.display.flip()
        else:
            print("Impossible")
        print("x:",x," y:", y," object:", level.get_objects_position((self.rect.x//tile)+x, (self.rect.y//tile)+y), " pos:",(self.rect.x//tile), (self.rect.y//tile))
        pass

    def get_position(self):
        return (self.rect.x, self.rect.y)


if __name__ == "__main__":
    main()

