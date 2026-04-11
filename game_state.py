from player import Player
from wall import Wall
from discard_pile import DiscardPile
from tiles import Tile, Suit, HONOR_TILES, WIND_TILES

class GameState:
    """Round-level state manager for the 4-player game."""

    def __init__(self, player_names):
        if len(player_names) != 4:
            raise ValueError("Gamestate requires four players.")
        
        winds = ['Dong','Nan','Xi','Bei'] #Start with player at East (Dong) and move CC (ESWN)
        self.players = [Player(name, wind) for name, wind in zip(player_names, winds)]
        self.wall = Wall() #Creates a wall 
        self.discard_pile = DiscardPile()
        self.current_player_idx = 0
        self.round_started = False

    @property 
    def current_player(self):
        return self.players[self.current_player_idx]
    
    def _build_standard_wall_tiles(self):
        """Build the standard 136-tile wall (no flowers)"""
        tiles = []

        #Regular tiles
        for suit in (Suit.Tiao, Suit.Wan, Suit.Tong):
            for value in range(1,10):
                for _ in range(4):
                    tiles.append(Tile(value,suit))

        #Honor tiles
        for value in HONOR_TILES:
            suit = Suit.Fang if value in WIND_TILES else Suit.Dragon
            for _ in range(4):
                tiles.append(Tile(value, suit))

        return tiles
    
    def setup_round(self):
        """
        1. Resets the state
        2. Build wall
        3. Shuffle the wall 
        4. deal 13 tiles to each player
        We ignore the IRL process of rolling a dice, and picking stacks of 4 tiles of the wall depending on the results
        """
        
        self.wall = Wall(self._build_standard_wall_tiles())
        self.wall.shuffle()
        self.discard_pile = DiscardPile()
        self.current_player_idx = 0

        # reset player hands
        for player in self.players: 
            player.hand = player.hand.__class__()

        # deal 13 