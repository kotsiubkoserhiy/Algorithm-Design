import tkinter as tk
from Logic_game import ComputerPlayer
from tkinter import messagebox
class CardGameUI:
    def __init__(self, master, game):
        self.master = master
        self.game = game
        master.title("101 Game")
        self.player_hand_label = tk.Label(master, text="Ваші картки:")
        self.player_hand_label.pack()
        self.cards_frame = tk.Frame(master)
        self.cards_frame.pack()
        self.update_hand_display()
        self.play_card_button = tk.Button(master, text="Викинути карту", command=self.play_card)
        self.play_card_button.pack()
        self.info_label = tk.Label(master, text="Хід гравця: " + self.game.players[self.game.current_player_index].name)
        self.info_label.pack()
        self.table_cards_label = tk.Label(master, text="Карти на столі: " + str(self.game.table_cards[-1]))
        self.table_cards_label.pack()

    def update_hand_display(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        player = self.game.players[self.game.current_player_index]
        if not isinstance(player, ComputerPlayer):
            for card in player.hand:
                btn = tk.Button(self.cards_frame, text=str(card), command=lambda c=card: self.select_card(c))
                btn.pack(side=tk.LEFT)
        else:
            label = tk.Label(self.cards_frame, text=f"Кількість карт у {player.name}: {len(player.hand)}")
            label.pack(side=tk.LEFT)

    def select_card(self, card):
        self.selected_card = card

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

    def update_info(self):
        current_player_name = str(self.game.players[self.game.current_player_index].name)
        self.info_label.config(text="Хід гравця: " + current_player_name)
        self.table_cards_label.config(text="Карти на столі: " + str(self.game.table_cards[-1]))

        if self.game.check_game_end():
            winner = self.game.find_winner()
            messagebox.showinfo("Гра закінчилася", f"Переможець: {winner.name} з {winner.score()} очками.")

    def play_round(self):
        player = self.game.players[self.game.current_player_index]

        if isinstance(player, ComputerPlayer):
            played_card = self.computer_move(player)
        else:
            played_card = self.player_choice(player)

        if played_card:
            player.play_card(played_card)
            self.game.table_cards.append(played_card)
            self.apply_special_rules(played_card)

        if player.score() > 101:
            player.points = 0

        self.next_turn()
        self.update_interface()

    def update_interface(self):
        self.update_info()
        self.update_hand_display()