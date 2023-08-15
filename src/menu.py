import sys

sys.path.extend('../src')

import time
import threading
import pygame
import numpy as np
import os
from hashlib import new
import glob

from src.constants import *
from src.actors import *



class Manager:
    def __init__(self, menu):
        self.menu = menu
        self.font_name = 'arial'
        self.screen = menu.screen

    def create_screen(self):
        return 0

    def screen_change(self, screen):
        self.screen = screen

    @staticmethod
    def draw_text(screen, txt, size, x, y, c: tuple = (0, 0, 0)):
        font = pygame.font.SysFont(name='consolas', size=size)
        text_surface = font.render(txt, True, c)
        text_rect = text_surface.get_rect()
        text_rect.left = x
        text_rect.centery = y
        screen.blit(text_surface, text_rect)
        return y


class MainMenu:
    def __init__(self, s_width: int, s_height: int):
        pygame.init()
        self.w, self.h = s_width, s_height

        self.offset = +50
        self.cursor_y = None
        self.cursor_str = None

        self.opt = {'MAIN': ['PLAY', 'CHOOSE CHARACTER', 'CHOOSE SOUNDTRACK', 'QUIT'], 
                    'CHOOSE CHARACTER': ['> NEXT', '< PREVIOUS'],
                    'CHOOSE SOUNDTRACK': ['> NEXT', '< PREVIOUS', 'P < PLAY/PAUSE'],
                    'QUIT': ['YES', 'NO']}

        self.opt_map = {'PLAY': self.play_screen,
                        'CHOOSE CHARACTER': self.choose_char_screen, 
                        'CHOOSE SOUNDTRACK': self.soundtrack_screen, 
                        'QUIT': pygame.quit
                        }

        self.char_path = glob.glob(os.path.join(CHAR_PATH, '*.*'))
        self.track_path = [None] + glob.glob(os.path.join(SOUNDTRACK_PATH, '*.*'))
        self.menu_path = glob.glob(os.path.join(MENU_PATH, '*.*'))

        self.chosen_char = self.char_path[:2]
        self.chosen_track = self.track_path[0]
        self.chosen_menu = self.menu_path[0]
        print(self.chosen_menu)

        self.start_screen()
    
    def reset_screen(self):
        self.menu_img = pygame.transform.scale(pygame.image.load(self.chosen_menu), (self.w, self.h))
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.blit(self.menu_img, (0,0))
        self.cursor_rect = pygame.Rect([20, self.w-self.w//2, 30, 30])

    def start_screen(self):
        self.reset_screen()

        RUN = True
        self.cursor_y = Manager.draw_text(screen=self.screen, txt='>', size=40, 
                                          x=self.cursor_rect.right - 30, y=self.cursor_rect.y)
        self.cursor_str = self.opt['MAIN'][0]
        
        while RUN:
            opt_y = [Manager.draw_text(screen=self.screen, txt=opt, size=40, x=self.cursor_rect.right + 50, 
                                       y=self.cursor_rect.y + self.offset * idx) 
                     for idx, opt in enumerate(self.opt['MAIN'])]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUN = False
                if event.type == pygame.KEYDOWN:
                    # change cursor
                    self.change_cursor(key=event.key, opt_y=opt_y, 
                                       opt_str=self.opt['MAIN'])
                    print(self.chosen_char)

                    if event.key==pygame.K_RETURN:
                        print('sgdfgkhjgh')
                        # choose screen according to the cursor position
                        self.opt_map[self.cursor_str]()

            pygame.display.update()
        pygame.quit()
    
    def change_cursor(self, key, opt_y, opt_str):
        d = {pygame.K_UP: -1, pygame.K_DOWN: 1}
        move = d.get(key)

        if move is not None:
            self.screen.blit(self.menu_img, (0,0))
            #self.screen = pygame.display.set_mode((self.w, self.h))
            try:
                cursor_idx = np.where(self.cursor_y == np.array(opt_y))[0][0]
                new_idx = cursor_idx + move
                new_idx = new_idx + (0 if (new_idx >= 0 and new_idx <= len(opt_y)-1) else -move)
                new_cursor_y = opt_y[new_idx]
                new_cursor_str = opt_str[new_idx]
            except Exception as e:
                print(e)
                new_cursor_y = self.cursor_y
                new_cursor_str = self.cursor_str
        else:
            new_cursor_y = self.cursor_y
            new_cursor_str = self.cursor_str

        self.cursor_y = Manager.draw_text(screen=self.screen, txt='>', size=40, 
                                          x=self.cursor_rect.right-30,
                                          y=new_cursor_y)
        self.cursor_str = new_cursor_str
    
    def change_char(self, key, curr_idx: int, characters: list, rect: pygame.Rect):
        d = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1}
        move = d.get(key)
        print(f"MOVE: {move}")

        if move is not None:
            self.screen.blit(self.menu_img, (0,0))

            #self.screen = pygame.display.set_mode((self.w, self.h))
            try:
                new_idx = curr_idx + move
                new_idx = new_idx if (new_idx >= 0 and new_idx <= len(characters)-1) else curr_idx
            except Exception as e:
                print(e)
                new_idx = curr_idx
        else:
            new_idx = curr_idx

        new_char = characters[new_idx]

        self.screen.blit(new_char, rect)
        return new_idx

    def change_track(self, key, curr_idx: int, tracks: list, rect: pygame.Rect):
        d = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1}
        move = d.get(key)
        print(f"MOVE: {move}")

        if move is not None:
            self.screen.blit(self.menu_img, (0,0))
            #self.screen = pygame.display.set_mode((self.w, self.h))
            try:
                new_idx = curr_idx + move
                new_idx = new_idx if (new_idx >= 0 and new_idx <= len(tracks)-1) else curr_idx
            except Exception as e:
                print(e)
                new_idx = curr_idx
        else:
            new_idx = curr_idx

        new_char = tracks[new_idx]

        Manager.draw_text(screen=self.screen, txt=new_char, size=40, x=self.cursor_rect.right + 50, 
                          y=self.cursor_rect.y + self.offset*(5))

        pygame.mixer.pause()
        pygame.mixer.music.load(self.track_path[new_idx])

        return new_idx
    
    def choose_char_screen(self):
        # Reset screen
        self.reset_screen()

        # Characters to display upon selection time
        characters = [pygame.transform.scale(pygame.image.load(i), (100, 160)) for i in self.char_path]

        # Rect for information
        rect = pygame.Rect(0,0,0,0)
        rect.center, curr_idx = (self.cursor_rect.right, self.cursor_rect.y+self.offset*4), 0

        # Loop for character choice
        chosen_char = []
        RUN, BACK_FLAG = True, False
        for p in ['Player1', 'Player2']:
            curr_idx = 0
            while RUN:
                Manager.draw_text(screen=self.screen, 
                                  txt=p, size=40, 
                                  x=self.cursor_rect.right + 50, 
                                  y=self.cursor_rect.y - self.offset, 
                                  c=(255, 0, 0)
                                  )
                opt_y = [Manager.draw_text(screen=self.screen, txt=opt, size=40, x=self.cursor_rect.right + 50, 
                                           y=self.cursor_rect.y + self.offset*(idx)) 
                         for idx, opt in enumerate(self.opt['CHOOSE CHARACTER'])]
                # Keys
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        RUN = False
                    
                    if event.type == pygame.KEYDOWN:
                        curr_idx = self.change_char(key=event.key, curr_idx=curr_idx, 
                                                    characters=characters, rect=rect)

                        if event.key==pygame.K_RETURN:
                            img_path = os.sep.join(self.char_path[curr_idx].split(os.sep)[-3:])
                            chosen_char.append(img_path)
                            RUN = False

                        if event.key == pygame.K_ESCAPE:
                            RUN = False
                            BACK_FLAG = True

                # Update display
                pygame.display.update()
            if BACK_FLAG:
                break
            else:
                RUN = True
        
        # Back to the main screen
        self.chosen_char = chosen_char
        self.reset_screen()
    
    def soundtrack_screen(self):
        # Reset screen
        self.reset_screen()

        # Songs to display upon selection time
        track_names = [t.split(os.sep)[-1].split('.')[0] + 'Sound' if t is not None else 'No sound' for t in self.track_path]

        # Rect for information
        rect = pygame.Rect(0,0,0,0)
        rect.center, curr_idx = (self.cursor_rect.right, self.cursor_rect.y+self.offset*4), 0

        # Loop for character choice
        RUN = True
        chosen_track, curr_idx, pause_flag = None, 0, 0
        while RUN:
            Manager.draw_text(screen=self.screen, 
                                txt='Choose the soundtrack', size=40, 
                                x=self.cursor_rect.right + 50, 
                                y=self.cursor_rect.y - self.offset, 
                                c=(0, 0, 0)
                                )
            opt_y = [Manager.draw_text(screen=self.screen, txt=opt, size=40, x=self.cursor_rect.right + 50, 
                                        y=self.cursor_rect.y + self.offset*(idx)) 
                        for idx, opt in enumerate(self.opt['CHOOSE SOUNDTRACK'])]
            # Keys
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUN = False

                if event.type == pygame.KEYDOWN:
                    curr_idx = self.change_track(key=event.key, curr_idx=curr_idx, 
                                                tracks=track_names, rect=rect)

                    if event.key==pygame.K_RETURN:
                        track_path = os.sep.join(self.track_path[curr_idx].split(os.sep)[-3:])
                        chosen_track = track_path
                        RUN = False

                    if event.key == pygame.K_ESCAPE:
                        RUN = False

                    if event.key == pygame.K_p:
                        pygame.mixer.pause() if pause_flag else pygame.mixer.music.play(-1)
                        pause_flag = abs(pause_flag-1)

            # Update display
            pygame.display.update()

        # Back to the main screen
        self.chosen_track = chosen_track
        self.reset_screen()

    def play_screen(self):
        self.reset_screen()
        try:
            if len(self.chosen_char) == 2:
                args = self.chosen_char + [self.chosen_track]
                run_game(*args)
        except Exception as e:
            print(e)
            print("Player characters not defined yet.")

    def pause_menu(self):
        pause_menu = PauseMenu(self.w, self.h)
        pause_menu.pause_screen()


class PauseMenu:
    def __init__(self, s_width: int, s_height: int):
        pygame.init()
        self.w, self.h = s_width, s_height

        self.offset = +50
        self.cursor_y = None
        self.cursor_str = None

        self.opt = {'PAUSE': ['RESUME GAME', 'BACK MENU', 'QUIT GAME'], 
                    'QUIT': ['YES', 'NO']}

        self.opt_map = {'RESUME GAME': self.resume_game,
                        'BACK MENU': self.restart_game,
                        'QUIT GAME': self.quit_game
                        }

        self.char_path = glob.glob(os.path.join(CHAR_PATH, '*.*'))
        self.track_path = [None] + glob.glob(os.path.join(SOUNDTRACK_PATH, '*.*'))
        self.menu_path = glob.glob(os.path.join(MENU_PATH, '*.*'))

        self.chosen_char = self.char_path[:2]
        self.chosen_track = self.track_path[0]
        self.chosen_menu = self.menu_path[0]

        self.reset_screen()
    
    def reset_screen(self):
        self.menu_img = pygame.transform.scale(pygame.image.load(self.chosen_menu), (self.w, self.h))
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.screen.blit(self.menu_img, (0,0))
        self.cursor_rect = pygame.Rect([20, self.w-self.w//2, 30, 30])

    def draw_text(self, txt, size, x, y, c: tuple = (0, 0, 0)):
        font = pygame.font.SysFont(name='consolas', size=size)
        text_surface = font.render(txt, True, c)
        text_rect = text_surface.get_rect()
        text_rect.left = x
        text_rect.centery = y
        self.screen.blit(text_surface, text_rect)
        return y

    def change_cursor(self, key, opt_y, opt_str):
        d = {pygame.K_UP: -1, pygame.K_DOWN: 1}
        move = d.get(key)

        if move is not None:
            self.screen.blit(self.menu_img, (0,0))
            #self.screen = pygame.display.set_mode((self.w, self.h))
            try:
                cursor_idx = np.where(self.cursor_y == np.array(opt_y))[0][0]
                new_idx = cursor_idx + move
                new_idx = new_idx + (0 if (new_idx >= 0 and new_idx <= len(opt_y)-1) else -move)
                new_cursor_y = opt_y[new_idx]
                new_cursor_str = opt_str[new_idx]
            except Exception as e:
                print(e)
                new_cursor_y = self.cursor_y
                new_cursor_str = self.cursor_str
        else:
            new_cursor_y = self.cursor_y
            new_cursor_str = self.cursor_str

        self.cursor_y = Manager.draw_text(screen=self.screen, txt='>', size=40, 
                                          x=self.cursor_rect.right-30,
                                          y=new_cursor_y)
        self.cursor_str = new_cursor_str

    def resume_game(self):
        # Unpause the game
        pygame.mixer.music.unpause()
        pygame.time.wait(200)

    def restart_game(self):
        # Restart the game
        pygame.mixer.music.stop()
        pygame.time.wait(200)
        self.reset_screen()
        run_game(*args)  # Replace with your game function and its arguments

    def quit_game(self):
        # Quit the game
        pygame.quit()
        sys.exit()

    def pause_screen(self):
        self.cursor_y = self.draw_text(txt='>', size=40, 
                                       x=self.cursor_rect.right-30, y=self.cursor_rect.y)
        self.cursor_str = self.opt['PAUSE'][0]

        PAUSED = True
        while PAUSED:
            pygame.mixer.pause()

            opt_y = [self.draw_text(txt=opt, size=40, 
                                    x=self.cursor_rect.right + 50, 
                                    y=self.cursor_rect.y + self.offset * idx) 
                     for idx, opt in enumerate(self.opt['PAUSE'])]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.change_cursor(key=event.key, opt_y=opt_y, 
                                       opt_str=self.opt['PAUSE'])

                    if event.key == pygame.K_RETURN:
                        self.opt_map[self.cursor_str]()

            pygame.display.update()



# RUNS THE GAME
def run_game(p1_path: str, p2_path: str, track_path: str):
    # Initialize pygame
    #pygame.init()

    keys1 = [K_LEFT, K_RIGHT, K_UP, K_SPACE]
    keys2 = [K_a, K_d, K_w, K_r]
    print(K_a)

    # Background image
    bg_img = pygame.image.load('img/bg/grass_with_house.png')

    # Define constants for the screen width and height
    SCREEN_WIDTH = bg_img.get_width()
    SCREEN_HEIGHT = bg_img.get_height()

    # Background soundtrack
    try:
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battle")

    # Player icon
    p1 = Fighter(20, bg_img.get_height() - 30, 100, 200,
                 icon_path=p1_path,
                 player=True, screen=screen, keys=keys1, mac=None)
    p2 = Fighter(bg_img.get_width() - 230, bg_img.get_height() - 30, 100, 200,
                 icon_path=p2_path,
                 player=True, screen=screen, keys=keys2, mac=None)
    RUN = True

    p1.smartphone_connect() if p1.mac is not None else None
    p2.smartphone_connect() if p2.mac is not None else None

    PAUSED = False
    pause_menu = PauseMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    winner = None
    slid_inc = 100
    end_flag = False
    while RUN:
        # Draw backgroundkeys1 = [K_LEFT, K_RIGHT, K_UP, K_SPACE]
        draw_bg(screen=screen, winner=winner, bg_img=bg_img, ended=end_flag, slid_inc=slid_inc)
        for event in pygame.event.get():
            print(event)

            if event.type == pygame.QUIT:
                RUN = False
            if event.type == KEYUP:
                p1.update_pos(key=event.key)
                p2.update_pos(key=event.key)
                p1.attack(key=event.key, p_op=p2)
                p2.attack(key=event.key, p_op=p1)

            # Check for key press events
            if event.type == KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    # Toggle the pause state
                    PAUSED = not PAUSED
                    if PAUSED:
                        pause_menu.__init__(500, 700)
                        pygame.mixer.music.pause()
                        pause_menu.pause_screen()
                    else:
                        pause_menu.__init__(SCREEN_WIDTH, SCREEN_HEIGHT)
                        pygame.mixer.music.unpause()


        p1.update_pos(key=p1.smartphone_control()) if p1.c is not None else None
        p2.update_pos(key=p2.smartphone_control()) if p2.c is not None else None
        p1.update_pos(key='')
        p2.update_pos(key='')
        change_constraints(p1, p2)
        p1.draw()
        p2.draw()
        pygame.display.update()
        if p1.hp * p2.hp <= 0 and not end_flag:
            winner = "P1 player won the match" if np.greater(p1.hp, p2.hp) else \
                "P2 player won the match"
            end_flag = True
            pygame.mixer.music.load("soundtrack/win_sound/win_sound.wav")
            pygame.mixer.music.play(1)
    pygame.quit()


if __name__ == '__main__':
    m = MainMenu(500, 700)