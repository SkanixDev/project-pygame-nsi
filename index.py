import pygame as pg
from pygame import mixer
import json
import os
import math

tile = 46
size_screen = 16
screen_width = tile*size_screen
screen_height = tile*size_screen
screen = pg.display.set_mode((screen_width, screen_height))

design_lvl = 1 # 0: low, 1: high

pg.init()
mixer.init()
pg.display.set_caption('Jeu')
timer = pg.time.Clock()
selected_level = 0
walk_cooldown = 0
game_status = "menu"
running = True
sound_on = True
sound_init = False

menu_music = mixer.Sound('assets/sons/bgmusic.wav')
death_sound = mixer.Sound('assets/sons/mort.wav')
mixer.music.set_volume(0.2)


#  gameover state
gameover_status = False
pause_status = False
shop_status = False
level_screen_status = False

## Nicholas
        

def startScreen():
        global pause_status
        global game_status

        button_lvl_startScreen = ButtonImage("assets/images/niveaux.png", (290,320), (180,60))
        button_regles_startScreen = ButtonImage("assets/images/regles.png", (90,330), (180,60))
        button_quit_startScreen = ButtonImage("assets/images/quitter.png", (490,410), (180,70))
        button_sett_startScreen = ButtonImage("assets/images/parametres.png", (290,410), (180,70))
        button_shop_startScreen = ButtonImage("assets/images/shop_menu.png", (490,330), (180,60))
        button_mod_startScreen = ButtonImage("assets/images/mod.png", (90,400), (180,70))
        
        gameDisplay.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))
        titre = pg.image.load("assets/images/titre.png")
        screen.blit(titre, (170, 200))
       
        # Draw buttons
        button_regles_startScreen.draw()
        button_quit_startScreen.draw()
        button_sett_startScreen.draw()
        button_shop_startScreen.draw()
        button_mod_startScreen.draw()
        button_lvl_startScreen.draw()


        if button_lvl_startScreen.is_clicked():
            game_status = "lvl"

        if button_regles_startScreen.is_clicked():
            game_status = "regles"

        if button_quit_startScreen.is_clicked():
            game_status = "quit"

        if button_shop_startScreen.is_clicked():
            game_status = "shop"

        if button_sett_startScreen.is_clicked():
            game_status = "sett"

        if button_mod_startScreen.is_clicked():
            game_status = "mod"

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

smallFont = pg.font.Font("assets/fonts/zephyrea.ttf", 30)
medFont = pg.font.Font("assets/fonts/zephyrea.ttf", 40)
largeFont = pg.font.Font("assets/fonts/zephyrea.ttf", 55)



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


def messageToScreen(msg, color, y_displace = 0, size = "small",):
    textSurface, textRect = text_objects(msg, color, size,)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurface, textRect)

def text_to_button(msg, color, buttonX, buttonY, buttonWidth, buttonHeight, size = "small"):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonX + (buttonWidth/2), buttonY + (buttonHeight/2)))
    gameDisplay.blit(textSurface, textRect)


def button(text, x, y, width, height, inactiveColor , activeColor,textColor = black, action = None, lvl = None):
    global game_status
    global selected_level
    global sound_on
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
            if action == "son":
                sound_on = not sound_on

    else:
        pg.draw.rect(gameDisplay, inactiveColor, (x,y,width,height))

    text_to_button(text,textColor,x,y,width,height)

sound_settings_cooldown = 0
design_lvl_settings_cooldown = 0

def settings():
        global game_status
        global sound_on
        global design_lvl
        global sound_settings_cooldown
        global design_lvl_settings_cooldown
        global sound_init

        gameDisplay.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))
        titre = pg.image.load("assets/images/parametres_maj.png")
        screen.blit(titre, (190, 100))
        button_retour = ButtonImage("assets/images/retour.png", (70,500), (150,40))
        button_quit = ButtonImage("assets/images/quitter.png", (515,500), (150,50))

        button_quality = Button("Qualité", (290, 400), (150,50), gray)
        button_sound = Button("Son", (290, 300), (150,50), gray)

        text_indicator_quality = Button("Haute", (200, 400), (100,50), gray)

        if sound_on:
            button_sound.set_background_color(light_green)
        else:
            button_sound.set_background_color(light_red)
        
        if design_lvl == 0:
            text_indicator_quality.set_background_color(light_red)
            text_indicator_quality.set_text("Basse")
        else:
            text_indicator_quality.set_background_color(light_green)
            text_indicator_quality.set_text("Haute")
        
        text_indicator_quality.draw()


        button_retour.draw()
        if button_retour.is_clicked():
            game_status = "menu"
        
        button_quit.draw()
        if button_quit.is_clicked():
            game_status = "quit"
        
        button_quality.draw()
        if button_quality.is_clicked():
            if design_lvl_settings_cooldown == 0:
                print("Design level", design_lvl, design_lvl_settings_cooldown)
                if design_lvl == 0:
                    design_lvl = 1
                else:
                    design_lvl = 0
                design_lvl_settings_cooldown = 10
        
        button_sound.draw()
        if button_sound.is_clicked():
            if sound_settings_cooldown == 0:
                sound_on = not sound_on
                sound_init = False
                sound_settings_cooldown = 10
                print("Sound settings", sound_on, sound_settings_cooldown)
                manage_sound()

        if sound_settings_cooldown > 0:
            sound_settings_cooldown -= 1
        
        if design_lvl_settings_cooldown > 0:
            design_lvl_settings_cooldown -= 1



        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                settings = False
                pg.quit()
                quit()

current_page_levelScreen = 1

def levelScreen():
    global level_screen_status
    global selected_level
    global game_status
    global current_page_levelScreen

    if level_screen_status == False:
        data = json.load(open('data.json'))
        font = pg.font.Font("assets/fonts/zephyrea.ttf", 36)

        buttons = []

        gameDisplay.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))
        titre_lvl = pg.image.load("assets/images/niveaux_maj.png")
        screen.blit(titre_lvl, (260, 100))

        levels_per_page = 6
        total_levels = len(data['levels'])
        total_pages = math.ceil(total_levels / levels_per_page)

        start_index = (current_page_levelScreen - 1) * levels_per_page
        end_index = min(start_index + levels_per_page, total_levels)

        for i in range(start_index, end_index):
            level = data['levels'][i]
            start_x = 60  
            start_y = 250
            x = start_x + (250 * ((i - start_index) % 3))
            y = start_y + (130 * ((i - start_index) // 3))
            level_number = str(level['id'])
            button(level_number, x, y, 150, 50, light_yellow, yellow, action="lvlset", lvl=level_number)

        if current_page_levelScreen > 1:
            previous_page_button = Button("<", (tile*3, tile*3), (46,46), light_yellow)
            previous_page_button.draw()
            if previous_page_button.is_clicked():
                current_page_levelScreen -= 1
                level_screen_status = False
        if current_page_levelScreen < total_pages:
            next_page_button = Button(">", (tile*12, tile*3), (46,46), light_yellow)
            next_page_button.draw()
            if next_page_button.is_clicked():
                current_page_levelScreen += 1
                level_screen_status = False

        button_retour = ButtonImage("assets/images/retour.png", (70,500), (150,40))
        button_quit = ButtonImage("assets/images/quitter.png", (515,500), (150,50))

        button_retour.draw()
        if button_retour.is_clicked():
            game_status = "menu"

        button_quit.draw()
        if button_quit.is_clicked():
            game_status = "quit"


    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            level = False
            pg.quit()
            quit()

def directions():
        gameDisplay.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))
        titre = pg.image.load("assets/images/regles_maj.png")
        screen.blit(titre, (275, 100))
        messageToScreen("Utilisez les fleches pour vous deplacer",white,-100)
        messageToScreen("Recuperez toutes les gems",white,-60)
        messageToScreen("Evitez les enemies",white,-20)
        messageToScreen("Amusez-vous !",blue,80, size = "medium")
        button_retour = ButtonImage("assets/images/retour.png", (70,500), (150,40))
        button_quit = ButtonImage("assets/images/quitter.png", (500,500), (150,50))
        button_retour.draw()
        global game_status
        if button_retour.is_clicked():
            game_status = "menu"

        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False
                pg.quit()
                quit()
        
        button_quit.draw()
        if button_quit.is_clicked():
            game_status = "quit"

        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False
                pg.quit()
                quit()

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

        manage_sound()

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
            running = False
            pg.quit()
            os.system('python3 mod.py')
            print("Mod")
            
        elif game_status == "quit":
            running = False

    pg.quit()

def game(level, gui, player, enemies, items):
    global walk_cooldown
    global game_status
    global selected_level

    delta =  timer.tick(30) / 1000.0

    # Input
    walk_cooldown -= delta
    time_cooldown = 0.25

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
    mixer.Sound.play(death_sound)
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
        # if self.cooldown_skin <= 0:
        #     if self.frame_skin < len(self.skin)-1:
        #         self.frame_skin += 1
        #     else:
        #         self.frame_skin = 0
        #     self.cooldown_skin = 0.3
        # else:
        #     self.cooldown_skin -= 0.1
        # if self.state == "idle":
            # self.frame_skin = 0
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

    def set_background_color(self, color):
        self.color = color
        pass

    def set_text(self, text):
        self.text = self.font.render(text, 1, (255,255,255))
        pass

class ButtonImage():
    def __init__(self, image, position, size) -> None:
        self.image = pg.image.load(image)
        self.x = position[0]
        self.y = position[1]
        self.image = pg.transform.scale(self.image, size)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        pass

    def is_clicked(self):
        if pg.mouse.get_pressed()[0]:
            if self.x + self.image.get_width() > pg.mouse.get_pos()[0] > self.x and self.y + self.image.get_height() > pg.mouse.get_pos()[1] > self.y:
                return True
        return False


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
button_buy_shop_retour = None
button_buy_shop_quitter = None
def shop():
    global shop_status
    global buttons_buy_shop
    global button_buy_shop_quitter
    global button_buy_shop_retour
    global button
    global game_status

    player_inv = read_player()
    shop_items = read_shop()

    if shop_status == False:
        buttons_buy_shop = []
        screen.blit(pg.image.load('assets/backgrounds/fond_menu.png'),(0,0))

        titre = pg.image.load("assets/images/shop_maj.png")
        position_x = ((tile*size_screen)/2)-(titre.get_width()/2)
        position_y = (50)
        screen.blit(titre, (position_x, position_y))

        # Button back/quit 
        button_buy_shop_retour = ButtonImage('assets/images/retour.png', (70, 500), (150, 50))
        button_buy_shop_retour.draw()
        button_buy_shop_quitter = ButtonImage('assets/images/quitter.png', (500, 500), (150, 50))
        button_buy_shop_quitter.draw()

        #Text
        font_gem = pg.font.Font(None, 30)
        text_gem = font_gem.render(str(player_inv["pieces"]) + " Gems", 1, (10,10,10))
        screen.blit(text_gem,(screen_width - text_gem.get_width()-50, 50))

        space = 100
        line = 0
        start_x = 30
        start_y = 150
        for item in shop_items:
            print(item)
            image_skin = pg.image.load(item["image"])
            image_skin = pg.transform.scale(image_skin, (90, 90))
            pos_y = start_y + (line*170)
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
                color_text = (255,255,255)
                if item["price"] > player_inv["pieces"]:
                    color_text = (255,0,0)
                text_price = font_price.render("Prix: "+ str(item["price"]), 1, color_text)
                screen.blit(text_price,((space+15, pos_y + 150)))

            space += image_skin.get_width()+50
            if space > 600:
                space = 100
                line += 1

        shop_status = True

    else:
        global button
        for button_buy in buttons_buy_shop:
            if button_buy.is_clicked() and button_buy.get_text() == "Acheter":
                for item in shop_items:
                    if item["id"] == buttons_buy_shop.index(button_buy):
                        if player_inv["pieces"] >= item["price"] and item["id"] not in player_inv["inventory_skin"]:
                            add_skin_inventory(item["id"])
                            modify_gems(-item["price"])
                            shop_status = False
            elif button_buy.is_clicked() and button_buy.get_text() == "Equiper":
                change_skin_ative(buttons_buy_shop.index(button_buy))
        if button_buy_shop_retour.is_clicked():
            game_status = "menu"
            shop_status = False
        if button_buy_shop_quitter.is_clicked():
            pg.quit()
            
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

def manage_sound():
    global sound_init
    global sound_on

    if sound_init == False:
        if sound_on:
            pg.mixer.Sound.play(menu_music)
        else:
            pg.mixer.stop()
        sound_init = True

if __name__ == "__main__":
    main()