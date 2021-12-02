import random
import os
import itertools


class Mancala:
    def __init__(self):
        self.board = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.max_index = len(self.board[0]) - 1
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


# Strategies
def first_hole_strategy(game: object, give_name=False):
    if give_name:
        return 'first hole'
    if game is None:
        game = Mancala()
    no_move_available = True
    for i in range(len(game.board[game.current_player])):
        if game.board[game.current_player][i] != 0:
            game.play_move(i)
            return
    if no_move_available:
        game.current_player = (game.current_player + 1) % 2


def last_hole_strategy(game: object, give_name=False):
    if give_name:
        return 'last hole'
    if game is None:
        game = Mancala()
    no_move_available = True
    for i in reversed(range(len(game.board[game.current_player]))):
        if game.board[game.current_player][i] != 0:
            game.play_move(i)
            return
    if no_move_available:
        game.current_player = (game.current_player + 1) % 2


def random_hole_strategy(game: object, give_name=False):
    if give_name:
        return 'random hole'
    if game is None:
        game = Mancala()
    random_hole = random.randint(0, game.max_index)
    if game.move_is_valid(random_hole):
        game.play_move(random_hole)
    else:
        random_hole_strategy(game)


def heaviest_hole_strategy(game: object, prefer_closest=True, give_name=False):
    if give_name:
        return 'heaviest hole'
    if game is None:
        game = Mancala()
    if not prefer_closest:
        heaviest = 0
        for h in range(game.max_index + 1):
            if game.board[game.current_player][h] > game.board[game.current_player][heaviest]:
                heaviest = h
    else:
        heaviest = game.max_index
        for h in reversed(range(game.max_index + 1)):
            if game.board[game.current_player][h] > game.board[game.current_player][heaviest]:
                heaviest = h
    game.play_move(heaviest)


def utility_strategy(game: object, give_name=False):
    if give_name:
        return 'utility'
    if game is None:
        game = Mancala()
    best_moves = game.find_highest_utility(game.utility_function)
    if best_moves[0][1] == 0:
        random_hole_strategy(game)
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


def alt_utility_strategy(game: object, give_name=False):
    if give_name:
        return 'alt utility'
    if game is None:
        game = Mancala()
    best_moves = game.find_highest_utility(game.utility_function)
    if best_moves[0][1] == 0:
        random_hole_strategy(game)
    elif len(best_moves) == 1:
        game.play_move(best_moves[0][0])
    else:
        ran = random.randint(0, len(best_moves) - 1)
        game.play_move((best_moves[ran][0]))


# Strategies to be simulated
strategies = [random_hole_strategy, heaviest_hole_strategy, utility_strategy, alt_utility_strategy]

all_combinations = []
for strat in itertools.product(strategies, strategies):
    all_combinations.append(strat)


# Simulation functions
def strat_vs_strat(game: object, strat1, strat2):
    if game is None:
        game = Mancala()
    if game.current_player == 0:
        strat1(game)
    else:
        strat2(game)


def simulate_games(depth: int, strat1=None, strat2=None, show_progress=False, print_result=True):
    game = Mancala()

    strategy = ''
    if strat1 is not None and strat2 is not None:
        strat1_name = strat1(game, give_name=True)
        strat2_name = strat2(game, give_name=True)
        strategy = strat1_name + ' vs ' + strat2_name

    score_count = [0, 0]
    win_count = [0, 0, 0]
    counter = 0
    while True:
        while not game.game_over:
            # Strat vs Strat
            if strat1 is not None and strat2 is not None:
                strat_vs_strat(game, strat1, strat2)

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

            if print_result:
                print(strategy)
                print('Score:', score_count, 'Normalized:', score_norm)
                print('Win Count:', win_count)
                print('\n')
            return [score_count, score_norm, win_count, strategy]


sim_depth = 1000

# simulate_games(sim_depth, strat1=utility_strategy, strat2=random_hole_strategy)

sim_all_strategies = True
if sim_all_strategies:
    for s in all_combinations:
        simulate_games(sim_depth, strat1=s[0], strat2=s[1])
