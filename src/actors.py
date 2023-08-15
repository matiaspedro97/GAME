import sys

sys.path.extend('../src')

import time
import threading
import pygame
import numpy as np
import os
from hashlib import new
import glob

from pygame.constants import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_UP,
    K_DOWN,
    QUIT,
    K_SPACE,
    KEYUP,
    KEYDOWN,
    K_DELETE,
    K_w,
    K_a,
    K_d,
    K_r
)


# FUNCTIONS
########################################################################################
def dist_players(p1, p2):
    p1_hor, p2_hor = list(range(p1.rect.left, p1.rect.right + 1)), \
                     list(range(p2.rect.left, p2.rect.right + 1))
    p1_ver, p2_ver = list(range(p1.rect.top, p1.rect.bottom)), \
                     list(range(p2.rect.top, p2.rect.bottom))

    d_hor = len(np.intersect1d(p1_hor, p2_hor))
    d_ver = len(np.intersect1d(p1_ver, p2_ver))
    print(d_hor)
    return d_hor, d_ver, p1_ver, p2_ver, p1_hor, p2_hor


def change_constraints(p1, p2):
    d_hor, d_ver, p1_ver, p2_ver, p1_hor, p2_hor = dist_players(p1, p2)

    if d_hor > 1:
        if p1_ver[-1] <= p2_ver[0]:
            p1.c_ymin, p2.c_ymax = p2_ver[0], p1_ver[-1]
            p1.c_ymax = p1.ymax
        elif p2_ver[-1] <= p1_ver[0]:
            p2.c_ymin, p1.c_ymax = p1_ver[0], p2_ver[-1]
            p2.c_ymax = p2.ymax
        else:
            p1.c_ymax, p2.c_ymax = p1.ymax, p1.ymax
            p1.c_ymin, p2.c_ymin = p1.ymin, p1.ymin
        if d_ver < 1:
            p1.c_xmin, p1.c_xmax, p2.c_xmin, p2.c_xmax = p1.xmin, p1.xmax, \
                                                         p1.xmin, p2.xmax

    else:
        p1.c_ymin, p2.c_ymin, p1.c_ymax, p2.c_ymax, = p1.ymin, p1.ymin, p1.ymax, p1.ymax
        if p1_hor[0] >= p2_hor[-1]:
            p1.c_xmin, p2.c_xmax = p2_hor[-1], p1_hor[0]
        else:
            p2.c_xmin, p1.c_xmax = p1_hor[-1], p2_hor[0]
        if d_ver < 1:
            p1.c_xmin, p1.c_xmax = p1.xmin, p1.xmax
            p2.c_xmin, p2.c_xmax = p2.xmin, p2.xmax


# Players class
class Fighter:
    def __init__(self, x, y, max_hp, strength, icon_path, player, screen, keys, mac):
        self.c = None
        self.mac = mac
        self.wait_time, self.curr_time = 0.5, 0

        self.hp, self.max_hp = max_hp, max_hp
        self.alive = True
        self.strength = strength
        self.side = 0
        self.anim = pygame.transform.scale(pygame.image.load(icon_path), (70, 100))
        self.anim_list = [self.anim, pygame.transform.flip(self.anim, True, False)]
        self.icon = self.anim_list[self.side]
        self.rect = self.icon.get_rect()
        self.rect.center = (x, y)
        self.player = player
        self.screen = screen
        self.avail_keys = keys
        self.flag_up, self.jump_flag = 1, 0
        self.ymax, self.ymin, self.xmin, self.xmax = self.screen.get_height() - 290, \
                                                     self.screen.get_height() - 50, 0, \
                                                     self.screen.get_width()
        self.c_ymax, self.c_ymin, self.c_xmin, self.c_xmax = self.ymax, self.ymin, \
                                                             self.xmin, self.xmax
        self.icon_h, self.icon_w = self.icon.get_height(), self.icon.get_width()

    def draw(self):
        self.icon = self.anim_list[self.side]
        self.screen.blit(self.icon, self.rect)
        # print(self.hp)
        life_perc = self.hp / self.max_hp
        c = (0, 255, 0) if self.hp > self.max_hp / 4 else (255, 0, 0)

        # Life bar
        self.screen.fill(color=c, rect=(self.rect.left, self.rect.top - 10,
                                        (self.rect.right - self.rect.left) * life_perc,
                                        10))

    def update_pos(self, key):
        if key == self.avail_keys[0]:
            self.rect.left -= 10 if self.rect.left > self.c_xmin else 0
            print('LEFT')
            self.side = 1
        elif key == self.avail_keys[1]:
            self.rect.right += 10 if self.rect.right < self.c_xmax else 0
            print('RIGHT')
            self.side = 0
        elif key == self.avail_keys[2]:
            self.jump_flag = 1
            print('JUMP')

        if self.jump_flag == 0 and self.rect.bottom < self.c_ymin:
            print('rrrrrrrrrrrrrrrrrrrr')
            self.jump_flag, self.flag_up = 1, 0
        if self.jump_flag:
            if self.flag_up:
                self.rect.centery -= 2
                self.flag_up = 0 if self.rect.top == self.c_ymax else 1
            else:
                self.rect.centery += 2
                self.jump_flag, self.flag_up = (0, 1) if self.rect.bottom == self.c_ymin else (1, 0)

            pygame.time.wait(1)
        # print(f'JUMP {self.jump_flag}')
        # print(f'UP {self.flag_up}')

    def smartphone_connect(self):
        self.c = Client(address=self.mac)
        self.c.connect()
        con_flag = bool(self.c.connected)
        data_flag = self.c.dataCurrent is not None
        while con_flag * data_flag != 1:
            pass
        print('Smartphone Connected')

    def smartphone_control(self):
        try:
            data_c = self.c.dataCurrent.Acceleration.Values.AsDouble
            magn = np.sqrt(np.sum(np.array(data_c) ** 2))
        except Exception:
            data_c, magn = 0, 0

        if time.time() - self.curr_time > self.wait_time:
            self.curr_time = 0
            if data_c[1] < -5:
                key = self.avail_keys[0]
                self.curr_time = time.time()
            elif data_c[1] > 5:
                key = self.avail_keys[1]
                self.curr_time = time.time()
            else:
                key = ""
        else:
            key = ""

        if magn > 2 * 10:
            key = self.avail_keys[2]
        return key

    def hp_update(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

    def hit(self, p_op):
        d_hor, d_ver, _, _, self_ver, p_op_ver = dist_players(p1=self, p2=p_op)
        op_side = 1 if self.rect.centerx > p_op.rect.centerx else 0
        if d_hor > 0 and d_ver > 0 and self.side == op_side:
            print(f"d_ver: {d_ver}")
            print(f"d_HOR: {d_hor}")
            punch_sound = pygame.mixer.Sound('soundtrack/punch.wav')
            punch_sound.play()
            p_op.hp_update(damage=5)

    def attack(self, key, p_op):
        if key == self.avail_keys[3]:
            self.hit(p_op=p_op)


def draw_bg(screen, winner, bg_img, ended=False, slid_inc=0):
    if not ended:
        screen.blit(bg_img, (0, 0)) 
    else:
        draw_game_over(screen, text=winner, slid_inc=slid_inc)


def draw_game_over(screen, text, slid_inc):
    pygame.display.set_caption(text)
    font = pygame.font.SysFont("calibri", 30)
    text_rend = font.render(text, False, (0, 255, 0), (255, 255, 255))
    screen.fill((255, 255, 255))
    screen.blit(text_rend, (0+slid_inc, 0+slid_inc))




