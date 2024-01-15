import unittest
from Logic_game import Deck, Player, Game, Card

class TestCardGame(unittest.TestCase):
    def test_deck_shuffling(self):
        deck = Deck()
        original_order = deck.cards.copy()
        deck.shuffle()
        shuffled_order = deck.cards

        self.assertNotEqual(original_order, shuffled_order, "Deck wasn't shuffled.")
        self.assertEqual(set(original_order), set(shuffled_order), "Shuffled deck contains the same cards.")
        self.assertEqual(len(original_order), len(shuffled_order), "Shuffled deck has the same number of cards.")

    def test_deck_initialization(self):
        deck = Deck()

        self.assertEqual(len(deck.cards), 36, "Incorrect number of cards in the deck.")
        self.assertTrue(all(isinstance(card, Card) for card in deck.cards), "Not all elements in the deck are cards.")

    def test_player_initialization(self):
        player_name = "Test Player"
        player = Player(player_name)

        self.assertEqual(player.name, player_name, "Incorrect player name.")
        self.assertEqual(len(player.hand), 0, "Player's hand is not empty initially.")
        self.assertEqual(player.points, 0, "Player's points are not initialized to zero.")

    def test_game_next_turn(self):
        players = ["Player 1", "Player 2"]
        game = Game(players)

        initial_current_player_index = game.current_player_index
        game.next_turn()
        new_current_player_index = game.current_player_index

        self.assertNotEqual(initial_current_player_index, new_current_player_index, "Next turn did not change the current player.")
        self.assertEqual(new_current_player_index, (initial_current_player_index + 1) % len(game.players), "Incorrect calculation of the next player index.")

if __name__ == '__main__':
    unittest.main()
