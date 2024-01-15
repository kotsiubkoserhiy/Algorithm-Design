import random
from tkinter import messagebox
from copy import deepcopy

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
CARD_VALUES = {'6': 6, '7': 7, '8': 8, '9': 0, '10': 10, 'Jack': 2, 'Queen': 3, 'King': 4, 'Ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.points = 0

    def draw(self, deck):
        card = deck.deal()
        if card:
            self.hand.append(card)

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        return None

    def score(self):
        self.points = sum(CARD_VALUES[card.rank] for card in self.hand)
        return self.points

class ComputerPlayer(Player):

    def __str__(self):
        return self.name
    def computer_move(self, game):
        best_move = self.minimax(game, 2, True)[1]
        return best_move

class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.players = [Player(name) for name in players]
        self.table_cards = []
        self.current_player_index = 0
        self.deck.shuffle()
        self.deal_cards()

    def deal_cards(self):
        for player in self.players:
            for _ in range(5):
                player.draw(self.deck)
        self.table_cards.append(self.deck.deal())

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def is_playable(self, card):
        top_card = self.table_cards[-1]
        if card.rank == 'Queen':
            return True
        elif card.rank == 'King' and card.suit == 'Spades':
            return top_card.rank == 'King' or top_card.suit == 'Spades'
        elif card.rank in ['9', '7', '6']:
            return card.suit == top_card.suit or card.rank == top_card.rank
        return card.suit == top_card.suit or card.rank == top_card.rank

    def play_card(self):
        if hasattr(self, 'selected_card') and self.selected_card in self.game.players[
            self.game.current_player_index].hand:
            current_player = self.game.players[self.game.current_player_index]
            # Наявність карт
            if current_player.hand:
                try:
                    current_player.play_card(self.selected_card)
                    self.game.table_cards.append(self.selected_card)
                    self.game.next_turn()
                    self.update_info()
                    if self.master.winfo_exists():
                        self.update_hand_display()
                except ValueError as e:
                    messagebox.showerror("Помилка", str(e))
            else:
                messagebox.showerror("Помилка", "Гравець не має карт.")
        else:
            messagebox.showerror("Помилка", "Виберіть карту.")

    def apply_special_rules(self, card):
        if card.rank == 'Ace':
            # Тузи
            if self.current_player_index < len(self.players) - 1:
                next_player = self.players[self.current_player_index + 1]
                if next_player.hand:
                    print(f"{next_player.name} пропускає свій хід через туза.")
                self.next_turn()

        elif card.rank == 'Queen':
            # Дами
            print(f"{self.players[self.current_player_index].name} кладе даму.")
            suit_choice = input("Виберіть масть (Hearts, Diamonds, Clubs, Spades): ")
            self.table_cards[-1].suit = suit_choice
            self.next_turn()

        elif card.rank == 'King' and card.suit == 'Spades':
            # Піковий король
            print(f"{self.players[self.current_player_index].name} кладе пікового короля.")
            if self.current_player_index < len(self.players) - 1:
                next_player = self.players[self.current_player_index + 1]
                for _ in range(4):
                    next_player.draw(self.deck)
                print(f"{next_player.name} бере 4 картки з колоди.")
                self.next_turn()

        elif card.rank == '9':
            # Девʼятки
            print(f"{self.players[self.current_player_index].name} кладе дев'ятку.")
            matching_suit = self.table_cards[-1].suit
            while True:
                next_card = self.player_choice(self.players[self.current_player_index])
                if next_card and next_card.suit == matching_suit:
                    break
                else:
                    self.players[self.current_player_index].draw(self.deck)
                    print(f"{self.players[self.current_player_index].name} бере карту з колоди.")
            self.next_turn()

        elif card.rank == '7':
            # Сімки
            print(f"{self.players[self.current_player_index].name} кладе семерку.")
            if self.current_player_index < len(self.players) - 1:
                next_player = self.players[self.current_player_index + 1]
                for _ in range(2):
                    next_player.draw(self.deck)
                print(f"{next_player.name} бере 2 картки з колоди.")
                self.next_turn()

        elif card.rank == '6':
            # Шістки
            print(f"{self.players[self.current_player_index].name} кладе шестерку.")
            if self.current_player_index < len(self.players) - 1:
                next_player = self.players[self.current_player_index + 1]
                next_player.draw(self.deck)
                print(f"{next_player.name} бере 1 карту з колоди.")
                self.next_turn()

        if card.rank == 'Queen':
            # Закінчення гри при закінченні ходу на даму
            for player in self.players:
                if not player.hand:
                    print(f"Гра закінчилася! {player.name} виграв!")
                    exit()

    def check_game_end(self):
        min_score = float('inf')
        winners = []

        for player in self.players:
            if player.score() > 101:
                messagebox.showinfo("Гра закінчилася", f"{player.name} виграв з {player.score()} очками.")
                return True
            elif not player.hand:
                winners.append(player)
            else:
                min_score = min(min_score, player.score())

        if winners:
            winners_with_min_score = [player for player in winners if player.score() == min_score]
            if len(winners_with_min_score) == 1:
                messagebox.showinfo("Гра закінчилася", f"{winners_with_min_score[0].name} виграв з {min_score} очками.")
                return True
            else:
                messagebox.showinfo("Нічия", "Декілька гравців мають однакову кількість очок.")
                return True

        return False

    def find_winner(self):
        active_players = [player for player in self.players if player.hand]
        return min(active_players, key=lambda p: (p.score(), len(p.hand)))

    def computer_move(self, player):
        if isinstance(player, ComputerPlayer):
            return player.computer_move(self)
        return None

    def play_round(self):
        player = self.players[self.current_player_index]
        if isinstance(player, ComputerPlayer):
            played_card = self.computer_move(player)
        else:
            played_card = self.player_choice(player)

        if played_card:
            player.play_card(played_card)
            self.table_cards.append(played_card)
            self.apply_special_rules(played_card)

        if player.score() > 101:
            player.points = 0

        self.next_turn()
        self.check_game_end()

    def play(self):
        while not self.check_game_end():
            self.play_round()
            self.next_turn()

        winner = self.find_winner()
        print(f"The winner is {winner.name} with {winner.score()} points.")

    def minimax(self, player, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.check_game_end():
            return self.evaluate_game_state(player)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(player):
                simulated_game_state = self.apply_move(player, move)
                eval = simulated_game_state.minimax(
                    simulated_game_state.players[simulated_game_state.current_player_index],
                    depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(player):
                simulated_game_state = self.apply_move(player, move)
                eval = simulated_game_state.minimax(
                    simulated_game_state.players[simulated_game_state.current_player_index],
                    depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_possible_moves(self, player):
        top_card = self.table_cards[-1]
        possible_moves = []
        for card in player.hand:
            if card.rank == 'Queen' or card.suit == top_card.suit or card.rank == top_card.rank:
                possible_moves.append(card)
            elif card.rank == 'King' and card.suit == 'Spades' and (
                    top_card.rank == 'King' or top_card.suit == 'Spades'):
                possible_moves.append(card)
            elif card.rank in ['9', '7', '6'] and (card.suit == top_card.suit or card.rank == top_card.rank):
                possible_moves.append(card)
        return possible_moves

    def apply_move(self, player, card):
        new_game_state = deepcopy(self)
        player_in_new_state = new_game_state.players[new_game_state.current_player_index]
        player_in_new_state.play_card(card)
        new_game_state.table_cards.append(card)
        new_game_state.apply_special_rules(card)
        return new_game_state

    def evaluate_game_state(self, player):
        score = sum(CARD_VALUES[card.rank] for card in player.hand)
        if player.hand and player.hand[-1].rank == 'Queen':
            if player.hand[-1].suit == 'Spades':
                score -= 40  # Зменшення очків, якщо кінець на піковій дамі
            else:
                score -= 20  # Зменшення очків, якщо кінець на дамі
        return score


