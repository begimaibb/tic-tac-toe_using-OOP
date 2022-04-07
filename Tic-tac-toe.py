from random import randint

class Field:
    def __init__(self, field_size: int = 3) -> None:
        self.field_size = field_size
        # self.playing_field = [[None]*3 for _ in self.field_size]
        self.playing_field = []
        for _ in range(self.field_size):
            self.playing_field.append([None]*3)
        self.free_cells = field_size ** 2

    def __checking_coordinates(self, x:int, y:int):
        if x > self.field_size - 1 or y > self.field_size - 1 or x < 0 or y < 0:
            raise ValueError(f"The coordinate ({x}, {y}) is out of field")
        if self.field_is_free(x, y):
            raise ValueError(f"The cell ({x}, {y}) has already a content")

    def field_is_free(self, x:int, y:int):
        return self.playing_field[x][y]

    def set_value(self, x: int, y: int, char: str):
        self.__checking_coordinates(x, y)
        self.playing_field[x][y] = char
        self.free_cells -= 1

    def __str__(self):
        result_field = []
        # top_line = f"{self.field_size * ' '}|{'|'.join([f'{num:^{self.field_size}}'for num in range(self.field_size)])}\n"
        top_cell_list = [' ' * self.field_size] 
        for num in range(self.field_size):
            top_cell_list.append(f'{num:^{self.field_size}}')
        top_line = ("|".join(top_cell_list)) + "\n"
        result_field.append(top_line)

        for index, row in enumerate(self.playing_field):
            rows_list = [f"{index:<{self.field_size}}"]
            for cell in row:
                rows_list.append(f'{cell or "":^{self.field_size}}')
            result_row = ('|'.join(rows_list)) + "\n"
            # result_row = f"{index:<{self.field_size}}|{'|'.join([f'{cell or str():^{self.field_size}}' for cell in row])}\n"
            result_field.append(result_row)
        return f"{'-'*len(top_line)}\n".join(result_field)

    def display(self):
        line_len = self.field_size ** 2 + 3 + self.field_size
        print(f"{' ' * self.field_size}", end="")
        for num in range(self.field_size):
            print(f'|{num:^{self.field_size}}', end="")
        print(f"\n{'-'* line_len}")
        for index, row in enumerate(self.playing_field):
            print(f"{index:<{self.field_size}}", end="")
            for cell in row:
                print(f'|{cell or "":^{self.field_size}}', end="")
            if index != self.field_size - 1:
                print(f"\n{'-'*line_len}")
            else:
                print()



class Player:
    def __init__(self, char: str, field: Field) -> None:
        self.char = char
        self.field = field

    def _get_coordinates(self):
        while True:
            try:
                x = int(input("Enter x-coordinate: "))
                y = int(input("Enter y-coordinate: "))
                return x, y
            except ValueError:
                print("The coordinates should be whole numbers")

    def make_move(self):
        while True:
            try:
                x, y = self._get_coordinates()
                self.field.set_value(x, y, self.char)
                break
            except ValueError as e:
                print(e)



class Bot(Player):
    def _get_coordinates(self):
        while True:
            x = randint(0, 2)
            y = randint(0, 2)
            if not self.field.field_is_free(x, y):
                break
        return x, y



class Checker:
    def __init__(self, char: str, field: Field) -> None:
        self.char = char
        self.field = field

    def check_horizontally(self):
        for i in range(3):
            is_winning = True
            for j in range(3):
                if self.field.playing_field[i][j] != self.char:
                    is_winning = False
            if is_winning:
                return True
        return False

    def check_vertically(self):
        for j in range(3):
            is_winning = True
            for i in range(3):
                if self.field.playing_field[i][j] != self.char:
                    is_winning = False
            if is_winning:
                return True
        return False
    
    def check_diagonally(self):
        is_winning = True
        for i in range(3):
            if self.field.playing_field[i][i] != self.char:
                is_winning = False
        for i in range(3):
            if self.field.playing_field[i][2 - i] != self.char:
                is_winning = False
        
        if is_winning:
            return True
        return False

    


class Game:
    def __init__(self,) -> None:
        pass
        
    def main_loop(self):
        player = int(input("Choose the playing method (1 player or 2 players): "))
        field = Field()
        print(field)

        checker_1 = Checker("x", field)
        checker_2 = Checker("o", field)

        if player == 1:
            player_1 = Player("x", field)
            player_2 = Bot("o", field)
        elif player == 2:
            player_1 = Player("x", field)
            player_2 = Player("o", field)
        else:
            print("You can either choose 1-player or 2-player mode")
            return
        
        first_move = randint(0, 1)
        if first_move == 0:
            temp = player_1
            player_1 = player_2
            player_2 = temp

            temp = checker_1
            checker_1 = checker_2
            checker_2 = temp

        
        while True:
            player_1.make_move()
            print(field)

            if checker_1.check_horizontally():
                print("Player 1 won")
                break
            if checker_1.check_vertically():
                print("Player 1 won")
                break
            if checker_1.check_diagonally():
                print("Player 1 won")
                break


            player_2.make_move()
            print(field)

            if checker_2.check_horizontally():
                print("Player 2 won")
                break
            if checker_2.check_vertically():
                print("Player 2 won")
                break
            if checker_2.check_diagonally():
                print("Player 2 won")
                break
        
        
        again = input("Wanna play again?: ")
        if again == "yes":
            self.main_loop()


game = Game()
game.main_loop()