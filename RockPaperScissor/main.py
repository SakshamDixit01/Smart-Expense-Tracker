import json 
from pathlib import Path


from game_logic import get_computer_choice , determine_winner

SCORE_FILE  = Path(__file__).with_name("score.json")


def load_score():
    if SCORE_FILE.exists():
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError , OSError):

            pass
    return {
        "player_wins": 0,
        "computer_wins": 0,
        "draws": 0
    }

def save_score(score):
    with open(SCORE_FILE, "w" , encoding = "utf-8" ) as file:
        json.dump(score , file , indent=4)


def play_game():
    score = load_score()


    print("\n ==== ROCK PAPER SCISSORS ====")

    print("1.Rock")
    print("2.Paper")
    print("3.Scissors")
    print("Q. Quit")


    while True:
        player_input = input("\n Enter your Choice :  ").strip().lower()


        if player_input == "q":
            break

        choices = {
            "1" : "rock",
            "2": "paper",
            "3": "scissors"
        }

        if player_input not in choices:
            print("Invalid choice! Enter 1,2,3, or Q.")
            continue

        player = choices[player_input]
        computer = get_computer_choice()

        print(f"\n You Chose : {player.title()}")
        print(f"Computer Choice : {computer.title}")

        result = determine_winner(player, computer)

        if result == "player":
            print("You win this round !")
            score["player_wins"] += 1

        elif result == "computer":
            print("Computer wins this round!")
            score["Computer wins"] += 1

        else:
            print("It is a Draw!")

        save_score(score)


        print("\n ---- SCOREBOARD ----")

        print(f"Your Wins : {score['player_wins']}")
        print(f"Computer Wins : {score['computer_wins']}")
        print(f"Draws: {score['draws']}")

    if __name__ == "__main__":
        play_game()

