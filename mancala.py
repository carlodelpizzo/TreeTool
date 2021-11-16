import random
import os


class Mancala:
    def __init__(self):
        self.board = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.max_index = 5
        self.pot = [0, 0]
        self.move_count = 0
        self.hand = 0
        self.current_player = 0
        self.game_over = False
        self.move_history = []

    def move_is_valid(self, pot_choice: int):
        pot_choice = pot_choice % (self.max_index + 1)
        if self.board[self.current_player][pot_choice] != 0:
            return True
        else:
            return False

    def ending_condition_check(self):
        current_player_sum = 0
        for hole in self.board[self.current_player]:
            current_player_sum += hole
        other_player_sum = 0
        for hole in self.board[(self.current_player + 1) % 2]:
            other_player_sum += hole
        if current_player_sum == 0 or other_player_sum == 0:
            if current_player_sum != 0:
                self.pot[self.current_player] += current_player_sum
                for i in range(len(self.board[self.current_player])):
                    self.board[self.current_player][i] = 0
            if other_player_sum != 0:
                other_i = (self.current_player + 1) % 2
                self.pot[other_i] += other_player_sum
                for i in range(len(self.board[other_i])):
                    self.board[other_i][i] = 0
            self.game_over = True

    def current_player_move(self, pot_choice: int):
        # print('before player ' + str(self.current_player) + ' move: ', self.board)
        pot_choice = pot_choice % (self.max_index + 1)
        self.move_count += 1
        hand_index = pot_choice + 1
        current_side = self.current_player
        if self.board[self.current_player][pot_choice] != 0:
            self.hand = self.board[self.current_player][pot_choice]
            self.board[self.current_player][pot_choice] = 0
        if self.hand > 0:
            while self.hand > 0:
                if 0 <= hand_index <= self.max_index:
                    self.board[current_side][hand_index] += 1
                    self.hand -= 1
                    hand_index += 1
                elif current_side == self.current_player and hand_index > self.max_index:
                    self.pot[current_side] += 1
                    self.hand -= 1

                    hand_index = 0
                    current_side = (current_side + 1) % 2
                else:
                    hand_index = 0
                    current_side = (current_side + 1) % 2
                    self.board[current_side][hand_index] += 1
                    self.hand -= 1
                    hand_index += 1

        # Special condition for capture
        if current_side == self.current_player and self.board[current_side][hand_index - 1] == 1:
            other_i = (current_side + 1) % 2
            self.board[current_side][hand_index - 1] = 0
            self.pot[self.current_player] += self.board[other_i][(len(self.board[other_i]) - 1) - (hand_index - 1)] + 1
            self.board[other_i][(len(self.board[other_i]) - 1) - (hand_index - 1)] = 0

        self.ending_condition_check()
        self.move_history.append([self.current_player, pot_choice])

        # print('player ' + str(self.current_player) + ' plays pot ' + str(pot_choice) + ': ', self.board,
        #       '\nScore: ', self.pot, '\n# of Moves: ', self.move_count, '\n----')

        if hand_index == 0 and current_side != self.current_player:
            pass
        else:
            self.current_player = (self.current_player + 1) % 2

    def first_hole_strategy(self):
        no_move_available = True
        for i in range(len(game.board[self.current_player])):
            if self.board[self.current_player][i] != 0:
                self.current_player_move(i)
                return
        if no_move_available:
            self.current_player = (self.current_player + 1) % 2

    def last_hole_strategy(self):
        no_move_available = True
        for i in reversed(range(len(game.board[self.current_player]))):
            if self.board[self.current_player][i] != 0:
                self.current_player_move(i)
                return
        if no_move_available:
            self.current_player = (self.current_player + 1) % 2

    def random_hole_strategy(self):
        random_hole = random.randint(0, self.max_index)
        if self.move_is_valid(random_hole):
            self.current_player_move(random_hole)
        else:
            self.random_hole_strategy()


def write_lines_to_history_file(lines: list):
    if os.path.isfile('history_file.txt'):
        history_file = open('history_file.txt', 'r', errors='ignore')
        temp_array = []
        for line in history_file:
            temp_array.append(line)
        history_file.close()
        history_file = open('history_file.txt', 'w', errors='ignore')
        for line in temp_array:
            history_file.writelines(line)
    else:
        history_file = open('history_file.txt', 'w', errors='ignore')
    history_file.writelines(lines)
    history_file.close()


def overwrite_history_file(lines: list):
    history_file = open('history_file.txt', 'w', errors='ignore')
    history_file.writelines(lines)
    history_file.close()


game = Mancala()

write_lines_to_history_file(['*****************************NEW INSTANCE*****************************\n'])

max_moves = 0
max_depth = 1000
counter = 0
gaming = True
while gaming:
    while not game.game_over:
        game.random_hole_strategy()
    if game.move_count > max_moves:
        max_moves = game.move_count
        print('current highest: ', max_moves)
        history_lines = ['Current Highest # of Moves: ' + str(max_moves) + '\n']
        for move in game.move_history:
            history_lines.append(str(move[0] + 1) + ', ' + str(move[1] + 1) + '\n')
        history_lines.append('---------\n')
        write_lines_to_history_file(history_lines)
        counter = 0
    game.__init__()
    # counter += 1
    # if counter == max_depth:
    #     gaming = False

print('highest: ', max_moves)
