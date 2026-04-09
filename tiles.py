from enum import Enum
from functools import total_ordering

CHINESE_NUMBERS = {
        1: '一',
        2: '二',
        3: '三',
        4: '四',
        5: '五',
        6: '六',
        7: '七',
        8: '八',
        9: '九'
    }

class Suit(Enum):
    """Enumeration for Mahjong tile suits. Suits will be sorted in ascending order."""

    Tiao = 1                            
    Wan = 2  
    Tong = 3        
    Fang = 4       # Dong, Nan, Xi, Bei
    Dragon = 5     # Hong zhong, Fa cai, Bai

@total_ordering
class Tile:
    """Represents a single Mahjong tile."""

    # Custom ordering for non-numerical tiles to allow proper hand sorting
    _honor_order = {
        'Bei': 1, 'Dong': 2, 'Nan': 3, 'Xi': 4,
        'Hong zhong': 1, 'Fa cai': 2, 'Bai ban': 3
    }

    def __init__(self, suit: Suit, value: int | str):
        self.suit = suit
        self.value = value

    @property
    def is_honor(self) -> bool:
        """Returns True if the tile is a Fang or Dragon."""

        return self.suit in (Suit.FANG, Suit.DRAGON)
    
    @property
    def is_numerical(self) -> bool:
        """Returns True if the tile is a 1 or 9 of a suited tile."""

        if self.is_honor:
            return False
        
        return self.value in (1, 9)
    
    def __eq__(self, other) -> bool:
        """Checks if two tiles are identical (useful for pairs/pongs)."""

        if not isinstance(other, Tile):
            return NotImplemented #Tells python to not attempt to handle the comparison if not both tile objects
        
        return self.suit == other.suit and self.value == other.value
    
    def __lt__(self, other) -> bool:
        """Defines how tiles should be sorted in a player's hand."""
        if not isinstance(other, Tile):
            return NotImplemented #Tells python to not attempt to handle the comparison if not both tile objects
        
        # Sort by suit first
        if self.suit != other.suit:
            return self.suit.value < other.suit.value
        
        # If suits are the same, sort by value
        if self.is_honor:
            self_val = self._honor_order.get(self.value, 99) #get numerical order value from the dict from the value string, else set to 99
        else: 
            self_val = self.value

        if other.is_honor: 
            other_val = self._honor_order.get(other.value, 99) #get numerical order value from the dict from the value string, else set to 99
        else: 
            other_val = other.value
        
        return self_val < other_val #return comparison of: self less than other
    
        ##alternate 
        #self_val = self.value if not self.is_honor else self._honor_order.get(self.value, 99)
        #other_val = other.value if not other.is_honor else self._honor_order.get(other.value, 99)
        #return self_val < other_val

    
    def __str__(self) -> str:
        """User-friendly string representation."""
        if self.suit in Suit.Dragon: 
            return f'{self.value}'
        
        if self.suit in Suit.Fang: 
            return f'{self.value} {self.suit.name}'

        else: 
            chinese_val = CHINESE_NUMBERS.get(self.value, self.value)

            return f'{chinese_val} {self.suit.name}'
        
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        return f"Tile({repr(self.value)}, {self.suit})"