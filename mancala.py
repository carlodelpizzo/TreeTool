import random
import os


class Mancala:
    def __init__(self):
        self.board = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.max_index = 5
        self.pot = [0, 0]
        self.move_count = 0
        self.move_count_fine = [0, 0]
        self.hand = 0
        self.current_player = 0
        self.game_over = False
        self.move_history = []

    def move_is_valid(self, hole_choice: int):
        hole_choice = hole_choice % (self.max_index + 1)
        if self.board[self.current_player][hole_choice] != 0:
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

    def play_move(self, hole_choice: int):
        hole_choice = hole_choice % (self.max_index + 1)
        self.move_count += 1
        self.move_count_fine[self.current_player] += 1
        hand_index = hole_choice + 1
        current_side = self.current_player
        if self.board[self.current_player][hole_choice] != 0:
            self.hand = self.board[self.current_player][hole_choice]
            self.board[self.current_player][hole_choice] = 0
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
        self.move_history.append([self.current_player, hole_choice])

        if hand_index == 0 and current_side != self.current_player:
            pass
        else:
            self.current_player = (self.current_player + 1) % 2

    def first_hole_strategy(self):
        no_move_available = True
        for i in range(len(self.board[self.current_player])):
            if self.board[self.current_player][i] != 0:
                self.play_move(i)
                return
        if no_move_available:
            self.current_player = (self.current_player + 1) % 2

    def last_hole_strategy(self):
        no_move_available = True
        for i in reversed(range(len(self.board[self.current_player]))):
            if self.board[self.current_player][i] != 0:
                self.play_move(i)
                return
        if no_move_available:
            self.current_player = (self.current_player + 1) % 2

    def random_hole_strategy(self):
        random_hole = random.randint(0, self.max_index)
        if self.move_is_valid(random_hole):
            self.play_move(random_hole)
        else:
            self.random_hole_strategy()

    def heaviest_hole_strategy(self):
        heaviest = 0
        for h in range(self.max_index + 1):
            print(self.board[self.current_player][h])

    def utility_function(self, hole_choice: int):
        hole_choice = hole_choice % (self.max_index + 1)
        bead_count = self.board[self.current_player][hole_choice]
        cycle_number = (((self.max_index + 1) * 2) + 1)
        opp_player = (self.current_player + 1) % 2
        final_index = (hole_choice + bead_count) % cycle_number
        full_passes = int((bead_count - 1) / cycle_number)

        utility = 0
        if self.move_is_valid(hole_choice):
            # If move results in 2nd turn
            if (self.max_index + 1) - hole_choice == bead_count % cycle_number:
                utility += 1.5

            # Number of beads landing in pot
            if (self.max_index + 1) - hole_choice <= bead_count:
                utility += (1 + int(bead_count / cycle_number))

            # If move ends on opposing players side
            if final_index >= 7:
                for i in reversed(range(0, final_index - (self.max_index + 1))):
                    # If move blocks opposing player from potential 2nd turn
                    if ((self.max_index + 1) - i) == self.board[opp_player][i] % cycle_number:
                        utility += 0.5
                    # If move gives opposing player a potential 2nd turn
                    elif ((self.max_index + 1) - i) == (self.board[opp_player][i] + full_passes + 1) % cycle_number:
                        utility -= 0.5

            # If move captures opposing beads
            if full_passes == 0 and 0 <= final_index <= self.max_index:
                if final_index == hole_choice or self.board[self.current_player][final_index] == 0:
                    utility += (self.board[opp_player][self.max_index - final_index]) * 2

        return utility

    def utility_function_alt(self, hole_choice: int):
        hole_choice = hole_choice % (self.max_index + 1)
        bead_count = self.board[self.current_player][hole_choice]
        cycle_number = (((self.max_index + 1) * 2) + 1)
        opp_player = (self.current_player + 1) % 2
        final_index = (hole_choice + bead_count) % cycle_number
        full_passes = int((bead_count - 1) / cycle_number)

        utility = 0
        if self.move_is_valid(hole_choice):
            # If move results in 2nd turn
            if (self.max_index + 1) - hole_choice == bead_count % cycle_number:
                utility += 10

            # Number of beads landing in pot
            if (self.max_index + 1) - hole_choice <= bead_count:
                utility += (1 + int(bead_count / cycle_number))

            # If move ends on opposing players side
            if final_index >= 7:
                for i in reversed(range(0, final_index - (self.max_index + 1))):
                    # If move blocks opposing player from potential 2nd turn
                    if ((self.max_index + 1) - i) == self.board[opp_player][i] % cycle_number:
                        utility += 0.5
                    # If move gives opposing player a potential 2nd turn
                    elif ((self.max_index + 1) - i) == (self.board[opp_player][i] + full_passes + 1) % cycle_number:
                        utility -= 0.5

            # If move captures opposing beads
            if full_passes == 0 and 0 <= final_index <= self.max_index:
                if final_index == hole_choice or self.board[self.current_player][final_index] == 0:
                    utility += 2

        return utility

    def find_highest_utility(self, func):
        # Returns list of holes which have the highest utility for current player
        # [hole index, utility value]
        best_ut = [0, 0]
        possible_moves = []
        secondary = []
        for h in range(0, self.max_index + 1):
            ut = func(h)
            possible_moves.append([h, ut])
            if ut > best_ut[1]:
                best_ut = [h, ut]
        possible_moves = sorted(possible_moves, key=lambda x: x[1], reverse=True)
        for h in range(1, len(possible_moves)):
            if possible_moves[h][1] == possible_moves[0][1]:
                secondary.append(possible_moves[h])
        if len(secondary) != 0:
            secondary.insert(0, possible_moves[0])
            return secondary
        else:
            return [best_ut]


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


def utility_vs_utility(game: object):
    if game is None:
        game = Mancala()
    best_moves = game.find_highest_utility(game.utility_function)
    if best_moves[0][1] == 0:
        game.random_hole_strategy()
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


def utility_vs_random(game: object):
    if game is None:
        game = Mancala()
    if game.current_player == 0:
        best_moves = game.find_highest_utility(game.utility_function)
        if best_moves[0][1] == 0:
            game.random_hole_strategy()
        elif len(best_moves) == 1:
            game.play_move(best_moves[0][0])
        else:
            ran = random.randint(0, len(best_moves) - 1)
            game.play_move((best_moves[ran][0]))
    else:
        game.random_hole_strategy()


def random_vs_utility(game: object):
    if game is None:
        game = Mancala()
    if game.current_player == 1:
        best_moves = game.find_highest_utility(game.utility_function)
        if best_moves[0][1] == 0:
            game.random_hole_strategy()
        elif len(best_moves) == 1:
            game.play_move(best_moves[0][0])
        else:
            ran = random.randint(0, len(best_moves) - 1)
            game.play_move((best_moves[ran][0]))
    else:
        game.random_hole_strategy()


def alt_utility_vs_random(game: object):
    if game is None:
        game = Mancala()
    if game.current_player == 0:
        best_moves = game.find_highest_utility(game.utility_function_alt)
        if best_moves[0][1] == 0:
            game.random_hole_strategy()
        elif len(best_moves) == 1:
            game.play_move(best_moves[0][0])
        else:
            ran = random.randint(0, len(best_moves) - 1)
            game.play_move((best_moves[ran][0]))
    else:
        game.random_hole_strategy()


def random_vs_alt_utility(game: object):
    if game is None:
        game = Mancala()
    if game.current_player == 1:
        best_moves = game.find_highest_utility(game.utility_function_alt)
        if best_moves[0][1] == 0:
            game.random_hole_strategy()
        elif len(best_moves) == 1:
            game.play_move(best_moves[0][0])
        else:
            ran = random.randint(0, len(best_moves) - 1)
            game.play_move((best_moves[ran][0]))
    else:
        game.random_hole_strategy()


def utility_vs_alt_utility(game: object):
    if game is None:
        game = Mancala()
    if game.current_player == 0:
        best_moves = game.find_highest_utility(game.utility_function)
        if best_moves[0][1] == 0:
            game.random_hole_strategy()
        elif len(best_moves) == 1:
            game.play_move(best_moves[0][0])
        else:
            ran = random.randint(0, len(best_moves) - 1)
            game.play_move((best_moves[ran][0]))
    else:
        best_moves = game.find_highest_utility(game.utility_function_alt)
        if best_moves[0][1] == 0:
            game.random_hole_strategy()
        elif len(best_moves) == 1:
            game.play_move(best_moves[0][0])
        else:
            ran = random.randint(0, len(best_moves) - 1)
            game.play_move((best_moves[ran][0]))


def alt_utility_vs_utility(game: object):
    if game is None:
        game = Mancala()
    if game.current_player == 1:
        best_moves = game.find_highest_utility(game.utility_function)
        if best_moves[0][1] == 0:
            game.random_hole_strategy()
        elif len(best_moves) == 1:
            game.play_move(best_moves[0][0])
        else:
            ran = random.randint(0, len(best_moves) - 1)
            game.play_move((best_moves[ran][0]))
    else:
        best_moves = game.find_highest_utility(game.utility_function_alt)
        if best_moves[0][1] == 0:
            game.random_hole_strategy()
        elif len(best_moves) == 1:
            game.play_move(best_moves[0][0])
        else:
            ran = random.randint(0, len(best_moves) - 1)
            game.play_move((best_moves[ran][0]))


def simulate_games(depth: int, strategy: str, show_progress=False):
    game = Mancala()
    score_count = [0, 0]
    win_count = [0, 0, 0]
    counter = 0
    while True:
        while not game.game_over:
            # Utility vs Utility
            if strategy == 'utility vs utility':
                utility_vs_utility(game)

            # Utility vs Random
            elif strategy == 'utility vs random':
                utility_vs_random(game)

            # Random vs Utility
            elif strategy == 'random vs utility':
                random_vs_utility(game)

            # Alt Utility vs Random
            elif strategy == 'alt utility vs random':
                alt_utility_vs_random(game)

            # Random vs Alt Utility
            elif strategy == 'random vs alt utility':
                random_vs_alt_utility(game)

            # Utility vs Random with random first move
            elif strategy == 'utility vs random rfm':
                if game.move_count_fine[game.current_player] == 0:
                    game.random_hole_strategy()
                else:
                    utility_vs_random(game)

            # Utility vs Utility with random first move
            elif strategy == 'utility vs utility rfm':
                if game.move_count_fine[game.current_player] == 0:
                    game.random_hole_strategy()
                else:
                    utility_vs_utility(game)

            # Utility vs Alt Utility
            elif strategy == 'utility vs alt utility':
                utility_vs_alt_utility(game)

            # Alt Utility vs Utility
            elif strategy == 'alt utility vs utility':
                alt_utility_vs_utility(game)

            # Random vs Random
            else:
                strategy = strategies[0]
                game.random_hole_strategy()

        score_count[0] += game.pot[0]
        score_count[1] += game.pot[1]

        if game.pot[0] > game.pot[1]:
            win_count[0] += 1
        elif game.pot[1] > game.pot[0]:
            win_count[1] += 1
        else:
            win_count[2] += 1

        game.__init__()

        counter += 1
        if show_progress and counter % 1000 == 0:
            print(str(counter) + ' / ' + str(depth))

        if counter == depth:
            score_norm = [score_count[0], score_count[1]]
            if score_norm[0] >= score_norm[1]:
                score_norm[0] = int((score_norm[0] / score_norm[1]) * 10000)
                score_norm[0] /= 10000
                score_norm[1] = 1.0
            else:
                score_norm[1] = int((score_norm[1] / score_norm[0]) * 10000)
                score_norm[1] /= 10000
                score_norm[0] = 1.0

            return [score_count, score_norm, win_count, strategy]


strategies = ['random vs random', 'utility vs random', 'random vs utility', 'utility vs utility',
              'utility vs random rfm', 'utility vs utility rfm', 'utility vs alt utility', 'alt utility vs utility',
              'alt utility vs random', 'random vs alt utility']

strat = strategies[1]
sim_depth = 1000

temp = Mancala()
temp.heaviest_hole_strategy()

# for s in range(0, len(strategies)):
#     output = simulate_games(sim_depth, strategies[s])
#
#     print(output[3])
#     print('Score:', output[0], 'Normalized:', output[1])
#     print('Win Count:', output[2])
#     print('\n')
