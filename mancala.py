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

    def current_player_move(self, hole_choice: int):
        hole_choice = hole_choice % (self.max_index + 1)
        self.move_count += 1
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

    def utility_function(self, hole_choice: int):
        hole_choice = hole_choice % (self.max_index + 1)
        bead_count = self.board[self.current_player][hole_choice]
        cycle_number = (((self.max_index + 1) * 2) + 1)
        opp_player = (self.current_player + 1) % 2
        final_index = (hole_choice + bead_count) % cycle_number
        full_passes = int(bead_count / cycle_number)

        utility = 0
        if self.move_is_valid(hole_choice):
            # If move results in 2nd turn
            if (self.max_index + 1) - hole_choice == bead_count % cycle_number:
                utility += 2

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
            if final_index <= self.max_index:
                if self.board[self.current_player][final_index] == 0:
                    utility += self.board[opp_player][self.max_index - final_index]

        return utility


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

cumulative_score = [0, 0]

strategy = 'utility random'

sim_depth = 20000
counter = 0
gaming = True
while gaming:
    while not game.game_over:
        if strategy == 'utility utility':
            # Both players use utility function
            best_move = [0, 0]
            for j in range(0, game.max_index + 1):
                ut = game.utility_function(j)
                if ut > best_move[1]:
                    best_move = [j, ut]
            if best_move[1] == 0:
                game.random_hole_strategy()
            else:
                game.current_player_move(best_move[0])

        elif strategy == 'utility random':
            # Player one uses utility, player 2 uses random
            if game.current_player == 0:
                best_move = [0, 0]
                for j in range(0, game.max_index + 1):
                    ut = game.utility_function(j)
                    if ut > best_move[1]:
                        best_move = [j, ut]
                if best_move[1] == 0:
                    game.random_hole_strategy()
                else:
                    game.current_player_move(best_move[0])
            else:
                game.random_hole_strategy()

    cumulative_score[0] += game.pot[0]
    cumulative_score[1] += game.pot[1]
    game.__init__()

    counter += 1
    if counter % 1000 == 0:
        print(counter)
    if counter == sim_depth:
        gaming = False
        temp = [cumulative_score[0], cumulative_score[1]]
        if cumulative_score[0] >= cumulative_score[1]:
            cumulative_score[0] = int((cumulative_score[0] / cumulative_score[1]) * 10000)
            cumulative_score[0] /= 10000
            cumulative_score[1] = 1
        else:
            cumulative_score[1] = int((cumulative_score[1] / cumulative_score[0]) * 10000)
            cumulative_score[1] /= 10000
            cumulative_score[0] = 1
        print(temp, 'normalized:', cumulative_score)
