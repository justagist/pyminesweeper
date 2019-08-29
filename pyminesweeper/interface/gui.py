
import pygame, sys
from pygame.locals import *
from pyminesweeper.interface import GameInterface
from pyminesweeper.core import Game

# ----- set constants
FPS = 50
WINDOWWIDTH = 800
WINDOWHEIGHT = 900
# BOXSIZE = 30
# GAPSIZE = 5
XMARGIN = 60
YMARGIN = XMARGIN



# ----- define colors 
LIGHTGRAY = (225, 225, 225)
DARKGRAY = (160, 160, 160)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

# ----- assign major colors
BGCOLOR = WHITE
FIELDCOLOR = BLACK
BOXCOLOR_COV = DARKGRAY # covered box color
BOXCOLOR_REV = LIGHTGRAY # revealed box color
MINECOLOR = BLACK
TEXTCOLOR_1 = BLUE
TEXTCOLOR_2 = RED
TEXTCOLOR_3 = BLACK
HILITECOLOR = GREEN
RESETBGCOLOR = LIGHTGRAY
FLAGGEDCELL_COV = RED

# ----- set up font 
FONTTYPE = 'Courier New'
FONTSIZE = 20

class GUI(GameInterface):

    def __init__(self, game):

        super().__init__(game)

        self.FIELDWIDTH, self.FIELDHEIGHT, self.NUM_MINES = game.field_info

        self.BOXSIZE = int((5*(XMARGIN+WINDOWWIDTH))/(7*self.FIELDWIDTH)) 
        self.GAPSIZE = int(self.BOXSIZE/6)
    
        # ----- assertions
        assert self.BOXSIZE^2 * (self.FIELDHEIGHT*self.FIELDWIDTH) < WINDOWHEIGHT*WINDOWWIDTH, 'Boxes will not fit on screen'
        assert self.BOXSIZE/2 > 5, 'Bounding errors when drawing rectangle, cannot use half-5 in draw_mines_and_numbers'

        self._initialise_pygame()

    def _initialise_pygame(self):

        if not pygame.get_init():
            pygame.init()
            pygame.display.set_caption('PyMinesweeper GUI')
            self._FPSCLOCK = pygame.time.Clock()
            self._DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
            self._BASICFONT = pygame.font.SysFont(FONTTYPE, FONTSIZE)

            # ----- obtain reset & show objects and rects
            self._RESET_SURF, self._RESET_RECT = self._draw_button('RESET', TEXTCOLOR_3, RESETBGCOLOR, WINDOWWIDTH/2, WINDOWHEIGHT-120)
            self._SHOW_SURF, self._SHOW_RECT = self._draw_button('REVEAL SOLUTION', TEXTCOLOR_3, RESETBGCOLOR, WINDOWWIDTH/2, WINDOWHEIGHT-95)

            # ----- set background color
        self._DISPLAYSURFACE.fill(BGCOLOR)

    def get_input(self):
        mouse_x, mouse_y, action = [0, 0, None]
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                self._terminate()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                action = Game.GameAction.REVEAL
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                mouse_x, mouse_y = event.pos
                action = Game.GameAction.FLAG

        return mouse_x, mouse_y, action



    def run(self):

        assert self._game.status != Game.GameStatus.NOT_RUNNING, "Error: Game is not Running!"

        while self._game.status == Game.GameStatus.RUNNING:

            mouse1_clicked = False
            mouse2_clicked = False

            # ----- draw field
            self._DISPLAYSURFACE.fill(BGCOLOR)
            pygame.draw.rect(self._DISPLAYSURFACE, FIELDCOLOR, (XMARGIN-5, YMARGIN-5, (self.BOXSIZE+self.GAPSIZE)*self.FIELDWIDTH+5, (self.BOXSIZE+self.GAPSIZE)*self.FIELDHEIGHT+5))

            self._draw_field()
            self._draw_mines_and_numbers() 

            mouse_x, mouse_y, action = self.get_input()

            self._draw_covers()

            tipFont = pygame.font.SysFont(FONTTYPE, 16) ## not using self._BASICFONT - too big
            self._draw_text('Tip: Highlight a box and press space (rather than click the mouse)', tipFont, TEXTCOLOR_3, WINDOWWIDTH/2, WINDOWHEIGHT-60)
            self._draw_text('to mark areas that you think contain mines.', tipFont, TEXTCOLOR_3, WINDOWWIDTH/2, WINDOWHEIGHT-40)

            # ----- determine boxes at clicked areas
            box_x, box_y = self._get_box_at_pixel(mouse_x, mouse_y)

            # ----- mouse not over a box in field
            if (box_x, box_y) == (None, None):

                # ----- check if reset box is clicked
                if self._RESET_RECT.collidepoint(mouse_x, mouse_y):
                    self._hightlight_button(self._RESET_RECT)
                    if action == Game.GameAction.REVEAL: 
                        self._reset_game()

                # ----- check if show box is clicked
                if self._SHOW_RECT.collidepoint(mouse_x, mouse_y):
                    self._hightlight_button(self._SHOW_RECT)
                    if action == Game.GameAction.REVEAL:
                        self.game_lost()

            # ---- mouse currently over box in field
            else:

                # ----- highlight unrevealed box
                if not self._game.minefield[box_x][box_y].is_visible: 
                    self._highlight_box(box_x, box_y)
                        
                    if action is not None:
                        self._game.play_move(box_x, box_y, action)

            # check if player has won 
            if self._game.status == Game.GameStatus.FAILED:
                self.game_lost()

            elif self._game.status == Game.GameStatus.WON:
                self.game_won()

            # ----- redraw screen, wait clock tick
            pygame.display.update()
            self._FPSCLOCK.tick(FPS)

    def _reset_game(self):
        row,col,num_mines = self._game.field_info
        self.__init__(Game(row, col, num_mines, False))


    def game_won(self):
        self._game_over_animation(win=True)
        self._reset_game()

    def game_lost(self):
        self._game.end_and_reveal_field(only_mines = True)
        self._game_over_animation(win=False)
        self._reset_game()

    def _highlight_box(self, box_x, box_y):
        '''
            highlight box when mouse hovers over it
        '''
        left, top = self._get_left_top_xy(box_x, box_y)
        pygame.draw.rect(self._DISPLAYSURFACE, HILITECOLOR, (left, top, self.BOXSIZE, self.BOXSIZE), 4)

    def _game_over_animation(self, win = True):

        origSurf = self._DISPLAYSURFACE.copy()
        flashSurf = pygame.Surface(self._DISPLAYSURFACE.get_size())
        flashSurf = flashSurf.convert_alpha()
        animationSpeed = 20

        if win:
            r, g, b = GREEN
        else:
            r, g, b = RED

        for i in range(5):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, animationSpeed*step):
                    self._check_for_keypress()
                    flashSurf.fill((r, g, b, alpha))
                    self._DISPLAYSURFACE.blit(origSurf, (0, 0))
                    self._DISPLAYSURFACE.blit(flashSurf, (0, 0))
                    pygame.draw.rect(self._DISPLAYSURFACE, FIELDCOLOR, (XMARGIN-5, YMARGIN-5, (self.BOXSIZE+self.GAPSIZE)*self.FIELDWIDTH+5, (self.BOXSIZE+self.GAPSIZE)*self.FIELDHEIGHT+5))
                    self._draw_field()
                    self._draw_mines_and_numbers()
                    tipFont = pygame.font.SysFont(FONTTYPE, 16) ## not using self._BASICFONT - too big
                    self._draw_text('Tip: Highlight a box and right click ', tipFont, TEXTCOLOR_3, WINDOWWIDTH/2, WINDOWHEIGHT-60)
                    self._draw_text('to flag cells that you think contain mines.', tipFont, TEXTCOLOR_3, WINDOWWIDTH/2, WINDOWHEIGHT-40)
                    self._RESET_SURF, self._RESET_RECT = self._draw_button('RESET', TEXTCOLOR_3, RESETBGCOLOR, WINDOWWIDTH/2, WINDOWHEIGHT-120)
                    self._SHOW_SURF, self._SHOW_RECT = self._draw_button('REVEAL SOLUTION', TEXTCOLOR_3, RESETBGCOLOR, WINDOWWIDTH/2, WINDOWHEIGHT-95)
                    self._draw_covers()
                    pygame.display.update()
                    self._FPSCLOCK.tick(FPS)

    def _get_box_at_pixel(self, x, y):
        '''
            gets coordinates of box at mouse coordinates
        '''
        for box_x in range(self.FIELDWIDTH):
            for box_y in range(self.FIELDHEIGHT):
                left, top = self._get_left_top_xy(box_x, box_y)
                boxRect = pygame.Rect(left, top, self.BOXSIZE, self.BOXSIZE)
                if boxRect.collidepoint(x, y):
                    return (box_x, box_y)
        return (None, None)


    def _hightlight_button(self, butRect):
        '''
            highlight button when mouse hovers over it
        '''
        linewidth = 4
        pygame.draw.rect(self._DISPLAYSURFACE, HILITECOLOR, (butRect.left-linewidth, butRect.top-linewidth, butRect.width+2*linewidth, butRect.height+2*linewidth), linewidth)


    def _draw_field(self):
        '''
            draws field GUI and reset button
        '''

        for box_x in range(self.FIELDWIDTH):
            for box_y in range(self.FIELDHEIGHT):
                left, top = self._get_left_top_xy(box_x, box_y)
                pygame.draw.rect(self._DISPLAYSURFACE, BOXCOLOR_REV, (left, top, self.BOXSIZE, self.BOXSIZE))

        self._DISPLAYSURFACE.blit(self._RESET_SURF, self._RESET_RECT)
        self._DISPLAYSURFACE.blit(self._SHOW_SURF, self._SHOW_RECT)

    def _draw_mines_and_numbers(self):
        '''    
            draws mines and numbers onto GUI
            field should have mines and numbers

        '''

        field = self._game.minefield

        half = int(self.BOXSIZE*0.5) 
        quarter = int(self.BOXSIZE*0.25)
        eighth = int(self.BOXSIZE*0.125)
        
        for box_x in range(self.FIELDWIDTH):
            for box_y in range(self.FIELDHEIGHT):
                if field[box_x][box_y].is_visible:
                    left, top = self._get_left_top_xy(box_x, box_y)
                    center_x, center_y = self._get_centre_xy(box_x, box_y)
                    if field[box_x][box_y]._is_mine:
                        pygame.draw.circle(self._DISPLAYSURFACE, MINECOLOR, (left+half, top+half), quarter)
                        pygame.draw.circle(self._DISPLAYSURFACE, WHITE, (left+half, top+half), eighth)
                        pygame.draw.line(self._DISPLAYSURFACE, MINECOLOR, (left+eighth, top+half), (left+half+quarter+eighth, top+half))
                        pygame.draw.line(self._DISPLAYSURFACE, MINECOLOR, (left+half, top+eighth), (left+half, top+half+quarter+eighth))
                        pygame.draw.line(self._DISPLAYSURFACE, MINECOLOR, (left+quarter, top+quarter), (left+half+quarter, top+half+quarter))
                        pygame.draw.line(self._DISPLAYSURFACE, MINECOLOR, (left+quarter, top+half+quarter), (left+half+quarter, top+quarter))
                    else: 
                        num = field[box_x][box_y].get_number()
                        if num in range(1,3):
                            text_colour = TEXTCOLOR_1
                        else:
                            text_colour = TEXTCOLOR_2
                        self._draw_text(str(num), self._BASICFONT, text_colour, center_x, center_y)

    def _draw_covers(self):

        # uses revealedBox FIELDWIDTH x FIELDHEIGHT data structure to determine whether to draw box covering mine/number
        # draw red cover instead of gray cover over marked mines

        for box_x in range(self.FIELDWIDTH):
            for box_y in range(self.FIELDHEIGHT):

                left, top = self._get_left_top_xy(box_x, box_y)
                if self._game.minefield[box_x][box_y].is_flagged:
                    pygame.draw.rect(self._DISPLAYSURFACE, FLAGGEDCELL_COV, (left, top, self.BOXSIZE, self.BOXSIZE), 5)

                if self._game.minefield[box_x][box_y].is_visible:

                    if self._game.minefield[box_x][box_y].get_number() == 0:
                        pygame.draw.rect(self._DISPLAYSURFACE, BOXCOLOR_COV, (left, top, self.BOXSIZE, self.BOXSIZE))
                    # else:
                    #     pygame.draw.rect(self._DISPLAYSURFACE, WHITE, (left, top, self.BOXSIZE, self.BOXSIZE), 5)


    def _get_left_top_xy(self, box_x, box_y):
        '''
            get left & top coordinates for drawing mine boxes
        '''
        left = XMARGIN + box_x*(self.BOXSIZE+self.GAPSIZE)
        top = YMARGIN + box_y*(self.BOXSIZE+self.GAPSIZE)
        return left, top

    def _get_centre_xy(self, box_x, box_y):
        '''
            get center coordinates for drawing mine boxes
        '''
        center_x = XMARGIN + self.BOXSIZE/2 + box_x*(self.BOXSIZE+self.GAPSIZE)
        center_y = YMARGIN + self.BOXSIZE/2 + box_y*(self.BOXSIZE+self.GAPSIZE)
        return center_x, center_y


    def _draw_text(self, text, font, color, x, y):  
        '''
            function to easily draw text and also return object & rect pair
        '''
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.centerx = x
        textrect.centery = y
        self._DISPLAYSURFACE.blit(textobj, textrect)

    def _draw_button(self, text, color, bgcolor, center_x, center_y):
        '''
            similar to drawText but text has bg color and returns obj & rect
        '''

        butSurf = self._BASICFONT.render(text, True, color, bgcolor)
        butRect = butSurf.get_rect()
        butRect.centerx = center_x
        butRect.centery = center_y

        return (butSurf, butRect)

    def _check_for_keypress(self):
        '''
            check if quit or any other key is pressed
        '''
        if len(pygame.event.get(QUIT)) > 0:
            self._terminate()
            
        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            self._terminate()
        return keyUpEvents[0].key


    def _terminate(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    
    gui = GUI(Game(15,15,50,False))

    gui.run()
