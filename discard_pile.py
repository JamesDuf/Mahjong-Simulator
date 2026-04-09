from tiles import Tile

class DiscardPile:
    """Ordered list of discarded tiles."""

    def __init__(self):
        self._tiles = []

    @property
    def tiles(self):
        return tuple(self._tiles)
    
    def __len__(self):
        return len(self._tiles)

    def __iter__(self):
        return iter(self._tiles)

    def __repr__(self):
        return f"DiscardPile({self._tiles!r})"
    
    def __str__(self):
        if not self._tiles:
            return "(empty discard pile)"
        return "\n".join(str(t) for t in self._tiles)
    
    def add(self, tile):
        """Add one discarded tile."""
        if not isinstance(tile, Tile):
            raise TypeError("DiscardPile.add expects a Tile")
    
        self._tiles.append(tile)

    def last(self):
        """Peek last discarded tile, or None if empty."""
        if not self._tiles:
            return None
        else: 
            return self._tiles[-1] 
        
    def claim_last(self):
        """
        Remove and return the last discarded tile. (player claims it for pong)
        """
        if not self._tiles:
            raise RuntimeError("Cannot claim from empty discard pile.")
        
        claimed_tile = self._tiles.pop()
        return claimed_tile