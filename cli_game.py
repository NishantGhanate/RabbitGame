import sys
import random

from getkey import getkey, keys

class BG_COLORS:
    GREEN = '\33[32m'
    RED = '\33[31m'
    ENDC = '\x1b[0m'
    BOLD = '\033[1m'

class RabbitGame:
    HELP = """
    Game elements:
    - Rabbit (denoted by the character “r” and “R”)
    - Carrot (denoted by the character “c”)
    - Rabbit hole (denoted by the character “O”)
    - Pathway stone (denoted by the character “-”
    - 1 Rabbit
    - 1 Carrot
    - 1 Rabbit Hole
    - 47 Pathway stones

    Controls:
    - enter to generate map
    - s to start
    - a to go left
    - d to go right
    - p (to pickup carrot) & (to drop carrot in the hole while standing next to it)
    - j to jump across hole


    """
    PATH = '-'
    START_POS = 0
    FINAL_POS = 10
    CARROT = '{}C{}'.format(BG_COLORS.RED, BG_COLORS.ENDC)
    HOLE = '{}O{}'.format(BG_COLORS.GREEN, BG_COLORS.ENDC)
    
    def __init__(self) -> None:
        self.rabbit_position = 0
        self.rabbit = 'r'
        self.game_started = True
        self.carrot_picked = False
        self.counter = 1
        
    def clear_terminal(self) -> None:
        print("\033c", end="")

    def reset(self) -> None:
        self.rabbit_position = 0
        self.rabbit = 'r'

    def generate_map(self) -> None:
        self.map = [RabbitGame.PATH] * RabbitGame.FINAL_POS
        self.carrot_pos, self.hole_pos = random.sample(
            range(1, RabbitGame.FINAL_POS), 2
        )
        self.map[self.rabbit_position] = self.rabbit
        self.map[self.carrot_pos] = RabbitGame.CARROT
        self.map[self.hole_pos] = RabbitGame.HOLE

        self.game_display()
        
    def game_display(self) -> None:
        print(*self.map, end='\n', flush=True)
        self.clear_terminal()
    
    def move_left(self) -> None:
        
        if (
            self.rabbit_position >= RabbitGame.START_POS + 1 and
            self.map[self.rabbit_position -1 ] != RabbitGame.CARROT and
            self.map[self.rabbit_position - 1] != RabbitGame.HOLE
            ):
            self.map[self.rabbit_position] = RabbitGame.PATH
            self.rabbit_position -= 1
            self.map[self.rabbit_position] = self.rabbit
            self.game_display()
            
    def move_right(self) -> None:
        if (
            self.rabbit_position <= RabbitGame.FINAL_POS - 2 and
            self.map[self.rabbit_position + 1] != RabbitGame.CARROT and
            self.map[self.rabbit_position + 1] != RabbitGame.HOLE
            ):
            self.map[self.rabbit_position] = RabbitGame.PATH
            self.rabbit_position += 1
            self.map[self.rabbit_position] = self.rabbit
            self.game_display()

    def jump(self) -> None:
        
        if (
            self.rabbit_position >= RabbitGame.START_POS and
            self.rabbit_position <= RabbitGame.FINAL_POS - 2
            ):
            # rabbit on left side
            if self.rabbit_position + 1 == self.hole_pos:
                self.map[self.rabbit_position] = RabbitGame.PATH
                self.rabbit_position += 2
                self.map[self.rabbit_position] = self.rabbit
                
            elif self.rabbit_position - 1 == self.hole_pos:
                self.map[self.rabbit_position] = RabbitGame.PATH
                self.rabbit_position -= 2
                self.map[self.rabbit_position] = self.rabbit

        self.game_display()

    def pick_up_carrot(self) -> None:
        
        if self.rabbit_position + 1 == self.carrot_pos and not self.carrot_picked:
            self.rabbit = 'R'
            self.map[self.rabbit_position] = RabbitGame.PATH
            self.rabbit_position += 1
            self.map[self.rabbit_position] = self.rabbit
            self.carrot_picked = True
            self.game_display()
            
        elif (
            self.rabbit == 'R' and
            self.rabbit_position + 1 == self.hole_pos or
            self.rabbit_position - 1 == self.hole_pos
            ):
            self.game_started = False
            print('{}Yay game completed !{}'.format(BG_COLORS.GREEN, BG_COLORS.ENDC))
            self.reset()

    def play(self) -> None:
        try :
            while self.game_started:
                action = getkey()

                if action == 'a':
                    self.move_left()

                elif action == 'd':
                    self.move_right()

                elif action == 'j':
                    self.jump()

                elif action == 'p':
                    self.pick_up_carrot()

                elif action == 'esc':
                    break

            # print(
            #     "Would you like to start the game again?\n"
            #     "For yes press Enter or any other key to exit", flush=True
            # )
            # action = ord(getch().lower())
            # if action == 13:
            #     self.start_game()

        except KeyboardInterrupt:
            print("Exited game")
    
    def start_game(self) -> None:
        while True:
            command = getkey()
            if command == keys.ENTER:
                self.generate_map()

            elif command == 's':
                # print('Starting game')
                break

        self.play()

if __name__ == '__main__':
   
    # hacky solution
    if len(sys.argv) >= 2 and sys.argv[1].lower() == '-h':
        print(RabbitGame.HELP)
    else:
        rabbit_game = RabbitGame()
        rabbit_game.start_game()
