import pygame as pg
from settings import *
from random import randint

vec = pg.math.Vector2


class Memorable(pg.sprite.Sprite):
    def __init__(self, game, x, y, text, index):
        self._layer = MEMO_OBJ
        self.groups = game.all_sprites, game.memo_objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((WIDTH_OBJ, HEIGHT_OBJ))
        self.image.fill(GREEN)
        self.font = pg.font.SysFont("Arial", 20)
        self.textSurf = self.font.render(text, True, BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.index = index
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [WIDTH_OBJ / 2 - W / 2, HEIGHT_OBJ / 2 - H / 2])
        # self.game.draw_text(text, self.game.game_font, 15, BLACK, x, y, align="center ")

    def update(self):
        pass
        # if self.game.vec_mouse == self.rect.center:
        #     print("click")


