from tiles import Tile


class Hand: 
    """Represents a player hand."""

    def __init__(self, tiles=None):
        if tiles is not None:
            self._tiles = list(tiles)
        else: 
            self._tiles = []
        self.sort()

    @property
    def tiles(self):
        """Read-only view so outside code cannot mutate internal list directly."""
        return tuple(self._tiles)
    
    def __len__(self):
        return len(self._tiles)
    
    def __iter__(self):
        return iter(self._tiles)
    
    def __repr__(self):
        return f'Hand({self._tiles!r})'

    def __str__(self):
        if not self._tiles:
            return "(empty hand)"
        return "\n".join(str(tile) for tile in self._tiles)

    def sort(self):
        self._tiles.sort()

    def add_tile(self, tile, auto_sort=True):
        """Add one tile to hand."""

        if not isinstance(tile, Tile):
            raise TypeError("add_tile expects a Tile")
        
        self._tiles.append(tile)

        if auto_sort:
            self.sort()

    def discard_tile(self, tile):
        """Discards a tile."""

        if not isinstance(tile, Tile):
            raise TypeError("add_tile expects a Tile")

        try:
            target_idx = self._tiles.index(tile)  # uses Tile.__eq__
        except ValueError:
            raise ValueError(f"Cannot discard {tile}: tile not in hand.")
        
        if len(self._tiles) != 14:
            raise RuntimeError(
                f"Hand size violated before discard: expected 14, got {len(self._tiles)}."
            )

        discarded_tile = self._tiles.pop(target_idx)

        return discarded_tile
    
    def count_specific_tile(self, tile):
        """Count occurrences of a specific tile."""
        return sum(1 for t in self._tiles if t == tile)