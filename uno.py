import random

############################################# DECK CREATION ##########################################
# Create an empty list for the deck
deck = []

# Create the card colors and numbers
card_colors = ["Green", "Yellow", "Blue", "Red"]
card_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Add number cards to the deck
for color in card_colors:
    deck.append({"color": color, "number": "0"})
    for number in card_numbers[1:]:
        deck.append({"color": color, "number": number})
        deck.append({"color": color, "number": number})

# Define the action cards
card_actions = ["skip", "Reverse", "Draw 2"]

# Add action cards to the deck
for color in card_colors:
    for action in card_actions:
        deck.append({"color": color, "action": action})
        deck.append({"color": color, "action": action})

# Define wild cards
wild_cards = ["Wild", "Wild Draw Four"]

# Add wild cards to the deck
for wild in wild_cards:
    for _ in range(4):
        deck.append({"wild_type": wild})

######################################### Shuffle the deck ######################################
random.shuffle(deck)


######################################### GAME MODE SELECTION #######################################
print('Welcome to the "UNO card game"')
print("Do you want to play single-player or multiplayer?")

while True:
    game_type = input("Type 'computer' for single-player or 'multiplayer' for multiplayer: ").lower()
    
    if game_type == "computer":
        print(f"You are playing against the computer.")
        player_names = [input("Enter your name: "), "Computer"]
        break
    elif game_type == "multiplayer":
        print(f"You are playing with multiple players.")
        print("How many players are going to play? Choose between 2 and 10")
        
        while True:
            no_of_players = input()
            if no_of_players.isdigit():
                no_of_players = int(no_of_players)
                if 2 <= no_of_players <= 10:
                    print(f"{no_of_players} players are going to play.")
                    break
                else:
                    print("Please enter a number between 2 and 10.")
            else:
                print("Please enter a number between 2 and 10.")
        
        # Ask for player names
        player_names = []
        for player in range(no_of_players):
            player_name = input(f"Enter the name of player {player + 1}: ")
            player_names.append(player_name)
        break
    else:
        print("Invalid choice. Choose between 'computer' and 'multiplayer'")

# Initialize player cards
player_cards = {player: [] for player in player_names}

# Deal 7 cards to each player
for _ in range(7):
    for player in player_names:
        player_cards[player].append(deck.pop())

# Display each player's cards (for multiplayer) or single player's cards
if game_type == "multiplayer":
    for player, cards in player_cards.items():
        print(f"{player}'s cards: {cards}")
else:
    print(f"\n{player_names[0]}'s cards: {player_cards[player_names[0]]}")

# Initialize discard pile with one card from the deck
discard_pile = [deck.pop()]
print(f"\nStarting card on the discard pile: {discard_pile[-1]}")

# Function to check if a card can be played
def can_play_card(card, top_card):
    if "wild_type" in card:
        return True  # Wild cards can always be played
    if card["color"] == top_card.get("color") or card.get("number") == top_card.get("number"):
        return True
    return False

# Function to handle drawing a card
def draw_card(player):
    if deck:
        drawn_card = deck.pop()
        player_cards[player].append(drawn_card)
        print(f"{player} draws a card: {drawn_card}")
    else:
        print("No more cards in the deck!")

# Function to handle a player's turn
def player_turn(player):
    global discard_pile
    print(f"\n{player}'s turn")

    if player == "Computer":
        # Computer's turn: Play a valid card or draw
        for card in player_cards["Computer"]:
            if can_play_card(card, discard_pile[-1]):
                print(f"Computer plays {card}")
                player_cards["Computer"].remove(card)
                discard_pile.append(card)
                return
        print("Computer has no matching card!")
        draw_card("Computer")

    else:
        # Player's turn: Play a card or draw
        print(f"Your cards: {player_cards[player]}")
        top_card = discard_pile[-1]
        print(f"Top card: {top_card}")

        # Let the player choose a card to play
        while True:
            chosen_card_idx = input(f"Choose a card to play (1-{len(player_cards[player])}) or 'D' to draw: ")
            if chosen_card_idx.lower() == 'd':
                draw_card(player)
                return

            if chosen_card_idx.isdigit():
                chosen_card_idx = int(chosen_card_idx) - 1
                if 0 <= chosen_card_idx < len(player_cards[player]):
                    chosen_card = player_cards[player][chosen_card_idx]
                    if can_play_card(chosen_card, top_card):
                        print(f"You played {chosen_card}")
                        player_cards[player].remove(chosen_card)
                        discard_pile.append(chosen_card)
                        return
                    else:
                        print(f"You cannot play {chosen_card}, it doesn't match the top card.")
                else:
                    print("Invalid card number. Try again.")
            else:
                print("Invalid input. Please enter a card number or 'D' to draw.")

# Main game loop for multiplayer and single-player
while True:
    for player in player_names:
        player_turn(player)
        if len(player_cards[player]) == 0:
            print(f"\n{player} wins! No more cards in hand!")
            break
    else:
        continue  # Continue the game if no one has won yet
    break  # Exit the game loop if someone has won