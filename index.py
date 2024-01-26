import pygame as pg
import json

tile = 46
size_screen = 16
screen_width = tile*size_screen
screen_height = tile*size_screen
screen = pg.display.set_mode((screen_width, screen_height))

design_lvl = 1 # 0: low, 1: high

pg.init()
pg.display.set_caption('Jeu')
timer = pg.time.Clock()
selected_level = 0
walk_cooldown = 0
game_status = "loadlevel"
running = True

def main():
    global running
    global game_status

    level = None
    player = None
    enemies = []
    

    while running: 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if game_status == "loadlevel":
            level = Level(selected_level)
            player = Player(tile,tile*2)
            for i in level.get_enemies():
                enemy = Enemy()
                enemy.load(i["type"], i["x"]*tile, i["y"]*tile, i["speed"], i["from_x"]*tile, i["from_y"]*tile, i["to_x"]*tile, i["to_y"]*tile)
                print(enemy.get_position())
                enemies.append(enemy)
            level.load_level()
            game_status = "playing"
        elif game_status == "playing":
            game(level, player, enemies)
        elif game_status == "gameover":
            gameover()
            pass
    pg.quit()

def game(level, player, enemies):
    global walk_cooldown
    delta =  timer.tick(30) / 1000.0

    # Input
    walk_cooldown -= delta
    time_cooldown = 0.1

    if walk_cooldown <= 0:
        if pg.key.get_pressed()[pg.K_UP]:
            player.move(level,enemies, 0, -1)
            walk_cooldown = time_cooldown
        if pg.key.get_pressed()[pg.K_DOWN]:
            player.move(level,enemies, 0, 1)
            walk_cooldown = time_cooldown
        if pg.key.get_pressed()[pg.K_LEFT]:
            player.move(level,enemies, -1, 0)
            walk_cooldown = time_cooldown
        if pg.key.get_pressed()[pg.K_RIGHT]:
            player.move(level,enemies, 1, 0)
            walk_cooldown = time_cooldown

        
     # Update
    level.render()
    for enemy in enemies:
        enemy.update(player.get_position())
    player.update()
    pg.display.flip()

def gameover():
    global running
    # create text "Game over"
    # create button "Rejouer"
    print("T'es nul arrete de jouer")
    pass



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

    def get_level_id(self):
        return self.id

    def get_enemies(self):
        enemies = []
        with open('data.json', 'r') as file_open:
            file = json.load(file_open)
            for level in file["levels"]:
                if level["id"] == self.id:
                    return level["enemy"]

    
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
        self.state = "idle"
        self.direction = "south" # north, south, east, west
        self.frame_skin = 0
        self.skin = ["assets/player/personnage.png", "assets/player/perso_d1.png",
                        "assets/player/perso_d2.png", "assets/player/perso_d3.png",
                    ]
        self.cooldown_skin = 0
    
    def update(self):
        self.draw()
        pass

    def draw(self):
        img = ""
        if self.cooldown_skin <= 0:
            if self.frame_skin < len(self.skin)-1:
                self.frame_skin += 1
            else:
                self.frame_skin = 0
            self.cooldown_skin = 0.3
        else:
            self.cooldown_skin -= 0.1
        if self.state == "idle":
            self.frame_skin = 0
        rotated_img = ""
        if self.direction == "south":
            rotated_img = pg.transform.rotate(pg.image.load(self.skin[self.frame_skin]), 0)
        elif self.direction == "north":
            rotated_img = pg.transform.rotate(pg.image.load(self.skin[self.frame_skin]), 180)
        elif self.direction == "east":
            rotated_img = pg.transform.rotate(pg.image.load(self.skin[self.frame_skin]), 90)
        elif self.direction == "west":
            rotated_img = pg.transform.rotate(pg.image.load(self.skin[self.frame_skin]), 270)
        
        screen.blit(rotated_img, (self.rect.x, self.rect.y))
        pass
    
    def move(self, level, enemies, x, y):
        # if player out screen return 
        if self.rect.x//tile+x < 0 or self.rect.x//tile+x > size_screen or self.rect.y//tile+y < 0 or self.rect.y//tile+y > size_screen:
            return
        if level.get_objects_position((self.rect.x//tile)+x, (self.rect.y//tile)+y) == 0:
            if x == 1:
                self.direction = "east"
            elif x == -1:
                self.direction = "west"
            elif y == 1:
                self.direction = "south"
            elif y == -1:
                self.direction = "north"
            if design_lvl == 0:
                for i in range(0, 1):
                    self.state = "walk"
                    self.rect.x += x*tile
                    self.rect.y += y*tile
                    level.render()
                    for enemie in enemies:
                        enemie.update(self.get_position())
                    self.draw()
                    pg.display.flip()
            elif design_lvl == 1:
                for i in range(0, int(tile/2)):
                    self.state = "walk"
                    self.rect.x += x*2
                    self.rect.y += y*2
                    level.render()
                    for enemie in enemies:
                        enemie.update(self.get_position())
                    self.draw()
                    pg.display.flip()
        self.state = "idle"
        pass

    def get_position(self):
        return (self.rect.x, self.rect.y)


class Enemy(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.init = False
        self.image = pg.Surface((tile, tile))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.speed = 0
        self.from_x = 0
        self.from_y = 0
        self.to_x = 0
        self.to_y = 0
        self.type = ""
        self.cool_down = 0
        self.cool_down_time = 0.8
    
    def load(self, type: str, x: int, y: int, speed: int,from_x: int, from_y: int,to_x: int, to_y: int):
        self.type = type
        self.rect.x =  x
        self.rect.y = y
        self.speed = speed
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.init = True
        print("[INFO] - Ennemi chargé")
        pass

    def update(self, player_position):
        if self.init:
            self.draw()
            # check if player is on enemy position
            if self.rect.x == player_position[0] and self.rect.y == player_position[1]:
                global game_status
                game_status= "gameover"
                print("Game Over")
            # Move to to_x and to_y but step by step
            if self.rect.x != self.to_x or self.rect.y != self.to_y:
                if self.cool_down <= 0:
                    if self.rect.x < self.to_x:
                        self.move(1, 0)
                    elif self.rect.x > self.to_x:
                        self.move(-1, 0)
                    elif self.rect.y < self.to_y:
                        self.move(0, 1)
                    elif self.rect.y > self.to_y:
                        self.move(0, -1)
                    self.cool_down = self.cool_down_time
                else:
                    self.cool_down -= 0.1
            else:
                if self.rect.x == self.to_x and self.rect.y == self.to_y:
                    self.to_x = self.from_x
                    self.to_y = self.from_y
                    self.from_x = self.rect.x
                    self.from_y = self.rect.y
        pass

    def draw(self):
        img = pg.image.load("assets/enemies/black_fly.png")
        screen.blit(img, (self.rect.x, self.rect.y))
        pass

    def move(self, x, y):
        self.rect.x += x*tile
        self.rect.y += y*tile
        pass

    def get_position(self):
        return (self.rect.x, self.rect.y)




if __name__ == "__main__":
    main()