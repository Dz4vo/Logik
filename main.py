import pygame
import random
import itertools
pygame.init()

# farby
WHITE = (120, 120, 120)
BLACK = (30, 30, 30)
DARKBROWN = (55, 22, 30)
GREEN = (0, 210, 0)
BLUE = (0, 0, 200)
RED = (210, 0, 0)
YELLOW = (210, 210, 0)
PINK = (255, 0, 255)
ORANGE = (210, 110, 0)
COLOR= [RED, GREEN, BLUE, YELLOW, PINK, ORANGE, BLACK]
color=["červená","zelená","modrá","žltá","ružová","oranžová","čierna"]

# volanie z konzoly
def get_number(x,k,l):
    while True:
        try:
            number = int(input("Zadajte " +str(x)+ "(číslo od " + str(k)+ " do " +str(l)+ "): "))
            if k <= number <= l:
                return number
            else:
                print("Číslo musí byť od " + str(k)+ " do " +str(l) )
        except ValueError:
            print("Toto nie je číslo")

#konštanty
LENGHT=get_number("dĺžku hľadanej postupnosti",3,6)
AMOUNT_COLOUR = get_number("počet farieb ",LENGHT,min(7,2*LENGHT))
TRIES=get_number("počet pokusov",5,10)
ROWS = LENGHT
COLS = TRIES+4
TILESIZE = 40
COLOURS=COLOR[:AMOUNT_COLOUR]
colours=color[:AMOUNT_COLOUR]


WIDTH = (ROWS * TILESIZE) + 1
HEIGHT = (COLS * TILESIZE) + 1
FPS = 60
TITLE = "Logik"

#určovanie hintu
guesses=[]
answers=[]
every=list(itertools.product(range(AMOUNT_COLOUR), repeat=LENGHT))

def compare(guess,actual):
    r=0
    w=0
    remaining_guess=[]
    remaining_actual=[]
    for i in range(len(guess)):
        if guess[i]==actual[i]:
            r+=1
        else:
            remaining_guess.append(guess[i])
            remaining_actual.append(actual[i])
    for x in remaining_guess:
        if x in remaining_actual:
            w+=1
            remaining_actual.remove(x)
    return [r,w]

def bestmove(guesses,answers,every):
    for i in range(len(guesses)):
        every= [x for x in every if compare(guesses[i],x)==answers[i]]
    return " ".join([colours[x] for x in every[random.randrange(len(every))]])
#tlačidlo a jeho funkcie
class Button:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, LENGHT*TILESIZE, TILESIZE)
        self.color = GREEN
        self.hover_color = RED
        self.text = "HINT"
        self.text_color = WHITE
        self.is_pressed = False



    def drawB(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
            if pygame.mouse.get_pressed()[0]: 
                 if not self.is_pressed:
                    print(bestmove(guesses,answers,every)) 
                    self.is_pressed=True
             
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
#kolíky a ich funkcie
class Pin:
    def __init__(self, x, y, colour=None, revealed=True):
        self.x, self.y = x, y
        self.colour = colour
        self.revealed = revealed

    def draw(self, screen):
        center = (self.x + (TILESIZE/2), self.y + (TILESIZE/2))
        if self.colour is not None and self.revealed:
            pygame.draw.circle(screen, tuple(x * 0.3 for x in self.colour), tuple(x + 1 for x in center), 15)
            pygame.draw.circle(screen, self.colour, center, 15)
        elif not self.revealed:
            pygame.draw.circle(screen, BLACK, center, 15)

        else:
            pygame.draw.circle(screen, DARKBROWN, center, 10)
# doska 
class Board:
    def __init__(self):
    
        self.tries = TRIES
        self.pins_surface = pygame.Surface((LENGHT*TILESIZE, (TRIES+4)*TILESIZE))
        self.pins_surface.fill(WHITE)

        self.colour_selection_surface = pygame.Surface((LENGHT*TILESIZE, 2*TILESIZE))
        self.colour_selection_surface.fill(WHITE)

        self.button=Button(0,(TRIES+3)*TILESIZE)
# tvorba priestoru pre kolíky
        self.colour_selection = [Pin(COLOURS.index(x)%ROWS*TILESIZE, COLOURS.index(x)//ROWS*TILESIZE,x) for x in COLOURS]
        self.board_pins = [[Pin(col * TILESIZE, row * TILESIZE) for col in range(LENGHT)] for row in range(TRIES+1)]

        random_code = random.choices(COLOURS,k=LENGHT)
        for i, pin in enumerate(self.board_pins[0]):
            pin.colour = random_code[i]
            pin.revealed = False
       
    def draw(self, screen):

        for pin in self.colour_selection:
            pin.draw(self.colour_selection_surface)

 
        for row in self.board_pins:
            for pin in row:
                pin.draw(self.pins_surface)
        
        self.button.drawB(self.pins_surface)

        screen.blit(self.pins_surface, (0,0))
        screen.blit(self.colour_selection_surface, (0, (TRIES+1)*TILESIZE))
        

        pygame.draw.rect(screen, GREEN, (0, TILESIZE*self.tries, LENGHT*TILESIZE, TILESIZE), 2)

  
    def select_colour(self, mouse_x, mouse_y, previous_colour):
        for pin in self.colour_selection:
            if pin.x < mouse_x < pin.x + TILESIZE and pin.y < mouse_y - (TRIES+1)*TILESIZE < pin.y + TILESIZE:
                return pin.colour

        return previous_colour

    def place_pin(self, mouse_x, mouse_y, colour):
        for pin in self.board_pins[self.tries]:
            if pin.x < mouse_x < pin.x + TILESIZE and pin.y < mouse_y < pin.y + TILESIZE:
                pin.colour = colour
                break

    def check_row(self):
        return all(pin.colour is not None for pin in self.board_pins[self.tries])

      
    def check_clues(self):
        r=0
        w=0
        remaining_guess=[]
        remaining_secrets=[]
        for i in range(LENGHT):
            if self.board_pins[self.tries][i].colour==self.board_pins[0][i].colour:
                r+=1
            else:
               remaining_guess.append(self.board_pins[self.tries][i].colour)
               remaining_secrets.append(self.board_pins[0][i].colour)
        for x in remaining_guess:
            if x in remaining_secrets:
                w+=1
                remaining_secrets.remove(x)

        guesses.append([COLOURS.index(x.colour) for x in self.board_pins[self.tries]])
        answers.append([r,w])
        return r,w


    def next_round(self):
        self.tries -= 1
        self.button.is_pressed=False
        return self.tries > 0

    def reveal_code(self):
        for pin in self.board_pins[0]:
            pin.revealed = True
  


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        self.board = Board() 
        self.colour = None

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()

    def update(self):
        self.screen.fill(WHITE)
        self.board.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.enter()

    def mouse_click(self, position):
        mouse_x, mouse_y = position
        self.colour = self.board.select_colour(mouse_x, mouse_y, self.colour)
        if self.colour is not None:
            self.board.place_pin(mouse_x, mouse_y, self.colour)

    def enter(self):
        if self.board.check_row():
            result = self.board.check_clues()
            print(result[0], result[1])
            if result[0] == LENGHT:
                print("Vyhrali ste!")
                self.board.reveal_code()
                self.end_screen()
            elif not self.board.next_round():
                print("Koniec hry!")
                self.board.reveal_code()
                self.end_screen()

    def end_screen(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            self.update()



game = Game()
while True:
    game.new()
    game.run()
