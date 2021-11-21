import pygame


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
    def draw_text(screen, txt, size, x, y):
        font = pygame.font.SysFont(name='arial', size=size)
        text_surface = font.render(txt, True, (0, 255, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_surface, text_rect)


class MainMenu:
    def __init__(self, s_width, s_height, options):
        pygame.init()
        self.screen = pygame.display.set_mode((s_width, s_height))
        self.cursor_rect = pygame.Rect([20, s_width-100, 30, 30])
        self.offset = -50
        RUN = True
        while RUN:

            Manager.draw_text(screen=self.screen, txt='*', size=40, x=self.cursor_rect.right,
                              y=self.cursor_rect.y)
            [Manager.draw_text(screen=self.screen, txt=opt, size=40, x=self.cursor_rect.right + 30,
                               y=self.cursor_rect.y - 50*(idx)) for idx, opt in enumerate(options)]
            for event in pygame.event.get():
                print(event)

                if event.type == pygame.QUIT:
                    RUN = False
            pygame.display.update()
        pygame.quit()


class PauseMenu:
    def __init__(self, width, height):
        screen = pygame.display.set_mode((width, height))
