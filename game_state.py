from player import Player
from wall import Wall
from discard_pile import DiscardPile
from tiles import Tile, Suit, HONOR_TILES, WIND_TILES
from hand import Hand

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
            player.hand = Hand()

        # deal 13 tiles to each player
        #Each player picks up 13 tiles in a row, one after the other
        for _ in range(13):
            for player in self.players:
                player.draw_tile(self.wall.draw())
            
        self.round_started = True

    def draw_for_current_player(self):
        if not self.round_started:
            raise RuntimeError("Round has not yet started.")
        if self.wall.is_empty():
            raise RuntimeError("Cannot draw: wall empty.")
        
        drawn_tile = self.wall.draw()
        self.current_player.draw_tile(drawn_tile)
        return drawn_tile 
    
    def discard_for_current_player(self, tile):
        if not self.round_started:
            raise RuntimeError("Round has not yet started.")
        if not isinstance(tile, Tile):
            raise TypeError("discard_tile_for_current_player expects a Tile")
        
        discarded_tile = self.current_player.discard_tile(tile)
        self.discard_pile.add(discarded_tile)
        return discarded_tile
    
    def next_turn(self) -> None:
        self.current_player_idx = (self.current_player_idx + 1 ) % 4 #will always have index 0,1,2,3

    def snapshot(self):
        return {
            "current_player": self.current_player.name, 
            "remaining_wall_tiles": len(self.wall),
            "discarded_amount": len(self.discard_pile),
            "hand_sizes": {p.name: len(p.hand) for p in self.players}
        }