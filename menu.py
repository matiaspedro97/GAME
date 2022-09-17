from hashlib import new
import pygame
import numpy as np
import glob
from constants import *
from test import *


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
        self.cursor_str = None

        self.opt = {'MAIN': ['PLAY', 'CHOOSE CHARACTER', 'CHOOSE SOUNDTRACK', 'QUIT'], 
                    'CHOOSE CHARACTER': ['-> NEXT', '<- PREVIOUS'],
                    'CHOOSE SOUNDTRACK': ['-> NEXT', '<- PREVIOUS', 'P <- PLAY'],
                    'QUIT': ['YES', 'NO']}

        self.opt_map = {'PLAY': self.play_screen,
                        'CHOOSE CHARACTER': self.choose_char_screen, 
                        'CHOOSE SOUNDTRACK': self.soundtrack_screen, 
                        'QUIT': pygame.quit
                        }

        self.char_path = glob.glob(os.path.join(CHAR_PATH, '*.*'))
        self.track_path = [None] + glob.glob(os.path.join(SOUNDTRACK_PATH, '*.*'))

        self.chosen_char = self.char_path[:2]
        self.chosen_track = self.track_path[0]

        self.start_screen()
    
    def reset_screen(self):
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.cursor_rect = pygame.Rect([20, self.w-self.w//2, 30, 30])

    def start_screen(self):
        self.reset_screen()

        RUN = True
        self.cursor_y = Manager.draw_text(screen=self.screen, txt='->', size=40, 
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
            self.screen = pygame.display.set_mode((self.w, self.h))
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

        self.cursor_y = Manager.draw_text(screen=self.screen, txt='->', size=40, 
                                              x=self.cursor_rect.right-30,
                                              y=new_cursor_y)
        self.cursor_str = new_cursor_str
    
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

    def change_track(self, key, curr_idx: int, tracks: list, rect: pygame.Rect):
        d = {pygame.K_LEFT: -1, pygame.K_RIGHT: 1}
        move = d.get(key)
        print(f"MOVE: {move}")

        if move is not None:
            self.screen = pygame.display.set_mode((self.w, self.h))
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
                                c=(255, 0, 0)
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
                        pygame.mixer.music.play(-1) if not pause_flag else pygame.mixer.pause()
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


class PauseMenu:
    def __init__(self, width, height):
        screen = pygame.display.set_mode((width, height))


if __name__ == '__main__':
    m = MainMenu(500, 700)
