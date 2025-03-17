from dataclasses import dataclass

@dataclass
class CartItem:
    name: str
    price: float
    count: int


    def __init__(self, name: str, price: float, count: int):
        self.name = name
        self.price = price
        self.count = count
