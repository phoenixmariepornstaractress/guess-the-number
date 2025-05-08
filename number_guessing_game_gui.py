import random
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QMessageBox, QDialog, QDialogButtonBox, QFormLayout, QComboBox,
    QScrollArea, QTextEdit, QHBoxLayout, QGroupBox,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class GameSettingsDialog(QDialog):
    """
    A dialog for setting game parameters like difficulty and player name.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game Settings")
        self.layout = QFormLayout(self)

        self.player_name_input = QLineEdit(self)
        self.layout.addRow("Player Name:", self.player_name_input)

        self.difficulty_combo = QComboBox(self)
        self.difficulty_combo.addItems(["Easy", "Medium", "Hard", "Custom"])
        self.layout.addRow("Difficulty:", self.difficulty_combo)
        self.difficulty_combo.currentIndexChanged.connect(self.update_custom_attempts_input)

        self.custom_attempts_input = QLineEdit(self)
        self.custom_attempts_input.setPlaceholderText("Enter attempts")
        self.layout.addRow("Custom Attempts:", self.custom_attempts_input)
        self.update_custom_attempts_input()

        self.hints_checkbox = QComboBox(self)
        self.hints_checkbox.addItems(["Yes", "No"])
        self.layout.addRow("Enable Hints:", self.hints_checkbox)

        self.game_mode_combo = QComboBox(self)
        self.game_mode_combo.addItems(["Single Player", "Two Player"])
        self.layout.addRow("Game Mode:", self.game_mode_combo)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addRow(self.button_box)

    def update_custom_attempts_input(self):
        """
        Show/hide the custom attempts input based on the difficulty selection.
        """
        if self.difficulty_combo.currentText() == "Custom":
            self.custom_attempts_input.show()
        else:
            self.custom_attempts_input.hide()

    def get_settings(self):
        """
        Returns the game settings as a dictionary.
        """
        if self.result() == QDialog.Accepted:
            player_name = self.player_name_input.text().strip()
            difficulty = self.difficulty_combo.currentText()
            hints_enabled = self.hints_checkbox.currentText() == "Yes"
            game_mode = self.game_mode_combo.currentText()
            if difficulty == "Custom":
                try:
                    attempts = int(self.custom_attempts_input.text())
                    if attempts <= 0:
                        QMessageBox.warning(self, "Invalid Input", "Attempts must be a positive number.")
                        return None
                except ValueError:
                    QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for attempts.")
                    return None
            else:
                attempts = {"Easy": 10, "Medium": 5, "Hard": 3}[difficulty]
            return {
                "player_name": player_name,
                "difficulty": difficulty,
                "attempts": attempts,
                "hints_enabled": hints_enabled,
                "game_mode": game_mode,
            }
        return None


class NumberGuessingGame(QWidget):
    """
    A GUI-based number guessing game.
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.random_number = 0
        self.max_attempts = 0
        self.attempts_left = 0
        self.player_name = ""
        self.game_started = False
        self.hints_enabled = False
        self.game_mode = "Single Player"
        self.player1_name = ""
        self.player2_name = ""
        self.current_player = 1

    def init_ui(self):
        """
        Initializes the user interface.
        """
        self.setWindowTitle("Number Guessing Game")

        # Title Label
        self.title_label = QLabel("Guess the Number!", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))

        # Instruction Label
        self.instruction_label = QLabel("", self)  # Will be set in start_new_game
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setWordWrap(True)

        # Attempts Label
        self.attempts_label = QLabel("", self)
        self.attempts_label.setAlignment(Qt.AlignCenter)

        # Guess Input
        self.guess_input = QLineEdit(self)
        self.guess_input.setAlignment(Qt.AlignCenter)
        self.guess_input.setPlaceholderText("Enter your guess")

        # Guess Button
        self.guess_button = QPushButton("Guess", self)
        self.guess_button.clicked.connect(self.check_guess)
        self.guess_button.setEnabled(False)

        # Feedback Label
        self.feedback_label = QLabel("", self)
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setFont(QFont("Arial", 12))

        # Settings Button
        self.settings_button = QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.show_settings_dialog)

        # New Game Button
        self.new_game_button = QPushButton("New Game", self)
        self.new_game_button.clicked.connect(self.start_new_game)

        # Game Log
        self.game_log = QTextEdit(self)
        self.game_log.setReadOnly(True)
        self.game_log.setMaximumHeight(200)
        self.game_log.setFont(QFont("Monospace", 10))
        self.log_scroll_area = QScrollArea(self)  # Wrap in a scroll area
        self.log_scroll_area.setWidget(self.game_log)
        self.log_scroll_area.setWidgetResizable(True)
        self.log_label = QLabel("Game Log:", self)

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.instruction_label)
        main_layout.addWidget(self.attempts_label)
        main_layout.addWidget(self.guess_input)
        main_layout.addWidget(self.guess_button)
        main_layout.addWidget(self.feedback_label)
        main_layout.addWidget(self.settings_button)
        main_layout.addWidget(self.new_game_button)
        main_layout.addWidget(self.log_label)
        main_layout.addWidget(self.log_scroll_area)

        self.setGeometry(300, 300, 400, 400)

        # Timer for animations (optional)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_feedback_label)
        self.feedback_colors = ["", "red", "green", "blue", "purple"]
        self.feedback_color_index = 0

    def show_settings_dialog(self):
        """
        Opens the game settings dialog.
        """
        dialog = GameSettingsDialog(self)
        settings = dialog.get_settings()
        if settings:
            self.player_name = settings["player_name"]
            self.max_attempts = settings["attempts"]
            self.attempts_left = self.max_attempts
            self.hints_enabled = settings["hints_enabled"]
            self.game_mode = settings["game_mode"]
            if self.game_mode == "Two Player":
                self.player1_name = self.player_name if self.player_name else "Player 1"
                self.player2_name = "Player 2"  # Simple default for 2nd player.
                self.setWindowTitle("Number Guessing Game - Two Player")
            else:
                self.setWindowTitle("Number Guessing Game - " + self.player_name)
            self.start_new_game()

    def start_new_game(self):
        """
        Starts a new game.
        """
        if self.max_attempts == 0:
            QMessageBox.critical(self, "Error", "Please set the game settings first.")
            return

        self.random_number = random.randint(1, 100)
        self.attempts_left = self.max_attempts
        self.feedback_label.setText("")
        self.guess_input.clear()
        self.guess_button.setEnabled(True)
        self.game_started = True
        self.game_log.clear()
        self.current_player = 1 #reset to player 1
        if self.game_mode == "Two Player":
            self.instruction_label.setText(f"It's {self.player1_name}'s turn to guess.  Number between 1 and 100.")
            self.attempts_label.setText(f"Attempts Left: {self.attempts_left}")
        else:
            self.instruction_label.setText(f"I'm thinking of a number between 1 and 100.  You have {self.attempts_left} attempts left.")
            self.attempts_label.setText(f"Attempts Left: {self.attempts_left}")

    def check_guess(self):
        """
        Checks the user's guess and provides feedback.
        """
        if not self.game_started:
            QMessageBox.critical(self, "Error", "Please start a new game!")
            return

        try:
            guess = int(self.guess_input.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")
            return

        if guess < 1 or guess > 100:
            QMessageBox.warning(self, "Invalid Input", "Please enter a number between 1 and 100.")
            return

        self.attempts_left -= 1
        self.attempts_label.setText(f"Attempts Left: {self.attempts_left}")

        if self.game_mode == "Two Player":
            current_player_name = self.player1_name if self.current_player == 1 else self.player2_name
            self.log_message(f"{current_player_name} guessed {guess}.")
        else:
            self.log_message(f"You guessed {guess}.")

        if guess == self.random_number:
            if self.game_mode == "Two Player":
                self.log_message(f"{current_player_name} guessed correctly!")
                QMessageBox.information(self, "Winner", f"{current_player_name} wins!")
            else:
                self.log_message(f"You guessed correctly!")
                QMessageBox.information(self, "Congratulations", f"You guessed it, {self.player_name}!")
            self.guess_button.setEnabled(False)
            self.game_started = False
            self.show_play_again_dialog()
        elif self.attempts_left == 0:
            self.log_message(f"Out of attempts. The number was {self.random_number}.")
            QMessageBox.information(self, "Game Over", f"Sorry, you're out of attempts. The number was {self.random_number}.")
            self.guess_button.setEnabled(False)
            self.game_started = False
            self.show_play_again_dialog()
        elif guess < self.random_number:
            self.feedback_label.setText("Too low!")
            self.start_feedback_animation()
        else:
            self.feedback_label.setText("Too high!")
            self.start_feedback_animation()
        self.guess_input.clear()

        if self.game_mode == "Two Player":
            self.current_player = 3 - self.current_player
            self.instruction_label.setText(f"It's {self.player1_name if self.current_player == 1 else self.player2_name}'s turn to guess.  Number between 1 and 100.")

    def show_play_again_dialog(self):
        """
        Asks the user if they want to play again.
        """
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Play Again?")
        message_box.setText("Do you want to play again?")
        message_box.addButton(QMessageBox.Yes)
        message_box.addButton(QMessageBox.No)
        message_box.setDefaultButton(QMessageBox.Yes)
        result = message_box.exec_()
        if result == QMessageBox.Yes:
            self.start_new_game()
        else:
            self.close()

    def log_message(self, message):
        """
        Adds a message to the game log.
        """
        self.game_log.append(message)
        self.game_log.ensureCursorVisible()

    def start_feedback_animation(self):
        """
        Starts a timer to cycle through colors for the feedback label.
        """
        self.feedback_color_index = 0
        self.timer.start(200)  # Update every 200 milliseconds

    def update_feedback_label(self):
        """
        Updates the feedback label color.
        """
        self.feedback_color_index = (self.feedback_color_index + 1) % len(self.feedback_colors)
        self.feedback_label.setStyleSheet(f"color: {self.feedback_colors[self.feedback_color_index]}")
        if self.feedback_color_index == 0:
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = NumberGuessingGame()
    game.show()
    sys.exit(app.exec_())

