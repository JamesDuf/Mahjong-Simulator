from hand import Hand
from tiles import Tile

class Player: 
    """Represents one player."""

    def __init__(self, name, wind):
        self.name = name 
        self.wind = wind
        self.hand = Hand() #Creates a default hand
    
    def __repr__(self):
        return f"Player({self.name}, wind={self.wind})"
    
    def __str__(self):
        return f"{self.name} ({self.wind})\n{self.hand}"
    
    def draw_tile(self, tile):
        """Draws one tile into player's hand"""
        if not isinstance(tile, Tile):
            raise TypeError("draw_tile expects a Tile")
        self.hand.add_tile(tile)

    def discard_tile(self,tile):
        """Removes a tile from the player's hand and places it in the discard pile"""
        if not isinstance(tile,Tile):
            raise TypeError("discard_tile expects a Tile")
        return self.hand.discard_tile(tile)

