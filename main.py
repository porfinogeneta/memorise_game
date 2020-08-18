import sys
import pygame as pg
from settings import *
from os import path
from sprites import *
from random import randint
from os import path

vec_mouse = pg.math.Vector2

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        # initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.game_font = "Arial"
        self.clock = pg.time.Clock()
        self.load_data()
        self.vec_mouse = vec_mouse(0, 0)
        self.start_index = 1
        self.current_level = 1
        self.start_timer = START_TIMER
        self.isClicked = False
        self.set_new_timer = False

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)


    def load_data(self):
        game_folder = path.dirname(__file__)
        # img_folder = path.join(game_folder, 'img')
        with open(path.join(game_folder, HIGHSCORE_FILE), 'w') as f: #creates the file
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0



    def new(self):
        # initialize all variables and do all the setup for a new game
        self.start_timer = START_TIMER
        self.start_index = 1
        # self.current_level = self.current_level
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.memo_objects = pg.sprite.Group()
        self.obj_list = []
        for i in range(1, 7):
            self.memo_object = Memorable(self, randint(0, WIDTH), randint(0, HEIGHT), str(i), i)



    def run(self):
        # Game Loop
        self.playing = True
        # pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        self.Clicked()
        self.TimeCounter()
        self.LevelFinished()

    def TimeCounter(self):
        self.time_counter = 60
        self.start_timer -= self.time_counter
        self.seconds = self.start_timer // 1000
        if self.seconds <= 0:
            self.timeFinished()

    def Clicked(self):
        if self.isClicked == True:
            self.timeFinished()
            for object in self.memo_objects:
                if object.rect.collidepoint(self.vec_mouse):
                    print(f"clicked: {object.index}")

                    if object.index == self.start_index:
                        print("correct")
                        self.start_index += 1
                        object.kill()
                        if self.highscore < self.current_level:
                            self.highscore = self.current_level

                    else:
                        print("wrong")
                        self.current_level = 1
                        self.playing = False

            self.isClicked = False



    def timeFinished(self):
        self.seconds = 0
        for object in self.memo_objects:
            object.image.fill(RED)
            


    def LevelFinished(self):
        if len(self.memo_objects) == 0:
            self.new()
            self.current_level += 1


    def draw(self):
        # Game Loop - draw
        pg.display.set_caption('{:2f}'.format(self.clock.get_fps()))
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.seconds), self.game_font, 40, BLACK, WIDTH/2, 20, "center")
        self.draw_text(f"Level: {self.current_level}", self.game_font, 30, BLACK, 20, 0, "nw")
        self.draw_text(f"High score: {self.highscore}", self.game_font, 30, BLACK, WIDTH, 20, "e")
        pg.display.flip()


    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                self.vec_mouse = pg.mouse.get_pos()
                self.isClicked = True
            else:
                self.vec_mouse = (0, 0)
                self.isClicked = False




    def show_start_screen(self):
        # game splash/start screen
        self.screen.fill(LIGHTBLUE)
        self.draw_text("START", self.game_font, 80, BLACK, WIDTH / 2, HEIGHT / 2, "center")
        self.draw_text("Press any key to begin", self.game_font, 30, BLACK, WIDTH/2, HEIGHT * 0.75, "center")
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        self.screen.fill(LIGHTBLUE)
        self.draw_text("YOU LOST!", self.game_font, 50, BLACK, WIDTH/2, HEIGHT/2, "center")
        self.draw_text(f"HIGH SCORE: {self.highscore}", self.game_font, 20, BLACK, WIDTH / 2, HEIGHT * 0.75, "center")
        self.draw_text("Press any key to begin", self.game_font, 30, BLACK, WIDTH / 2, HEIGHT * 0.25, "center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()