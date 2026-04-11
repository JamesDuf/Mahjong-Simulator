from random import shuffle
from tiles import Tile


class Wall:
    """Tiles remaining in the round."""

    def __init__(self, tiles):
        self._tiles = list(tiles)

    @property
    def tiles(self):
        return tuple(self._tiles)

    def __len__(self):
        return len(self._tiles)

    def __repr__(self):
        return f"Wall(remaining={len(self._tiles)})"

    def shuffle(self):
        shuffle(self._tiles)

    def is_empty(self):
        return len(self._tiles) == 0

    def draw(self):
        """Draw one tile from the front of the wall."""
        if not self._tiles:
            raise RuntimeError("Cannot draw: wall is empty.")
        
        drawn_tile = self._tiles.pop(0)
        return drawn_tile