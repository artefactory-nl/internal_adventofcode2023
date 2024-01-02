from abc import abstractmethod
from dataclasses import dataclass
from functools import total_ordering
from typing import Self, final

@dataclass(frozen=True)
@total_ordering
class BaseCard:
    rank: str

    def __post_init__(self):
        if type(self.rank) is not str:
            raise TypeError("Field 'value' must be of type 'str'.")
    
    @final
    def get_rank(self) -> str: return self.rank
    
    @abstractmethod
    def get_numerical_value(self) -> int:
        raise NotImplementedError("get_numerical_value() not implemented")
        
    @final
    def __repr__(self) -> str: return f"Card('{self.rank}')"
    
    @final
    def __gt__(self, other: Self) -> bool:
        return self.get_numerical_value() > other.get_numerical_value()
    
    @final
    def __lt__(self, other: Self) -> bool:
        return self.get_numerical_value() < other.get_numerical_value()

    @final
    def __eq__(self, other: Self) -> bool:
        return self.get_numerical_value() == other.get_numerical_value()
    
    @final
    def __ge__(self, other: Self) -> bool:
        return self.get_numerical_value() >= other.get_numerical_value()
    
    @final
    def __le__(self, other: Self) -> bool:
        return self.get_numerical_value() <= other.get_numerical_value()
