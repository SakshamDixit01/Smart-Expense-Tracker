import random

CHOICES = ["rock", "paper" , "scoissor"]

def get_computer_choice():
    return random.choice(CHOICES)

def determine_winner(player, computer):
    if player == computer:
        return "tie"

    if (
        (player== "rock" and computer == "scissors")
        or (player == "paper" and computer == "rock")
        or (player == "scissors" and computer == "paper")

    ):
        return "player"

    return "computer"

