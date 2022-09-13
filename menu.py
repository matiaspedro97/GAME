import pygame
import numpy as np
import glob
from constants import *


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
    def draw_text(screen, txt, size, x, y, c: tuple = (0, 255, 0)):
        font = pygame.font.SysFont(name='arial', size=size)
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

        self.opt = {'MAIN': ['PLAY', 'CHOOSE CHARACTER', 'SETTINGS', 'QUIT'], 
                    'CHOOSE CHARACTER': ['-> NEXT', '<- PREVIOUS'],
                    'SETTINGS': ['SOUND'],
                    'QUIT': ['YES', 'NO']}

        self.opt_map = {'PLAY': self.play_screen,
                        'CHOOSE CHARACTER': self.choose_char_screen, 
                        'SETTINGS': self.settings_screen, 
                        'QUIT': pygame.quit
                        }

        self.char_path = glob.glob(os.path.join(CHAR_PATH, '*_rev.*'))
        self.chosen_char = self.char_path[:2]

        self.start_screen()
    
    def reset_screen(self):
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.cursor_rect = pygame.Rect([20, self.w-self.w//2, 30, 30])

    def start_screen(self):
        self.reset_screen()

        RUN = True
        self.cursor_y = Manager.draw_text(screen=self.screen, txt='->', size=40, 
                                          x=self.cursor_rect.right - 30, y=self.cursor_rect.y)

        while RUN:
            opt_y = [Manager.draw_text(screen=self.screen, txt=opt, size=40, x=self.cursor_rect.right + 50, 
                                       y=self.cursor_rect.y + self.offset * idx) 
                     for idx, opt in enumerate(self.opt['MAIN'])]

            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    RUN = False
                if event.type == pygame.KEYDOWN:
                    self.change_cursor(key=event.key, cursor_y=self.cursor_y, opt_y=opt_y)

                    if event.key==pygame.K_RETURN:
                        print('sgdfgkhjgh')
                        self.choose_char_screen()

            pygame.display.update()
        pygame.quit()
    
    def change_cursor(self, key, cursor_y, opt_y):
        d = {pygame.K_UP: -1, pygame.K_DOWN: 1}
        move = d.get(key)

        if move is not None:
            self.screen = pygame.display.set_mode((self.w, self.h))
            try:
                cursor_idx = np.where(cursor_y == np.array(opt_y))[0][0]
                new_idx = cursor_idx + move
                new_cursor_y = opt_y[new_idx] if (new_idx >= 0 and new_idx <= len(opt_y)-1) else cursor_y
            except Exception as e:
                print(e)
                new_cursor_y = cursor_y
        else:
            new_cursor_y = cursor_y

        self.cursor_y = Manager.draw_text(screen=self.screen, txt='->', size=40, 
                                              x=self.cursor_rect.right-30,
                                              y=new_cursor_y)
    
    def change_char(self, key, curr_idx: int, characters: list, rect: pygame.Rect):
        d = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1}
        move = d.get(key)
        print(f"MOVE: {move}")

        if move is not None:
            self.screen = pygame.display.set_mode((self.w, self.h))
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
    
    def choose_char_screen(self):
        self.reset_screen()

        characters = [pygame.transform.scale(pygame.image.load(i), (100, 160)) for i in self.char_path]
        print(f"CHARS: {len(characters)}")
        rect = pygame.Rect(0,0,0,0)
        rect.center, curr_idx = (self.cursor_rect.right, self.cursor_rect.y+self.offset*4), 0

        chosen_char = []
        for p in ['Player1', 'Player2']:
            RUN = True
            curr_idx = 0
            print(p)
            while RUN:
                Manager.draw_text(screen=self.screen, txt=p, size=40, x=self.cursor_rect.right + 50,
                                  y=self.cursor_rect.y - self.offset, c=(255, 0, 0))
                opt_y = [Manager.draw_text(screen=self.screen, txt=opt, size=40, x=self.cursor_rect.right + 50,
                                        y=self.cursor_rect.y + self.offset*(idx)) 
                         for idx, opt in enumerate(self.opt['CHOOSE CHARACTER'])]
                for event in pygame.event.get():
                    print(event)

                    if event.type == pygame.QUIT:
                        RUN = False
                    
                    if event.type == pygame.KEYDOWN:
                        curr_idx = self.change_char(key=event.key, curr_idx=curr_idx, 
                                                    characters=characters, rect=rect)

                        if event.key==pygame.K_RETURN:
                            chosen_char.append(self.char_path[curr_idx])
                            RUN = False
                pygame.display.update()
        
        # Back to the main screen
        self.chosen_char = chosen_char if len(chosen_char) == 2 else self.chosen_char
        self.reset_screen()
    
    def play_screen(self):
        raise NotImplementedError
    
    def settings_screen(self):
        raise NotImplementedError


class PauseMenu:
    def __init__(self, width, height):
        screen = pygame.display.set_mode((width, height))


if __name__ == '__main__':
    m = MainMenu(500, 700)
