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
game_status = "menu"
running = True

#  gameover state
gameover_status = False
pause_status = False
shop_status = False
level_screen_status = False

## Nicholas
def startScreen():

        gameDisplay.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))

        messageToScreen("Gem Raider", black, -100, size = "large")
        button("Niveaux",100, 325,150,50, light_green, green, action = "lvl")
        button("Regles",300, 325,150,50, light_yellow, yellow, action = "directions")
        button("Quitter",500, 325,150,50, light_red, red, action = "quit")
        button("Parametres", 100, 400,150,50, gray, light_blue, action = "sett")
        button("Shop", 300, 400,150,50, gray, light_blue, action = "shop")
        button("Modificateur", 500, 400,150,50, gray, light_blue, action = "mod")
       


        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False
                pg.quit()
                quit()
display_width = 46*16
display_height = 46*16

white = (253,255,252)
brown = (248,126,98)
black = (9,8,9)
gray = (114,119,108)
red = (175,0,0)
green = (34,177,76)
yellow = (117,130,250)
blue = (30,144,255)
light_green = (34,230,76)
light_red = (230,0,0)
light_yellow = (117,184,200)
light_blue = (105,103,115)

smallFont = pg.font.SysFont("Fantacy", 30)
medFont = pg.font.SysFont("Fantacy", 40)
largeFont = pg.font.SysFont("Fantacy", 55)



gameDisplay = pg.display.set_mode((display_width, display_height))

pg.display.set_caption("Gem Raider")


def text_objects(text, color, size):
    if size == "small":
        textSurf = smallFont.render(text, True, color)
    elif size == "medium":
        textSurf = medFont.render(text, True, color)
    elif size == "large":
        textSurf = largeFont.render(text, True, color)

    return textSurf, textSurf.get_rect()


def messageToScreen(msg, color, y_displace = 0, size = "small"):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurface, textRect)

def text_to_button(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size = "small"):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonX + (buttonWidth/2), buttonY + (buttonHeight/2)))
    gameDisplay.blit(textSurface, textRect)


def button(text, x, y, width, height, inactiveColor , activeColor,textColor = black, action = None, lvl = None):
    global game_status
    global selected_level
    cur = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if x+ width > cur[0] > x and y + height > cur[1] > y:
        pg.draw.rect(gameDisplay, activeColor, (x,y,width,height))
        if click[0] == 1 and action !=  None:
            if action == "quit":
                pg.quit()
                quit()
            if action == "directions":
                game_status = "regles"
            if action == "lvl":
                game_status = "lvl"
            if action == "sett":
                game_status = "sett"
            if action == "shop":
                game_status = "shop"
            if action == "mod":
                game_status = "mod"
            if action == "main":
                game_status = "menu"
            if action == "lvlset" and lvl is not None:
                selected_level = lvl
                print("Selected level", selected_level)
                game_status = "loadlevel"    

    else:
        pg.draw.rect(gameDisplay, inactiveColor, (x,y,width,height))

    text_to_button(text,textColor,x,y,width,height)


def settings():
        gameDisplay.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))
        messageToScreen("Paramètres", black, -200, size = "large")
        button("Retour",70, 500,150,50, light_yellow, yellow, action = "main")
        button("Qualité",290, 500,150,50, gray, light_blue, action = "none")
        button("Quitter",500,500,150,50,light_red,red,action = "quit")
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings = False
                pg.quit()
                quit()

def levelScreen():
    global level_screen_status
    global selected_level

    if level_screen_status == False:
        data = json.load(open('data.json'))
        font = pg.font.Font(None, 36)
    

        buttons = []

        gameDisplay.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))

        for i, level in enumerate(data['levels']):
            x = 0
            if i // 3:
                x = 400
            elif i // 2:
                x = 450
            elif i //1:
                x = 500
            y = 250

            level_number = str(level['id'])
            button(level_number, x, y, 150,50, light_yellow, yellow, action="lvlset", lvl=level_number)
            
            messageToScreen("Niveaux", black, -200, size="large")
            button("Retour", 70, 500, 150, 50, light_yellow, yellow, action="main")
            button("Quitter", 500, 500, 150, 50, light_red, red, action="quit")

            pg.display.flip()
            level_screen_status = True
    else:
            button("Retour", 70, 500, 150, 50, light_yellow, yellow, action="main")
            button("Quitter", 500, 500, 150, 50, light_red, red, action="quit")



def directions():
        gameDisplay.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))
        messageToScreen("Regles", black, -200, size = "large")
        messageToScreen("Utilisez les fleches pour vous deplacer",black,-100)
        messageToScreen("Recuperez toutes les gems",black,-60)
        messageToScreen("Evitez les enemies",black,-20)
        messageToScreen("Amusez-vous !",blue,80, size = "medium")
        button("Retour",70, 500,150,50, light_yellow, yellow, action = "main")
        button("Quitter",500,500,150,50,light_red,red,action = "quit")
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                directions = False
                pg.quit()
                quit()

## Nicholas

def main():
    global running
    global game_status
    global game_status
    global level_screen_status

    level = None
    player = None
    gui = None
    enemies = []
    items = []

    while running: 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        if game_status == "loadlevel": # Chargement du niveau
            if level is not None: # Reset game
                del level
                del player
                del enemies
                level = None
                player = None
                enemies = []
                items = []
                gui = None
            level = Level(int(selected_level))
            level.load_level()
            player_init_position = level.get_player_init_position()
            print("Player", player_init_position)
            player = Player(player_init_position[0], player_init_position[1], [get_current_skin()])
            gui = GUI()
            for i in level.get_enemies():
                enemy = Enemy()
                enemy.load(i["type"], i["x"]*tile, i["y"]*tile, i["speed"], i["from_x"]*tile, i["from_y"]*tile, i["to_x"]*tile, i["to_y"]*tile)
                print(enemy.get_position())
                enemies.append(enemy)
            for i in level.get_items():
                item = Item()
                item.load(i["type"], i["x"]*tile, i["y"]*tile, i["image"])
                items.append(item)
            print("Ennemis", enemies)
            print("Items", items)
            game_status = "playing"
            
        elif game_status == "playing":
            game(level, gui, player, enemies, items)

        elif game_status == "gameover":
            gameover()
        
        elif game_status == "pause":
            pause()
        elif game_status == "menu":
            startScreen()
        elif game_status == "regles":
            directions()
        elif game_status == "lvl":
            level_screen_status = False
            levelScreen()
        elif game_status == "sett":
            settings()
        elif game_status == "shop":
            shop()
            pass
        elif game_status == "mod":
             pass

    pg.quit()

def game(level, gui, player, enemies, items):
    global walk_cooldown
    global game_status
    global selected_level

    delta =  timer.tick(30) / 1000.0

    # Input
    walk_cooldown -= delta
    time_cooldown = 0.35

    if walk_cooldown <= 0:
        if pg.key.get_pressed()[pg.K_UP]:
            player.move(level,enemies,items, 0, -1)
            walk_cooldown = time_cooldown
        if pg.key.get_pressed()[pg.K_DOWN]:
            player.move(level,enemies,items, 0, 1)
            walk_cooldown = time_cooldown
        if pg.key.get_pressed()[pg.K_LEFT]:
            player.move(level,enemies,items, -1, 0)
            walk_cooldown = time_cooldown
        if pg.key.get_pressed()[pg.K_RIGHT]:
            player.move(level,enemies,items, 1, 0)
            walk_cooldown = time_cooldown

        
     # Update
    level.render()
    for enemy in enemies:
        enemy.update(player.get_position())
    player.update()
    for item in items:
        if item.get_state():
            item.draw()
        if player.get_position() == item.get_position():
            item.set_state(False)
            items.remove(item)
            player.add_coin()
            modify_gems(1)
            gui.set_coins(player.get_coins())
            print("Coin", player.get_coins(), gui.get_coins())
            if len(items) == 0:
                game_status = "loadlevel"
                print("Level terminé")
                selected_level += 1
                print("Level", selected_level)
                if selected_level >= 2:
                    selected_level = 0
                print("Level", selected_level)
                break

    # GUI
    gui.draw()

    pg.display.flip()


button_rejouer = None
button_menu = None

def gameover():
    global running
    global gameover_status
    global game_status
    global button_rejouer
    global button_menu

    if not gameover_status:
        fond = pg.Surface((screen_width,screen_height))
        fond.fill((0,0,0))
        fond.set_alpha(128)

        image_mort = pg.image.load('assets/images/WASTED.png')
        position_x = ((tile*size_screen)/2)-(image_mort.get_width()/2)
        position_y = ((tile*size_screen)/2)-(image_mort.get_height()/2)
        screen.blit (fond,(0,0))    
        screen.blit(image_mort, (position_x, position_y))
        gameover_status = True

        button_rejouer = Button("Rejouer", (position_x-50, position_y+100),(120,70), (255,66,66))
        button_rejouer.draw()

        button_menu = Button("Menu", (50+position_x+image_mort.get_width()/2, position_y+100),(120,70), (64,213,66))
        button_menu.draw()

        pg.display.flip()
    else:
        if button_rejouer.is_clicked():
            gameover_status = False
            game_status = "loadlevel"
            print("Rejouer")
        if button_menu.is_clicked():
            gameover_status = False
            game_status = "menu"
            print("Menu")
    pass


def pause():
    global running
    global game_status
    global button_rejouer
    global button_menu
    global pause_status

    if not pause_status:
        fond = pg.Surface((screen_width,screen_height))
        fond.fill((0,0,0))
        fond.set_alpha(128)

        image_pause = pg.image.load('assets/images/PAUSE.png')
        position_x = ((tile*size_screen)/2)-(image_pause.get_width()/2)
        position_y = ((tile*size_screen)/2)-(image_pause.get_height()/2)
        screen.blit (fond,(0,0))    
        screen.blit(image_pause, (position_x, position_y))

        button_rejouer = Button("Reprendre", (position_x-50, position_y+100),(120,70), (255,66,66))
        button_rejouer.draw()

        button_menu = Button("Menu", (50+position_x+image_pause.get_width()/2, position_y+100),(120,70), (64,213,66))
        button_menu.draw()

        pg.display.flip()
        pause_status = True
    else:
        if button_rejouer.is_clicked():
            game_status = "playing"
            pause_status = False
            print("Rejouer")
        if button_menu.is_clicked():
            game_status = "menu"
            pause_status = False
            print("Menu")
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
        self.player_init_position = (0, 0)
        
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
                    self.player_init_position = (level["player_coordinates"][0]*tile, level["player_coordinates"][1]*tile)
            for textures in file["textures_map"]:
                if textures["id"] == self.textures_map:
                    for background in textures["backgrounds"]:
                        print("Loading textures", background)
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
        with open('data.json', 'r') as file_open:
            file = json.load(file_open)
            for level in file["levels"]:
                if level["id"] == self.id:
                    return level["enemy"]
    
    def get_items(self):
        with open('data.json', 'r') as file_open:
            file = json.load(file_open)
            for level in file["levels"]:
                if level["id"] == self.id:
                    return level["items"]
    
    def get_player_init_position(self):
        return self.player_init_position
    
class Entity(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y, skins):
        Entity.__init__(self)
        self.image = pg.Surface((tile, tile))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = "idle"
        self.direction = "south" # north, south, east, west
        self.frame_skin = 0
        self.skin = [skins[0]]
        self.cooldown_skin = 0
        self.coins = 0
    
    def update(self):
        self.draw()
        pass

    def draw(self):
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
    
    def move(self, level, enemies, items, x, y):
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
                    for item in items:
                        item.draw()
                    self.draw()
                    pg.display.flip()
            elif design_lvl == 1:
                for i in range(0, int(tile/2)):
                    self.state = "walk"
                    self.rect.x += x*2
                    self.rect.y += y*2
                    self.draw()
                    pg.time.delay(2)
                    pg.display.flip()
        self.state = "idle"
        pass

    def get_position(self):
        return (self.rect.x, self.rect.y)
    
    def add_coin(self):
        self.coins += 1
        pass
    
    def get_coins(self):
        return self.coins


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
        self.direction = "south" # north, south, east, west
    
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
                        self.direction = "east"
                    elif self.rect.x > self.to_x:
                        self.move(-1, 0)
                        self.direction = "west"
                    elif self.rect.y < self.to_y:
                        self.move(0, 1)
                        self.direction = "south"
                    elif self.rect.y > self.to_y:
                        self.move(0, -1)
                        self.direction = "north"
                    self.cool_down = self.cool_down_time
                else:
                    self.cool_down -= 0.15
            else:
                if self.rect.x == self.to_x and self.rect.y == self.to_y:
                    self.to_x = self.from_x
                    self.to_y = self.from_y
                    self.from_x = self.rect.x
                    self.from_y = self.rect.y
        pass

    def draw(self):
        img = pg.image.load("assets/enemies/black_fly.png")
        if self.direction == "south":
            img = pg.transform.rotate(img, 0)
        elif self.direction == "north":
            img = pg.transform.rotate(img, 180)
        elif self.direction == "east":
            img = pg.transform.rotate(img, 90)
        elif self.direction == "west":
            img = pg.transform.rotate(img, 270)
        screen.blit(img, (self.rect.x, self.rect.y))
        pass

    def move(self, x, y):
        self.rect.x += x*tile
        self.rect.y += y*tile
        pass

    def get_position(self):
        return (self.rect.x, self.rect.y)


class Button():
    def __init__(self, text, position, size, color = (120,120,120)) -> None:
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.font = pg.font.Font(None, 30)
        self.text = self.font.render(text, 1, (255,255,255))
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.color = color
        self.textStr = text

    def draw(self):
        self.image.fill(self.color)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        position_x = self.rect.x + (self.rect.width/2) - (self.text.get_width()/2)
        position_y = self.rect.y + (self.rect.height/2) - (self.text.get_height()/2)
        screen.blit(self.text, (position_x, position_y))
        pass

    def is_clicked(self):
        if pg.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                return True
        return False
    
    def get_text(self):
        return self.textStr


class Item():
    def __init__(self) -> None:
        self.init = False
        self.type = ""
        self.x = 0
        self.y = 0
        self.image = pg.Surface((tile, tile))
        self.state = True

    def load(self, type, x, y, image):
        self.type = type
        self.x = x
        self.y = y
        self.init = True
        self.image = pg.image.load(image)
        print("[INFO] - Item chargé")
        pass

    def draw(self):
        if self.init or self.state:
            screen.blit(self.image, (self.x, self.y))
        pass

    def get_position(self):
        return (self.x, self.y)
    
    def get_type(self):
        return self.type
    
    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        pass
    
class GUI():
    def __init__(self):
        self.coins = 0
        self.font = pg.font.Font("assets/fonts/pixel.TTF", 30)
        self.coinsText = self.font.render(str(self.coins), 1, (255,255,255))
        self.pauseButton = Button("Pause", (screen_width-100, 10), (90, 30), (232, 105, 32))
        pass

    def draw(self):
        self.coinsText = self.font.render(str(self.coins), 1, (255,255,255))
        # get size of text
        text_rect = self.coinsText.get_rect()
        # blit text in center of text
        self.pauseButton.draw()
        screen.blit(self.coinsText, ((screen_width/2)-(text_rect.width/2), 10))

        if self.pauseButton.is_clicked():
            global game_status
            game_status = "pause"
            print("Pause")
        pass
    
    def set_coins(self, coins):
        self.coins = coins
        pass
    
    def get_coins(self):
        return self.coins

buttons_buy_shop = []
def shop():
    global shop_status
    global buttons_buy_shop

    player_inv = read_player()
    shop_items = read_shop()

    if shop_status == False:
        buttons_buy_shop = []
        screen.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))

        image_shop = pg.image.load('assets/images/SHOP.png')
        position_x = ((tile*size_screen)/2)-(image_shop.get_width()/2)
        position_y = (50)
        screen.blit(image_shop, (position_x, position_y))

        #Text
        font_gem = pg.font.Font(None, 30)
        text_gem = font_gem.render(str(player_inv["pieces"]) + " Gems", 1, (10,10,10))
        screen.blit(text_gem,(screen_width - text_gem.get_width()-50, 50))

        space = 100
        for item in shop_items:
            print(item)
            image_skin = pg.image.load(item["image"])
            image_skin = pg.transform.scale(image_skin, (90, 90))
            pos_y = (tile*size_screen)/2-(image_shop.get_height()/2)
            screen.blit(image_skin, (space, pos_y))

            #button buy item
            if item["id"] in player_inv["inventory_skin"]:
                button_buy = Button("Equiper", (space, pos_y + 100), (92, 50), (50,255,50))
                button_buy.draw()
                buttons_buy_shop.append(button_buy)
            else:
                button_buy = Button("Acheter", (space, pos_y + 100), (92, 50), (50,50,50))
                button_buy.draw()
                buttons_buy_shop.append(button_buy)

            #text price
            font_price = pg.font.Font(None, 25)
            text_price = font_price.render("Prix: "+ str(item["price"]), 1, (10,10,10))
            screen.blit(text_price,((space+15, pos_y + 150)))

            space += image_skin.get_width()+50

        shop_status = True
    else:
        
        for button in buttons_buy_shop:
            if button.is_clicked() and button.get_text() == "Acheter":
                for item in shop_items:
                    if item["id"] == buttons_buy_shop.index(button):
                        if player_inv["pieces"] >= item["price"] and item["id"] not in player_inv["inventory_skin"]:
                            add_skin_inventory(item["id"])
                            modify_gems(-item["price"])
                            shop_status = False
            elif button.is_clicked() and button.get_text() == "Equiper":
                change_skin_ative(buttons_buy_shop.index(button))
    pg.display.flip()


def read_player():
    with open('player.json', 'r') as file_open:
        file = json.load(file_open)
        return file

def read_shop():
    with open('data.json', 'r') as file_open:
        file = json.load(file_open) 
        shop_file = file["shop"]
        return shop_file   


def modify_gems(value_modified):
    with open('player.json', 'r') as file_open:
        data = json.load(file_open)
        data["pieces"] = data["pieces"] + value_modified
        with open("player.json", "w") as json_file:
            json.dump(data, json_file, indent=4)

def add_skin_inventory(id):
    with open('player.json', 'r') as file_open:
        data = json.load(file_open)
        data["inventory_skin"].append(id)
        with open("player.json", "w") as json_file:
            json.dump(data, json_file, indent=4) 

def change_skin_ative(id):
    with open('player.json', 'r') as file_open:
        data = json.load(file_open)
        data["active_skin"] = id
        with open("player.json", "w") as json_file:
            json.dump(data, json_file, indent=4) 

def get_current_skin():
    with open('player.json', 'r') as file_open:
        data = json.load(file_open)
        with open('data.json', 'r') as file_open:
            file = json.load(file_open)
            return file["shop"][data["active_skin"]]["image"]

if __name__ == "__main__":
    main()




