from turtle import Screen
import pygame
import random
import itertools

pygame.init()

WHITE = (120, 120, 120)
BLACK = (30, 30, 30)
DARKBROWN = (55, 22, 30)
GREEN = (0, 210, 0)
BLUE = (0, 0, 200)
RED = (210, 0, 0)
YELLOW = (210, 210, 0)
PINK = (255, 0, 255)
ORANGE = (210, 110, 0)
BEIGE=(245,245,220)
COLORS = [RED, GREEN, BLUE, YELLOW, PINK, ORANGE, BLACK]
COLOR_NAMES = ["červená", "zelená", "modrá", "žltá", "ružová", "oranžová", "čierna"]

def get_number(prompt, min_val, max_val):
    while True:
        try:
            number = int(input(f"Zadajte {prompt} (číslo od {min_val} do {max_val}): "))
            if min_val <= number <= max_val:
                return number
            else:
                print(f"Číslo musí byť od {min_val} do {max_val}")
        except ValueError:
            print("Toto nie je číslo")

LENGTH = get_number("dĺžku hľadanej postupnosti", 3, 6)
AMOUNT_COLORS = get_number("počet farieb", 3, 6)
TRIES = get_number("počet pokusov", 5, 10)
ROWS = LENGTH+1
COLS = TRIES + 5
SQUARE = 40
GAME_COLORS = COLORS[:AMOUNT_COLORS]
GAME_COLOR_NAMES = COLOR_NAMES[:AMOUNT_COLORS]

WIDTH = (ROWS * SQUARE) + 1
HEIGHT = (COLS * SQUARE) + 1
FPS = 60
TITLE = "Logik"

guesses = []
answers = []
all_combinations = list(itertools.product(range(AMOUNT_COLORS), repeat=LENGTH))

def compare(guess, actual):
    red_pegs = 0
    white_pegs = 0
    remaining_guess = []
    remaining_actual = []

    for i in range(len(guess)):
        if guess[i] == actual[i]:
            red_pegs += 1
        else:
            remaining_guess.append(guess[i])
            remaining_actual.append(actual[i])

    for peg in remaining_guess:
        if peg in remaining_actual:
            white_pegs += 1
            remaining_actual.remove(peg)

    return [red_pegs, white_pegs]

def knuth(possible_combinations):
    best_guess = None
    max_eliminated = -1

    for guess in possible_combinations:
        min_eliminated = AMOUNT_COLORS ** LENGTH

        for red_pegs in range(LENGTH + 1):
            for white_pegs in range(LENGTH - red_pegs + 1):
                eliminated = sum(1 for comb in possible_combinations if compare(guess, comb) != [red_pegs, white_pegs])
                min_eliminated = min(len(possible_combinations) - eliminated, min_eliminated)

        if min_eliminated > max_eliminated:
            best_guess = guess
            max_eliminated = min_eliminated

    return best_guess

def best_move(guesses, answers, all_combinations):
    possible_combinations = all_combinations.copy()

    for guess, answer in zip(guesses, answers):
        possible_combinations = [comb for comb in possible_combinations if compare(guess, comb) == answer]

    if len(possible_combinations) > 300 or len(answers) == 0:
        return " ".join([GAME_COLOR_NAMES[x] for x in random.choice(possible_combinations)])
    elif len(possible_combinations) != 1:
        return " ".join([GAME_COLOR_NAMES[x] for x in knuth(possible_combinations)])
    else:
        return " ".join([GAME_COLOR_NAMES[x] for x in possible_combinations[0]])

class Button:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, LENGTH * SQUARE, SQUARE)
        self.color = GREEN
        self.hover_color = RED
        self.text = "HINT"
        self.text_color = WHITE
        self.is_pressed = False

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
            if pygame.mouse.get_pressed()[0] and not self.is_pressed:
                print(best_move(guesses, answers, all_combinations))
                self.is_pressed = True
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Pin:
    def __init__(self, x, y, color=None, revealed=True):
        self.x = x
        self.y = y
        self.color = color
        self.revealed = revealed

    def draw(self, screen):
        center = (self.x + SQUARE // 2, self.y + SQUARE // 2)
        if self.color and self.revealed:
            pygame.draw.circle(screen, self.color, center, 15)
        elif not self.revealed:
            pygame.draw.circle(screen, BLACK, center, 15)
        else:
            pygame.draw.circle(screen, DARKBROWN, center, 10)

class Board:
    def __init__(self):
        self.tries = TRIES

        self.pins_surface = pygame.Surface((LENGTH * SQUARE, (TRIES + 4) * SQUARE))
        self.pins_surface.fill(BEIGE)

        self.color_selection_surface = pygame.Surface((LENGTH * SQUARE, 2 * SQUARE))
        self.color_selection_surface.fill(DARKBROWN)

        self.clue_display_surface=pygame.Surface((SQUARE,(TRIES+4)*SQUARE))
        self.clue_display_surface.fill(BEIGE)

        self.button = Button(0, (TRIES + 3) * SQUARE)
        self.color_selection = [Pin(i % ROWS * SQUARE, i // ROWS * SQUARE, color) for i, color in enumerate(GAME_COLORS)]
        self.board_pins = [[Pin(col * SQUARE, row * SQUARE) for col in range(LENGTH)] for row in range(TRIES + 1)]
      

        random_code = random.choices(GAME_COLORS, k=LENGTH)
        for i, pin in enumerate(self.board_pins[0]):
            pin.color = random_code[i]
            pin.revealed = False

    def draw(self, screen):
        for pin in self.color_selection:
            pin.draw(self.color_selection_surface)

        for row in self.board_pins:
            for pin in row:
                pin.draw(self.pins_surface)
            
        self.button.draw(self.pins_surface)
        screen.blit(self.pins_surface, (0, 0))
        screen.blit(self.color_selection_surface, (0, (TRIES + 1) * SQUARE))
        screen.blit(self.clue_display_surface,(LENGTH*SQUARE,0))
     
        pygame.draw.rect(screen, GREEN, (0, self.tries * SQUARE, LENGTH * SQUARE, SQUARE), 2)

    def select_color(self, mouse_x, mouse_y, previous_color):
        for pin in self.color_selection:
            if pin.x < mouse_x < pin.x + SQUARE and pin.y < mouse_y - (TRIES + 1) * SQUARE < pin.y + SQUARE:
                return pin.color

        return previous_color

    def place_pin(self, mouse_x, mouse_y, color):
        for pin in self.board_pins[self.tries]:
            if pin.x < mouse_x < pin.x + SQUARE and pin.y < mouse_y < pin.y + SQUARE:
                pin.color = color
                break

    def check_row(self):
        return all(pin.color is not None for pin in self.board_pins[self.tries])

    def check_clues(self):
        red_pegs = 0
        white_pegs = 0
        remaining_guess = []
        remaining_secret = []

        for i in range(LENGTH):
            if self.board_pins[self.tries][i].color == self.board_pins[0][i].color:
                red_pegs += 1
            else:
                remaining_guess.append(self.board_pins[self.tries][i].color)
                remaining_secret.append(self.board_pins[0][i].color)

        for peg in remaining_guess:
            if peg in remaining_secret:
                white_pegs += 1
                remaining_secret.remove(peg)

        guesses.append([GAME_COLORS.index(pin.color) for pin in self.board_pins[self.tries]])
        answers.append([red_pegs, white_pegs])
        return red_pegs, white_pegs

    def display_clues(self,value_1,value_2):
        font = pygame.font.Font(None, SQUARE)
        red_peg = font.render(value_1, True, RED)
        white_peg=font.render(value_2,True,WHITE)
        self.clue_display_surface.blit(red_peg,(0,(self.tries+0.25)*SQUARE))
        self.clue_display_surface.blit(white_peg,(0.5*SQUARE,(self.tries+0.25)*SQUARE))


    def next_round(self):
        self.tries -= 1
        self.button.is_pressed = False
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

    def new_game(self):
        self.board = Board()
        self.selected_color = None

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.handle_events()
            self.update_screen()

    def update_screen(self):
        self.screen.fill(WHITE)
        self.board.draw(self.screen)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.handle_enter()

    def handle_mouse_click(self, position):
        mouse_x, mouse_y = position
        self.selected_color = self.board.select_color(mouse_x, mouse_y, self.selected_color)
        if self.selected_color:
            self.board.place_pin(mouse_x, mouse_y, self.selected_color)

    def handle_enter(self):
        if self.board.check_row():
            result = self.board.check_clues()
            self.board.display_clues(str(result[0]),str(result[1]))
            if result[0] == LENGTH:
                print("Vyhrali ste!")
                self.board.reveal_code()
                self.show_end_screen()
            elif not self.board.next_round():
                print("Koniec hry!")
                self.board.reveal_code()
                self.show_end_screen()

    def show_end_screen(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            self.update_screen()
  

if __name__ == "__main__":
    game = Game()
    while True:
        game.new_game()
        game.run()
