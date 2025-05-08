import random
import math
import json
import time

def guess(x, max_attempts=0, player_name="", hints_enabled=False, game_mode="single"):
    """
    This function makes the user guess a random number between 1 and x.
    It provides feedback if the guess is too low or too high.  It also limits
    the number of attempts if max_attempts is provided.

    Args:
        x: The upper bound of the range for the random number.
        max_attempts: The maximum number of attempts allowed (optional).
        player_name: The name of the player (optional, for high scores).
        hints_enabled:  Boolean to enable/disable hints.
        game_mode: "single" or "two_player"
    """
    random_number = random.randint(1, x)
    guess_count = 0
    if max_attempts > 0:
        print(f"You have {max_attempts} attempts to guess the number.")
    while True:
        guess_count += 1
        try:
            guess = int(input(f'Guess a number between 1 and {x}: '))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if guess < random_number:
            print('Sorry, guess again. Too low.')
        elif guess > random_number:
            print('Sorry, guess again. Too high.')
        else:
            print(
                f'Yay, congrats, {player_name}! You have guessed the number {random_number} correctly in {guess_count} guesses!!')
            if player_name and game_mode == "single":
                save_high_score(player_name, guess_count)
            return True
        if max_attempts > 0 and guess_count >= max_attempts:
            print(f"Sorry, you've run out of attempts. The number was {random_number}.")
            return False
        if hints_enabled:
            if guess_count % 3 == 0:
                print(f"Hint: The number is {'even' if random_number % 2 == 0 else 'odd'}.")



def computer_guess(x):
    """
    This function makes the computer guess a number between 1 and x
    that the user is thinking of. It uses a binary search approach
    to efficiently find the number.
    Args:
        x: The upper bound of the range for the number to be guessed.
    """
    low = 1
    high = x
    feedback = ''
    while feedback != 'c':
        if low != high:
            guess = (low + high) // 2
        else:
            guess = low
        print(f"Is your number {guess}?")
        feedback = input(
            f'Is the number too high (H), too low (L), or correct (C)?? ').lower()
        if feedback == 'h':
            high = guess - 1
        elif feedback == 'l':
            low = guess + 1
        elif feedback != 'c':
            print("Invalid input. Please enter 'H', 'L', or 'C'.")
    print(f'Yay! The computer guessed your number, {guess}, correctly!')




def play_again():
    """
    Asks the user if they want to play again.  Returns True if they do,
    False otherwise.
    """
    while True:
        answer = input("Do you want to play again? (yes/no): ").lower()
        if answer == "yes":
            return True
        elif answer == "no":
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")




def choose_game():
    """
    Prompts the user to choose which game to play (guess the number,
    computer guess, or two-player). Returns 1 for user guess, 2 for
    computer guess, 3 for two-player, or 0 to exit.
    """
    while True:
        try:
            choice = int(input(
                "Choose a game:\n1. Guess the number\n2. Let the computer guess your number\n3. Two-player guess the number\n0. Exit\nEnter your choice: "))
            if choice in [0, 1, 2, 3]:
                return choice
            else:
                print("Invalid input. Please enter 0, 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")




def get_difficulty():
    """
    Prompts the user to choose a difficulty level.
    Returns the maximum number of attempts based on the difficulty.
    """
    while True:
        try:
            difficulty = int(input(
                "Choose difficulty:\n1. Easy (10 attempts)\n2. Medium (5 attempts)\n3. Hard (3 attempts)\n4. Custom attempts\nEnter your choice: "))
            if difficulty == 1:
                return 10
            elif difficulty == 2:
                return 5
            elif difficulty == 3:
                return 3
            elif difficulty == 4:
                while True:
                    attempts_input = input("Enter the number of attempts: ")
                    try:
                        attempts = int(attempts_input)
                        if attempts > 0:
                            return attempts
                        else:
                            print("Number of attempts must be positive.")
                    except ValueError:
                        print("Invalid input. Please enter a positive number.")
            else:
                print("Invalid input. Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")




def get_player_name(player_num):
    """
    Gets the player's name.
    """
    name = input(f"Enter Player {player_num}'s name: ")
    return name




def save_high_score(player_name, score):
    """
    Saves the player's high score to a JSON file (high_scores.json).
    Handles potential errors during file operations.
    """
    high_scores = {}
    try:
        with open("high_scores.json", "r") as f:
            try:
                high_scores = json.load(f)
            except json.JSONDecodeError:
                print("Error decoding high scores file.  Starting with empty scores.")
                high_scores = {}
    except FileNotFoundError:
        print("Starting with empty high scores (no existing file).")

    if player_name in high_scores:
        if score < high_scores[player_name]:
            high_scores[player_name] = score
            print("New high score!")
    else:
        high_scores[player_name] = score
        print("Score saved!")
    try:
        with open("high_scores.json", "w") as f:
            json.dump(high_scores, f)
    except Exception as e:
        print(f"Error writing high scores to file: {e}")




def display_high_scores():
    """
    Displays the high scores from the JSON file.  Handles file errors.
    """
    try:
        with open("high_scores.json", "r") as f:
            high_scores = json.load(f)
    except FileNotFoundError:
        print("No high scores available yet.")
        return
    except json.JSONDecodeError:
        print("Error reading high scores.  The file may be corrupted.")
        return

    if not high_scores:
        print("No high scores available yet.")
        return

    print("\n--- High Scores ---")
    for player, score in high_scores.items():
        print(f"{player}: {score} guesses")




def show_instructions():
    """
    Displays the instructions for the game.
    """
    print("\n--- How to Play ---")
    print("In this game, you try to guess a secret number.")
    print("The computer will tell you if your guess is too high or too low.")
    print("You can choose the difficulty, which affects the number of attempts.")
    print("Try to guess the number in as few attempts as possible!")




def play_sound(sound):
    """
    Plays a sound effect (simulated with text).
    Args:
        sound: The name of the sound effect ('win', 'lose', 'guess').
    """
    if sound == 'win':
        print("🎉🎉🎉 You win! 🎉🎉🎉")
    elif sound == 'lose':
        print("😞😞😞 You lose! 😞😞😞")
    elif sound == 'guess':
        print("🔊 Guessing...")
    elif sound == 'invalid':
        print("❌ Invalid Input ❌")
    time.sleep(0.5)




def two_player_game(x):
    """
    A two-player version of the number guessing game.
    """
    player1_name = get_player_name(1)
    player2_name = get_player_name(2)
    max_attempts = get_difficulty()
    print(f"Okay, {player1_name} and {player2_name}, let's begin!")
    random_number = random.randint(1, x)
    turn = 1
    while True:
        print(f"\nIt's {player_name}'s turn.")
        if turn == 1:
            player_name = player1_name
        else:
            player_name = player2_name
        guess_result = guess(x, max_attempts, player_name, game_mode="two_player")
        if guess_result:
            play_sound('win')
            print(f"{player_name} wins!")
            break
        elif guess_result == False:
            play_sound('lose')
            break
        else:
            turn = 3 - turn




def main():
    """
    Main function to run the number guessing game.
    """
    show_instructions()
    while True:
        choice = choose_game()
        if choice == 0:
            print("Thanks for playing!")
            break
        elif choice == 1:
            player_name = get_player_name(1)
            max_attempts = get_difficulty()
            hints_enabled = input("Enable hints? (yes/no): ").lower() == "yes"
            guess(10, max_attempts, player_name, hints_enabled)
            display_high_scores()
        elif choice == 2:
            computer_guess(10)
        elif choice == 3:
            two_player_game(10)
        if not play_again():
            print("Thanks for playing!")
            break



if __name__ == "__main__":
    main()

 
