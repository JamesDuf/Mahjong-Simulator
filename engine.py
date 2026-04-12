from game_state import GameState

def choose_tile_to_discard(player):
    print("\nYour hand:")
    for i, tile in enumerate(player.hand, start = 1):
        print(f"{i}: {tile}") #that way the tiles are indexed, even if not useful specifically for this print statement

    while True:
        choice = input("Choose a tile number to discard: ").strip()

        if not choice.isdigit():
            print("Please enter a valid tile index.")
            continue

        index = int(choice) - 1 #because the tile number printed starts at 1, so shift it down by 1

        if index < 0 or index >= len(player.hand):
            print("Index is out of range.")
            continue

        return player.hand.tiles[index]
    
def main():
    game_state = GameState(
        ['Alice', 'Bob', 'Charlie', 'David']
    )

    game_state.setup_round()

    while True:

        if game_state.wall.is_empty():
            print("Wall is empty. Round is over, nobody wins.")
            break

        player = game_state.current_player
        print(f"\nCurrent Player: {player.name} ({player.wind})")

        drawn_tile = game_state.draw_for_current_player()
        print(f"{player.name} drew: {drawn_tile}")

        tile_to_discard = choose_tile_to_discard(player) #will prompt player for choice
        discarded_tile = game_state.discard_for_current_player(tile_to_discard)
        print(f"{player.name} discarded: {discarded_tile}")

        game_state.next_turn()

        print("\nState snapshot:")
        print(game_state.snapshot())

        

if __name__ == "__main__":
    main()